from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from apps.tasks.models import Task
from apps.users.models import User, Customer
from rest_framework.authtoken.models import Token
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.models import Group


#Gestion de converson de imagenes desde el serializer
class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64, six, uuid
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
                try:
                    decoded_file = base64.b64decode(data)
                except Exception:
                    raise serializers.ValidationError(_('Invalid image format'))
                file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
                # Get the file name extension:
                file_extension = self.get_file_extension(header)
                complete_file_name = "%s.%s" % (file_name, file_extension,)
                data = ContentFile(decoded_file, name=complete_file_name)
            else:
                raise serializers.ValidationError(_('Invalid image format'))
        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, header):
        data, format =  header.split('/')
        return format

class TaskSerializer(serializers.ModelSerializer):
    #user_id = serializers.ReadOnlyField(source='user.id')
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    class Meta:
        model = Task
        fields =['id','title','description','completed','created_at','updated_at','completed_at','enabled', 'formatted_duration']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'lastname', 'document', 'email', 'phone', 'avatar', 'enabled','groups']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id",'name', 'email', 'phone']




class UserLoginSerializer(serializers.Serializer):  # SERIALIZERS DE USUARIOS (LOGIN)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=5, max_length=64)

    def validate(self, data):
        # print("Validate Serializer", data['email'], data['password'])
        user = authenticate(email=data['email'], password=data['password'])
        # print("user", user)
        if not user:
            raise serializers.ValidationError('Las credenciales no son válidas')
        self.context['user'] = user
        return data

    def create(self, data):
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class UserSignUpSerializer(serializers.Serializer): # SERIALIZERS DE REGISTRO DE USUARIOS CUANDO SE ENVIA FORM CON FOTO
    email = serializers.EmailField( validators=[UniqueValidator(queryset=User.objects.all(), message=("Este Correo Ya existe"))], required=True )
    password = serializers.CharField(min_length=8, max_length=64, required=True)
    password_confirmation = serializers.CharField(min_length=8, max_length=64, required=True)
    name = serializers.CharField(min_length=2, max_length=50, required=True)
    lastname = serializers.CharField(min_length=2, max_length=100)
    document = serializers.CharField(min_length=2, max_length=100, validators=[UniqueValidator(queryset=User.objects.all(), message=("Esta identificacion Ya existe"))], required=True )
    phone = serializers.CharField(min_length=2, max_length=20, required=True)
    avatar = Base64ImageField(use_url=True, required=False,allow_null=True)
    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        return {
            'id': user.id,  # Devuelve el ID del usuario creado
            'user': user
        }

class UserSignUpNoSerializer(serializers.Serializer): # SERIALIZERS DE REGISTRO DE USUARIOS CUANDO SE ENVIA FORM SIN FOTO
    email = serializers.EmailField( validators=[UniqueValidator(queryset=User.objects.all(), message=("Este Correo Ya existe"))], required=True )
    password = serializers.CharField(min_length=8, max_length=64, required=True)
    password_confirmation = serializers.CharField(min_length=8, max_length=64, required=True)
    name = serializers.CharField(min_length=2, max_length=50, required=True)
    lastname = serializers.CharField(min_length=2, max_length=100)
    document = serializers.CharField(min_length=2, max_length=100, validators=[UniqueValidator(queryset=User.objects.all(), message=("Esta identificacion Ya existe"))], required=True )
    phone = serializers.CharField(min_length=2, max_length=20, required=True)
    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        return {
            'id': user.id,  # Devuelve el ID del usuario creado
            'user': user
        }



class GroupSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    class Meta:
        model = Group
        fields = ['id', 'text']  # Ajusta los campos según lo que necesites

    def get_text(self, obj):
        return obj.name.upper()
