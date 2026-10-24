# Evaluacion2 - Software de Geolocalización

Proyecto desarrollado para la Evaluación Parcial N°2 de CUY6142.

El programa utiliza la API de GraphHopper Directions para obtener una ruta entre dos ubicaciones.

## Funcionalidades

- Solicita una ubicación de inicio y un destino.
- Obtiene las coordenadas mediante la API de GraphHopper.
- Calcula la distancia y duración del viaje.
- Muestra las instrucciones paso a paso en español.
- Los valores de distancia se muestran con un máximo de dos decimales.
- Permite finalizar el programa ingresando "s" o "salir".

## Requisitos

- Python 3
- Librería requests
- API Key de GraphHopper

## Configuración

La API Key debe configurarse como una variable de entorno:

export GRAPHHOPPER_API_KEY="TU_API_KEY"

## Ejecución

Ejecutar:

python3 geolocalizacion.py
