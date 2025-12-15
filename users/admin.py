from django.contrib import admin
from .models import User, Filial

admin.site.register([User, Filial])