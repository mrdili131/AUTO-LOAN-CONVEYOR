from django.contrib import admin
from .models import Client, Loan, PhoneNumber, Product

admin.site.register([Client, Loan, PhoneNumber, Product])