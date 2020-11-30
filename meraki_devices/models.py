from django.db import models

# Create your models here.

# Device Catalogue Model
class DeviceCatalogue(models.Model):
    meraki_id = models.CharField(max_length=254)
    vehicle = models.CharField(max_length=254)
    wifi_mac = models.CharField(max_length=254)
    os_name = models.CharField(max_length=254)
    system_model = models.CharField(max_length=254)
    uuid = models.CharField(max_length=254)
    serial_number = models.CharField(max_length=254)

    # Cambiar nombre de modelo para mostrar
    class Meta:
        verbose_name = "Device Catalogue"
        verbose_name_plural = "Device Catalogues"

    # Cambio de nombre de proyectos para mostrar
    def __str__(self):
        return self.vehicle


# Modelo de prueba para la relacion de la unidad
class Vehicle(models.Model):
    id_vehicle = models.IntegerField()
    name = models.CharField(max_length=254)

# Connectivity info model
class ConectivityInfoDevice(models.Model):
    id_vehicle = models.CharField(max_length=254)
    meraki = models.CharField(max_length=254)
    battery_level = models.IntegerField()
    last_connected = models.DateTimeField()
    data_used = models.IntegerField()
    location = models.CharField(max_length=254)
    received_on = models.DateTimeField()