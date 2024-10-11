from django.core.exceptions import ValidationError
from .models import Customer
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'lastname', 'email', 'phone', 'avatar']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Correo Electrónico', max_length=254)

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        User = get_user_model()

        # Asegúrate de que el usuario exista
        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError('Usuario no encontrado.')

            # Verifica la contraseña
            if not user.check_password(password):
                raise forms.ValidationError('Contraseña incorrecta.')

        return super().clean()

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'enable']  # Añade más campos si es necesario


class UpdateProfilePictureForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']  # Campo de la foto de perfil


User = get_user_model()

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Verifica que las contraseñas coincidan
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        # Verifica la longitud mínima de la contraseña
        if password1 and len(password1) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está en uso.")
        return email

class UpdateUserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'phone']

    widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
