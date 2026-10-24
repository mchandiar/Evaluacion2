import requests
import random
URL_BASE = "http://library.demo.local/api/v1"
URL_LIBROS = URL_BASE + "/books"

USUARIO = "cisco"
PASSWORD = "Cisco123!"

print("Obteniendo token de autenticación...")

respuesta_login = requests.post(
    URL_BASE + "/loginViaBasic",
    auth=(USUARIO, PASSWORD)
)

if respuesta_login.status_code != 200:
    print("Error al obtener el token.")
    print("Código HTTP:", respuesta_login.status_code)
    exit()

token = respuesta_login.json()["token"]

headers = {
    "X-API-KEY": token,
    "Content-Type": "application/json"
}

print("Autenticación exitosa.")
print()


nombres = [
    "Martin", "Carlos", "Andrea", "Felipe", "Camila",
    "Diego", "Valentina", "Sebastian", "Daniela", "Javier"
]

apellidos = [
    "Gonzalez", "Perez", "Soto", "Munoz", "Rojas",
    "Silva", "Torres", "Contreras", "Ramirez", "Castro"
]

temas = [
    "Redes", "Python", "Ciberseguridad", "Linux",
    "Cisco", "Programacion", "Cloud", "DevNet",
    "Automatizacion", "Telecomunicaciones"
]

niveles = [
    "Basico", "Intermedio", "Avanzado",
    "Profesional", "Practico"
]


print("GENERANDO 50 LIBROS ALEATORIOS")
print("--------------------------------")

creados = 0

for id_libro in range(8, 58):

    autor = (
        random.choice(nombres)
        + "_"
        + random.choice(apellidos)
    )

    titulo = (
        random.choice(temas)
        + " "
        + random.choice(niveles)
        + " "
        + str(random.randint(1, 999))
    )

    isbn = "".join(
        str(random.randint(0, 9))
        for _ in range(13)
    )

    libro = {
        "id": id_libro,
        "title": titulo,
        "author": autor,
        "isbn": isbn
    }

    respuesta = requests.post(
        URL_LIBROS,
        headers=headers,
        json=libro
    )

    if respuesta.status_code == 200:
        creados += 1
        print(
            "OK | ID:",
            id_libro,
            "|",
            titulo,
            "|",
            autor,
            "| ISBN:",
            isbn
        )
    else:
        print(
            "ERROR | ID:",
            id_libro,
            "| Código:",
            respuesta.status_code
        )


print()
print("--------------------------------")
print("Libros creados correctamente:", creados)
print("--------------------------------")


print()
print("LISTADO TOTAL DE LIBROS")
print("--------------------------------")

parametros = {
    "includeISBN": "true",
    "sortBy": "author"
}

respuesta = requests.get(
    URL_LIBROS,
    params=parametros
)

if respuesta.status_code == 200:

    libros = respuesta.json()

    for libro in libros:

        print()
        print("ID:", libro.get("id"))
        print("Título:", libro.get("title"))
        print("Autor:", libro.get("author"))
        print("ISBN:", libro.get("isbn"))

    print()
    print("--------------------------------")
    print("TOTAL DE LIBROS:", len(libros))
    print("--------------------------------")

else:
    print(
        "Error al consultar los libros:",
        respuesta.status_code
    )