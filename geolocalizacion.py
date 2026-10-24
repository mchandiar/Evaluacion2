import requests
import urllib.parse

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
key = "668ab33f-eb1a-4afe-a84f-07bf2a00ff82"


def geocoding(location, key):
    while location == "":
        location = input("Ingrese la ubicación nuevamente: ")

    url = geocode_url + urllib.parse.urlencode({
        "q": location,
        "limit": "1",
        "key": key
    })

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country = ""

        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state = ""

        if len(state) != 0 and len(country) != 0:
            new_loc = name + ", " + state + ", " + country
        elif len(country) != 0:
            new_loc = name + ", " + country
        else:
            new_loc = name

        print(
            "URL de la API de geocodificación para "
            + new_loc
            + " (Tipo de ubicación: "
            + value
            + ")\n"
            + url
        )

    else:
        lat = "null"
        lng = "null"
        new_loc = location

        if json_status != 200:
            print("Error en la API de geocodificación. Estado: " + str(json_status))
        else:
            print("No se encontró la ubicación ingresada.")

    return json_status, lat, lng, new_loc


while True:

    loc1 = input("\nUbicación de inicio (s/salir para terminar): ")

    if loc1.lower() == "s" or loc1.lower() == "salir":
        print("Programa finalizado.")
        break

    orig = geocoding(loc1, key)

    loc2 = input("Destino (s/salir para terminar): ")

    if loc2.lower() == "s" or loc2.lower() == "salir":
        print("Programa finalizado.")
        break

    dest = geocoding(loc2, key)

    print("=================================================")

    if orig[0] == 200 and dest[0] == 200:

        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])

        # locale=es solicita las instrucciones de navegación en español
        paths_url = (
            route_url
            + urllib.parse.urlencode({
                "key": key,
                "locale": "es"
            })
            + op
            + dp
        )

        paths_response = requests.get(paths_url)
        paths_status = paths_response.status_code
        paths_data = paths_response.json()

        print(
            "Estado de la API de rutas: "
            + str(paths_status)
            + "\nURL de la API de rutas:\n"
            + paths_url
        )

        print("=================================================")
        print("Ruta desde " + orig[3] + " hasta " + dest[3])
        print("=================================================")

        if paths_status == 200:

            miles = paths_data["paths"][0]["distance"] / 1000 / 1.61
            km = paths_data["paths"][0]["distance"] / 1000

            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            minute = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)

            print(
                "Distancia recorrida: "
                "{0:.2f} millas / {1:.2f} km".format(miles, km)
            )

            print(
                "Duración del viaje: "
                "{0:02d}:{1:02d}:{2:02d}".format(hr, minute, sec)
            )

            print("=================================================")
            print("Instrucciones del viaje:")
            print("=================================================")

            for each in range(
                len(paths_data["paths"][0]["instructions"])
            ):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]

                print(
                    "{0} ( {1:.2f} km / {2:.2f} millas )".format(
                        path,
                        distance / 1000,
                        distance / 1000 / 1.61
                    )
                )

            print("=================================================")

        else:
            if "message" in paths_data:
                print("Error de la API de rutas: " + paths_data["message"])
            else:
                print("No fue posible calcular la ruta.")

            print("=================================================")