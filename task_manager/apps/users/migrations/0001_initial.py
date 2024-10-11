# Generated by Django 5.1.1 on 2024-10-08 20:33

import django.db.models.deletion
import phone_field.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UtilsData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='La fecha de creacion de este objeto', null=True, verbose_name='creada el')),
                ('modified', models.DateTimeField(auto_now=True, help_text='la fecha de modificacion de este objeto', verbose_name='modificada el')),
                ('enable', models.BooleanField(default=True, verbose_name='Visible/No Visible')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('name', models.CharField(max_length=255)),
                ('lastname', models.CharField(max_length=255)),
                ('document', models.CharField(blank=True, max_length=30, null=True, verbose_name='Documento')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Correo Electrónico')),
                ('phone', phone_field.models.PhoneField(blank=True, help_text='Telefono/Celular', max_length=31)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='user_profile/', verbose_name='Foto Perfil')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Admin')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo/Inactivo')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Permiso al PA')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creada el')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Modificada el')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='custom_user_set', to='auth.group', verbose_name='Grupo')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='custom_user_set_permissions', to='auth.permission', verbose_name='Permiso de Usuario')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('utilsdata_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.utilsdata')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre / Razon social')),
                ('email', models.EmailField(max_length=254, verbose_name='Correo')),
                ('phone', phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31, verbose_name='Telefono/Celular')),
            ],
            bases=('users.utilsdata',),
        ),
        migrations.AddField(
            model_name='utilsdata',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Creado por'),
        ),
    ]