from django.shortcuts import render
# Import rest_framework libraries
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Import Meraki library
import meraki

# Datetime
from datetime import datetime
import pytz

# Q
from django.db.models import Q

# Import App's models
from .models import *

# Create your views here.

# Device catalogue view
@api_view(['GET'])
def device_catalogue(request):
    # Clave API
    API_KEY = "0"
    # Pasamos la clave al Dashboard de la API para la autenticación
    dashboard = meraki.DashboardAPI(API_KEY)

    # Este es el ID de la red en Meraki
    network_id = 'N_584342051651361715'

    # Obtenemos el catalogo de dispositivos totales (lo regresa como diccionario)
    response = dashboard.sm.getNetworkSmDevices(
        network_id,
        total_pages='all',
        direction='next'
    )

    # Recorremos el Dict
    for data in response:
        # Obtenemos el ID para hacer la validación si ya existe un registro o no
        validate_data = DeviceCatalogue.objects.values().filter(meraki_id=data['id'])
        # Si no existe, creamos un registro nuevo con los datos del Dict
        if len(validate_data) == 0:
            # Solo tomamos los campos que nos interesan del Dict porque la API nos regresa más info
            device_catalogue_id = DeviceCatalogue.objects.create(
                meraki_id=data['id'],
                vehicle=data['name'],
                wifi_mac=data['wifiMac'],
                os_name=data['osName'],
                system_model=data['systemModel'],
                uuid=data['uuid'],
                serial_number=data['serialNumber'],
            )
        # Si ya existe actualizamos el registro con la información que nos regresa el Dict
        else:
            device_catalogue_id = DeviceCatalogue.objects.filter(meraki_id=data['id']).update(
                vehicle=data['name'],
                wifi_mac=data['wifiMac'],
                os_name=data['osName'],
                system_model=data['systemModel'],
                uuid=data['uuid'],
                serial_number=data['serialNumber'],
            )
    # Retornamos el método Response de rest-framework para la validación del servicio
    return Response(template_name=None, headers=None, content_type=None, status=status.HTTP_202_ACCEPTED)

# Connectivity info device view
@api_view(['GET'])
def connectivity_info_device(request):
    # Clave API
    API_KEY = "407c11244ffb6289d3add7ffacc6945adefdfbb4"
    # Pasamos la clave al Dashboard de la API para la autenticación
    dashboard = meraki.DashboardAPI(API_KEY)

    # Este es el ID de la red en Meraki
    network_id = 'N_584342051651361715'

    # Obtenemos los datos, bateria, última conexión y posición
    response = dashboard.sm.getNetworkSmDevices(
        network_id,
        total_pages='all',
        fields=['batteryEstCharge', 'lastConnected', 'cellularDataUsed']
    )

    for data in response:
        # Sustituimos los None por null en el dict
        if data['cellularDataUsed'] == None:
            data.update(cellularDataUsed=0)
        # Cambiamos formato de campo lastConnected a datetime
        timestamp = data['lastConnected']
        new_date = datetime.fromtimestamp(timestamp)
        stamp_utc = new_date.astimezone(pytz.utc)
        data.update(lastConnected=stamp_utc)
        # Validamos si el ID existe dentro de nuestro catalogo de dispositivos
        validate_data = DeviceCatalogue.objects.values().filter(meraki_id=data['id'])
        if validate_data != 0:
            # Creamos el registro en la bd
            connectivity_info_device_id = ConectivityInfoDevice.objects.create(
                battery_level=data['batteryEstCharge'],
                last_connected=data['lastConnected'],
                data_used=data['cellularDataUsed'],
                location=data['location'],
                received_on= datetime.now(pytz.utc),
                vehicle=Vehicle.objects.values('id_vehicle').filter(
                    Q(name=data['name'])
                ),
                meraki=data['id']
            )
        else:
            pass
    # Retornamos el método Response de rest-framework para la validación del servicio
    return Response(template_name=None, headers=None, content_type=None, status=status.HTTP_202_ACCEPTED)