from django.urls import path
from . import views

app_name = "accounting"

urlpatterns = [
    path('',views.IndexView.as_view(),name='home'),
    path('history/',views.HistoryView.as_view(),name='history'),
    path('done/',views.done,name='done')
]