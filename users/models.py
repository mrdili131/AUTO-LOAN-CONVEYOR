from django.db import models
from django.contrib.auth.models import AbstractUser

roles = (
    ('new','Yangi'),
    ('creditor','Kreditor'),
    ('accountant','Buxgalter'),
    ('admin','Admin')
)

class Filial(models.Model):
    name = models.CharField(max_length=50)
    manager = models.CharField(max_length=50,default="")
    created_at = models.DateTimeField(auto_now_add=True)

class User(AbstractUser):
    username = models.CharField(max_length=15,unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20,choices=roles,default="new")
    phone_number = models.CharField(max_length=20,null=True,blank=True)
    filial = models.ForeignKey(Filial,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
