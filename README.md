# Cumplo back challenge

Esta aplicación se creó con el lenguaje Python y el framework Django.

Las gráficas se hicieron la librería Chart.js

El despliegue de la aplicación se realizó en Pythonanywhere.

# App en producción

http://quattrococodrilo.pythonanywhere.com/

# App desarrollo

Para correr la aplicación de desarrollo de debe usar docker>=20

`docker-compose build`: genera los contenedores.

`docker-compose up`: levanta los servicios.

## Servicios

**web**: Se encarga de la aplicación de Django.

**mysql**: Se encarga de la base de datos.

## Estructura de archivos

```
django
├── back_challenge
│   ├── back_chanllenge
│   ├── core
│   ├── dollar
│   ├── manage.py
│   ├── templates
│   ├── udis
│   └── utils
├── compose
│   ├── Dockerfile
│   ├── entry_point.sh
│   ├── requirements.txt
│   └── wait-for-it.sh
└── requirements_local_env copy.txt
```

**back_challenge**: contiene el proyecto Django.

**core**: es el punto de entrada a la aplicación.

**dollar**: es la aplicación para la consulta de los datos relacionados al dollar.

**udis**: es la aplicación para la consulta de los datos relacionados al UDIS.

**utils**: contiene clases y funciones ajenas a Django.

**compose**: contiene la configuración para docker.

## Utils

### utils.BanxicoApi

Clase destinada a abstraer el proceso de consulta de la API de Banxico.

Los datos necesarios para las consultas se encuentran en el archivo settings.py, marcadas por el sufijo *BANXICO*.

#### Métodos

**create**: Método estático que devuelve una instancia de BanxicoApi

Argumentos:

- api_url (str): URL de la API.
- token (str): Token de autorización.

Retorno:

- object: BanxicoApi

**get**: Realiza la petición a BANXICO.

Argumentos:

- serie (str): Serie de tópico a consultar.

- start_date (str): Fecha inicial (YYYY-mm-dd)

- end_date (str, optional): Fecha final (YYYY-mm-dd). Default ''.

Retorno:

  - list: lista de datos [{fecha: str, dato: float}...]

#### Ejemplo

    api = BanxicoApi.create(
        api_url=URL_API_BANXICO,
        token=TOKEN
    )

    api.get(
        serie=SERIE,
        start_date='2020-01-01',
        end_date='2020-01-20',
    )

*Nota: las fechas deben estar en el formato YYYY-mm-dd

### utils.helpers.get_banxico_dat

Obtiene los datos de Banxico según la serie de que se indique.

Argumentos:

- start_date (str): Fecha de inicio
- end_date (str, optional): Fecha de término. Default ''.

Retorno:

- list: [{'fecha': string, 'dato': float}]

#### Ejemplo

    get_banxico_data(
        serie='544sdf5',
        start_date='2020-01-01',
        end_date='2020-01-20')

## Urls

`/`: punto de entrada, se encuentra manejado por la aplicación **core**.

`/udis`: punto de entrada para la aplicación udis.

`/dollar`: punto de entrada para la aliación dollar.

Los parámetros de consulta de pasan por GET.

## Tests

Los test deben correrse de la siguiente manera:

`docker-compose exec web python manage.py test --keepdb`
