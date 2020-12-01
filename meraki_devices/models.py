from django.db import models
from datetime import datetime

# Create your models here.

# Device Catalogue Model
class DeviceCatalogue(models.Model):
    Id_Meraki = models.CharField(max_length=254)
    Name = models.CharField(max_length=254)
    Wifi_Mac = models.CharField(max_length=254)
    Os_Name = models.CharField(max_length=254)
    System_Model = models.CharField(max_length=254)
    Uuid = models.CharField(max_length=254)
    Serial_Number = models.CharField(max_length=254)
    Data_Plan = models.IntegerField()


# Modelo de prueba para la relacion de la unidad
class Vehicle(models.Model):
    id_vehicle = models.IntegerField()
    name = models.CharField(max_length=254)

# Connectivity info model
class ConectivityInfoDevice(models.Model):
    Vehicle_Id = models.IntegerField()
    Meraki_Id = models.CharField(max_length=254)
    Battery_Level = models.IntegerField()
    Last_Connected = models.DateTimeField()
    Data_Used = models.IntegerField()
    Location_Device = models.CharField(max_length=254)
    Received_On = models.DateTimeField(default=datetime.now)
