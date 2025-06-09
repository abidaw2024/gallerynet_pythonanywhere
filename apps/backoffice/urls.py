from django.urls import path
from . import views

app_name = 'backoffice'

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard')
] 

