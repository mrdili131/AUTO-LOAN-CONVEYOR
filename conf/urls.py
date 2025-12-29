from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('root/', admin.site.urls),
    path('',include('krd.urls')),
    path('accounting/',include('accounting.urls')),
    path('auth/',include('users.urls'))
]
