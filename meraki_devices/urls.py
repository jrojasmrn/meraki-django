from django.urls import path
#Import views
from . import views

urlpatterns = [
    path('device_catalogue', views.device_catalogue, name='device_catalogue'),
    path('connectivity_info_device', views.connectivity_info_device, name='connectivity_info_device')
]