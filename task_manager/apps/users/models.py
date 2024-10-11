from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group, Permission
from django.utils import timezone
from datetime import date, datetime, timedelta

# Create your models here.
class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        user = self.model(email=self.normalize_email(email),
                          is_active=True,
                          is_staff=is_staff,
                          is_superuser=is_superuser,
                          last_login=timezone.now(),
                          created=timezone.now(),
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        is_staff = extra_fields.pop('is_staff', True)
        is_superuser = extra_fields.pop('is_superuser', False)
        return self._create_user(email, password, is_staff, is_superuser, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, is_staff=True, is_superuser=True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(verbose_name="Nombres", max_length=255)
    lastname = models.CharField(verbose_name="Apellidos", max_length=255)
    document = models.CharField(verbose_name='Documento', max_length=30, blank=True,null=True)
    email = models.EmailField(verbose_name='Correo Electrónico', unique=True, max_length=255)
    phone =  PhoneField(blank=True, help_text='Telefono/Celular')
    avatar = models.ImageField(verbose_name='Foto Perfil', upload_to='user_profile/', blank=True, null=True)
    is_admin = models.BooleanField(verbose_name='Admin', default=False)
    is_active = models.BooleanField(verbose_name='Activo/Inactivo', default=True)
    is_staff = models.BooleanField(verbose_name='Permiso al PA', default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Nombre único para evitar el choque
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='Grupo',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set_permissions',  # Nombre único para evitar el choque
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='Permiso de Usuario',
    )
    created = models.DateTimeField(verbose_name='Creada el', auto_now_add=True, blank=True, null=True, help_text='La fecha de creacion de este objeto')
    modified = models.DateTimeField(verbose_name='Modificada el', auto_now=True, blank=True, null=True, help_text='la fecha de modificacion de este objeto')

    # Fields settings
    REQUIRED_FIELDS = [] # removes email from REQUIRED_FIELDS
    USERNAME_FIELD = 'email'
    objects = UserManager()
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        if self.document:
            return self.name +" "+ self.lastname+" - "+self.document
        else:
            return self.name +" "+ self.lastname

    def name_complete(self):
        return self.name +" "+ self.lastname


    def name_short(self):
        print(f"Nombre completo: {self.name_complete()}")  # Para depuración
        #names = (self.name).split()[0] +" "+ (self.lastname).split()[0]  # Suponiendo que 'name' es un campo que contiene el nombre completo.
        names = self.name.split()
        if names:
            return names[0]
        return "nombre no disponible"

class UtilsData(models.Model):
    created = models.DateTimeField(
        'creada el',
        auto_now_add=True,
        blank=True,
        null=True,
        help_text='La fecha de creacion de este objeto',
    )
    modified = models.DateTimeField(
        'modificada el',
        auto_now=True,
        help_text='la fecha de modificacion de este objeto',
    )
    enable = models.BooleanField("Visible/No Visible", default=True)
    user = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.SET_NULL, blank=True, null=True)

class Customer(UtilsData):
    name = models.CharField(verbose_name="Nombre / Razon social", max_length=255)
    email =  models.EmailField(verbose_name="Correo", max_length=254)
    phone =  PhoneField(verbose_name="Telefono/Celular", blank=True, help_text='Contact phone number')


