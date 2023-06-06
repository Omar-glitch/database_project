# Pasos para ejecutar

1. Crearse un archivo .env en la raíz del directorio con las siguientes variables de entorno

```
PORT = 8000
HOST = 0.0.0.0
DEBUG = True
POSTGRES_USER = postgres
POSTGRES_PASSWORD = C0ntrol1*
POSTGRES_HOST = database
POSTGRES_PORT = 5432
POSTGRES_DATABASE = postgres
POSTGRES_SCHEMA = pharmaguide
```

2. Ejecutar el siguiente comando en la ruta raíz:

```
docker compose up
```
