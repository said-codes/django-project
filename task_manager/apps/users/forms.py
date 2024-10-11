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
