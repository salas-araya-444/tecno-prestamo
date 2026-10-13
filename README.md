# TecnoPréstamo

API REST para gestionar equipos tecnológicos y sus préstamos.

- **Estudiante:** Esteban Salas Araya
- **Carné:** C5J444
- **Curso:** Desarrollo de Software 4
- **Universidad:** Universidad de Costa Rica, Sede del Pacífico

**Tecnologías:** Python, Django, Django REST Framework, MySQL y Postman.

---

## 1. Base de datos

En MySQL Workbench, abra y ejecute el archivo `database/tecnoprestamo_db.sql`.
Este script crea la base `tecnoprestamo_db` y el usuario `tecnoprestamo_user`.

## 2. Instalación

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Archivo .env

Copie `.env.example` con el nombre `.env` y complete la contraseña del usuario de MySQL:

```
DB_NAME=tecnoprestamo_db
DB_USER=tecnoprestamo_user
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
```

## 4. Migraciones

```
python manage.py migrate
```

## 5. Usuarios y grupo

Crear el administrador:

```
python manage.py createsuperuser
```

Luego ejecute el servidor, entre a `http://127.0.0.1:8000/admin/` con el administrador y haga lo siguiente:

1. Cree el grupo **Prestamistas** con los permisos `Can add prestamo` y `Can change prestamo`.
2. Cree un usuario normal llamado `prestamista` y agréguelo al grupo **Prestamistas**.

## 6. Ejecución

```
python manage.py runserver
```

## 7. Endpoints

| Método | Ruta | Acceso |
|---|---|---|
| GET | `/api/equipos/` (`?categoria=`, `?ordering=nombre`, `?page=`) | Público |
| POST | `/api/equipos/` | Token + add_equipo |
| GET | `/api/equipos/<id>/` | Público |
| PUT / PATCH | `/api/equipos/<id>/` | Token + change_equipo |
| DELETE | `/api/equipos/<id>/` | Token + delete_equipo |
| GET | `/api/prestamos/` (`?estado=`, `?equipo=`, `?page=`) | Token |
| POST | `/api/prestamos/` | Token + grupo Prestamistas + add_prestamo |
| GET | `/api/prestamos/<id>/` | Token |
| PUT / PATCH | `/api/prestamos/<id>/` | Token + change_prestamo |
| DELETE | `/api/prestamos/<id>/` | Token + administrador |
| POST | `/api/token/` | Usuario y contraseña |
| GET / POST | `/api/sesion/preferencia/` | Sesión (cookie + CSRF) |

Para las rutas con token se envía el header `Authorization: Token <valor>`.

## 8. Pruebas en Postman

1. Importe `postman/TecnoPrestamo.postman_collection.json`.
2. En las dos peticiones auxiliares de **TOKEN**, escriba la contraseña de cada usuario y envíelas.
3. Copie cada token en el header `Authorization` de las peticiones, en lugar de `TOKEN_ADMIN_AQUI` o `TOKEN_PRESTAMISTA_AQUI`.
4. Ejecute las peticiones en orden, de la 01 a la 27, sobre una base de datos recién migrada para que los ids coincidan.

Para probar la sesión:

1. Ejecute la petición **25**.
2. Copie el valor de `csrftoken` que aparece en la respuesta.
3. En la petición **26**, péguelo en el header `X-CSRFToken`, en lugar de `TU_CSRF_AQUI`.
4. Ejecute la petición **27**: la preferencia se mantiene porque Postman envía la cookie `sessionid` automáticamente.

## 9. Pruebas automatizadas

```
python manage.py test
```
