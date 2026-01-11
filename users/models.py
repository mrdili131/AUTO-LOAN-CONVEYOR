from django.db import models
from django.contrib.auth.models import AbstractUser

roles = (
    ('new','Yangi'),
    ('creditor','Kreditor'),
    ('accountant','Buxgalter'),
    ('admin','Admin')
)

class Company(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Filial(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=50)
    manager = models.CharField(max_length=50,default="")
    accountant = models.CharField(max_length=50,default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    username = models.CharField(max_length=15,unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100,default="")
    role = models.CharField(max_length=20,choices=roles,default="new")
    phone_number = models.CharField(max_length=20,null=True,blank=True)
    filial = models.ForeignKey(Filial,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self,*args,**kwargs):
        if(self.first_name,self.last_name,self.middle_name):
            self.full_name = f"{self.last_name} {self.first_name} {self.middle_name}"
        super().save(*args,**kwargs)
