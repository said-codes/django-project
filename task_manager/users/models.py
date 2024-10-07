from django.db import models
from phone_field import PhoneField

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email =  models.EmailField(max_length=254)
    phone =  PhoneField(blank=True, help_text='Contact phone number')
    photo = models.ImageField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
