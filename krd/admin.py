from django.contrib import admin
from .models import Client, Loan, PhoneNumber, Product, PaymentMonth

admin.site.register([Client, Loan, PhoneNumber, Product, PaymentMonth])