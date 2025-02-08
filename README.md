# FastAPI Ghibli API

Este proyecto es una API REST desarrollada con FastAPI, PostgreSQL, Flyway, Docker, y pruebas con pytest. La API permite la creación, obtención, actualización y eliminación de usuarios, y también permite a los usuarios consumir datos de la API de Studio Ghibli según su rol.

## Requisitos

- Docker
- Docker Compose
Asegúrate de tener instalado lo siguiente en tu sistema:

-
## Instalación

- Docker

- Docker Compose

- Python 3.x11(opcional, solo si deseas trabajar fuera del contenedor)

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu-usuario/fastapi-ghibli.git
   cd fastapi-ghibli

 Si deseas trabajar fuera del contenedor, crea un entorno virtual para aislar las dependencias del proyecto:
  python3 -m venv venv

  - Linux/MacOS
    source venv/bin/activate

  - Windows
    source venv/bin/activate

    Instala las dependencias del proyecto:
        pip install -r requirements.txt


2. Levantar el proyecto con Docker
El proyecto utiliza Docker Compose para gestionar los servicios. Asegúrate de estar en la raíz del proyecto y ejecuta el siguiente comando para construir y levantar los contenedores:
- docker-compose up --build

Para detener los servicios

- docker-compose down
Esto levantará los siguientes servicios:

PostgreSQL: Base de datos en el puerto 5430.

Flyway: Aplicará las migraciones de la base de datos ubicadas en la carpeta ./migrations.

Aplicación Python: Servicio principal de la aplicación en el puerto 8000.

Si no lo agrega se puede crear la base con cualquier cliente Postgres
 agregando:
 ![alt text](image.png)
 password: password
3. Acceder a la aplicación
Una vez que los contenedores estén en funcionamiento, la aplicación estará disponible en:
    http://localhost:8000

se agregó la colecion de postman
- **Endpoint**:
   - `GET /users/`
   - `GET /users/id(int)`
   - `POST /users/`
   - `PUT /users/id(int)`
   - `DELETE /users/id(int)`

   ### Consumo de Studio Ghibli API

Los usuarios pueden consumir datos de la API de Studio Ghibli según su rol. Los roles disponibles son: `admin`, `films`, `people`, `locations`, `species`, `vehicles`.

- **Endpoint**: `GET /users/{user_id}/ghibli/{resource}`
- **Recursos permitidos por rol**:
  - `admin`: Puede acceder a todos los recursos (`films`, `people`, `locations`, `species`, `vehicles`).
  - `films`: Solo puede acceder a `films`.
  - `people`: Solo puede acceder a `people`.
  - `locations`: Solo puede acceder a `locations`.
  - `species`: Solo puede acceder a `species`.
  - `vehicles`: Solo puede acceder a `vehicles`.

**Ejemplo**:
```bash
curl "http://localhost:8000/users/1/ghibli/films"
