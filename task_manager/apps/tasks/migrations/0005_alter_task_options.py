# Generated by Django 5.1.1 on 2024-10-08 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_task_enabled'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'permissions': [('reactivate_task', 'Puede reactivar tareas')]},
        ),
    ]
