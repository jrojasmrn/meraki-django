# Import rest_framework libraries
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Import Meraki library
import meraki

# Datetime
from datetime import datetime
import pytz

# Import App's models
from .models import *

# Create your views here.

# Device catalogue view
@api_view(['GET'])
def device_catalogue(request):
    # Clave API
    API_KEY = "407c11244ffb6289d3add7ffacc6945adefdfbb4"
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
        validate_data = DeviceCatalogue.objects.values().filter(Id_Meraki=data['id'])
        # Si no existe, creamos un registro nuevo con los datos del Dict
        if len(validate_data) == 0:
            # Solo tomamos los campos que nos interesan del Dict porque la API nos regresa más info
            device_catalogue_id = DeviceCatalogue.objects.create(
                Id_Meraki=data['id'],
                Name=data['name'],
                Wifi_Mac=data['wifiMac'],
                Os_Name=data['osName'],
                System_Model=data['systemModel'],
                Uuid=data['uuid'],
                Serial_Number=data['serialNumber'],
                Data_Plan=1048576 #Plan de datos de los operadores
            )
        # Si ya existe actualizamos el registro con la información que nos regresa el Dict
        else:
            device_catalogue_id = DeviceCatalogue.objects.filter(Id_Meraki=data['id']).update(
                Name=data['name'],
                Wifi_Mac=data['wifiMac'],
                Os_Name=data['osName'],
                System_Model=data['systemModel'],
                Uuid=data['uuid'],
                Serial_Number=data['serialNumber'],
                Data_Plan=1048576  # Plan de datos de los operadores
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

        # Obtenemos el ID de la unidad
        vehicle = Vehicle.objects.values('id_vehicle').filter(name=data['name'])
        for sub in vehicle:
            data['vehicle_id'] = int(sub.get('id_vehicle'))
            # Validamos si el ID existe dentro de nuestro catalogo de dispositivos
            validate_data = DeviceCatalogue.objects.values().filter(Id_Meraki=data['id'])
            if len(validate_data) != 0:
                # Creamos el registro en la bd
                connectivity_info_device_id = ConectivityInfoDevice.objects.create(
                    Vehicle_Id=data['vehicle_id'],
                    Meraki_Id=data['id'],
                    Battery_Level=data['batteryEstCharge'],
                    Last_Connected=data['lastConnected'],
                    Data_Used=data['cellularDataUsed'],
                    Location_Device=data['location'],
                    Received_On=datetime.now(pytz.utc)
                )
    # Retornamos el método Response de rest-framework para la validación del servicio
    return Response(template_name=None, headers=None, content_type=None, status=status.HTTP_202_ACCEPTED)