from django.contrib import admin
from .models import User, Company, Filial

admin.site.register([User, Company, Filial])