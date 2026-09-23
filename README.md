# Book & Movie Review Social API

API REST construida con **FastAPI** que permite gestionar un catálogo de libros y películas, escribir reseñas, marcar favoritos y manejar usuarios con autenticación basada en JWT.

## Características

- **Catálogo de obras** — libros y películas con géneros, autor/director, fecha de lanzamiento y portada.
- **Sistema de usuarios** — registro, login (form-data y JSON), roles `admin` / `user`, JWT.
- **Reseñas** — puntuación de 1 a 5 estrellas y contenido texto.
- **Favoritos** — marcar y listar obras favoritas (con restricción de unicidad por usuario/obra).
- **Migraciones de base de datos** con **Alembic**.
- **Documentación automática** de la API con Swagger UI y ReDoc.

## Requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recomendado) o `pip`

## Instalación

```bash
# 1. Clona o accede al proyecto
cd "proyecto integrador"

# 2. Crea y activa el entorno virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# 3. Instala las dependencias
pip install -r requirements.txt
```

O usando `uv`:

```bash
uv venv
uv pip install -r requirements.txt
```

## Configuración

La aplicación lee las variables de entorno desde el archivo **`.env`** en la raíz del proyecto. El archivo ya existe con valores por defecto; revísalos en `app/core/config.py`.

| Variable                      | Descripción                        | Valor por defecto                              |
|-------------------------------|------------------------------------|-----------------------------------------------|
| `DATABASE_URL`                | URL de conexión a la base de datos | `sqlite:///./app.db`                          |
| `SECRET_KEY`                  | Clave secreta para firmar JWTs     | `change-this-secret-key-in-production`        |
| `ALGORITHM`                   | Algoritmo de firma de tokens       | `HS256`                                       |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Minutos de expiración del token    | `30`                                          |

> **Nota:** El primer usuario registrado automáticamente obtiene el rol de **admin**.

## Inicializar la base de datos

El proyecto usa SQLite por defecto y Alembic para las migraciones. Sigue estos pasos para inicializar:

```bash
# 1. Aplica las migraciones existentes (crea las tablas users, works, reviews, favorites)
alembic upgrade head

# 2. (Opcional) Si modificaste los modelos y quieres generar una nueva migración:
alembic revision --autogenerate -m "descripción del cambio"
alembic upgrade head
```

Si prefieres crear las tablas directamente sin Alembic (modo desarrollo):

```bash
# Ejecuta este script una sola vez:
python -c "from app.database.base import Base; from app.models import User, Work, Review, Favorite; from app.database.connection import engine; Base.metadata.create_all(bind=engine); print('Tablas creadas.')"
```

## Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`.

| Ruta                          | Descripción                                   |
|-------------------------------|-----------------------------------------------|
| `http://localhost:8000/docs`  | Documentación interactiva (Swagger UI)        |
| `http://localhost:8000/redoc` | Documentación alternativa (ReDoc)             |

## API — Endpoints

### Auth (`/api/auth`)

| Método | Endpoint       | Descripción                              |
|--------|----------------|------------------------------------------|
| POST   | `/login`       | Login con form-data → devuelve token JWT |
| POST   | `/login-json`  | Login con JSON → devuelve token JWT      |
| POST   | `/register`    | Registro de nuevo usuario                |

### Catálogo (`/api/catalog`)

| Método | Endpoint        | Autenticación   | Descripción                              |
|--------|-----------------|-----------------|------------------------------------------|
| GET    | `/`             | Pública         | Listar obras (paginado)                  |
| GET    | `/{work_id}`    | Pública         | Obtener una obra por ID                  |
| POST   | `/`             | Admin requerido | Crear una obra                           |
| PUT    | `/{work_id}`    | Admin requerido | Actualizar una obra                      |
| DELETE | `/{work_id}`    | Admin requerido | Eliminar una obra (elimina reseñas en cascada) |

### Reseñas (`/api/reviews`)

| Método | Endpoint         | Autenticación           | Descripción                              |
|--------|------------------|-------------------------|------------------------------------------|
| GET    | `/`              | Pública                 | Listar reseñas (filtra por `work_id`)    |
| GET    | `/{review_id}`   | Pública                 | Obtener una reseña por ID                |
| POST   | `/?work_id=…`    | Usuario autenticado     | Crear reseña                             |
| PUT    | `/{review_id}`   | Autor / Admin           | Editar reseña                            |
| DELETE | `/{review_id}`   | Autor / Admin           | Eliminar reseña                          |

### Favoritos (`/api/favorites`)

| Método | Endpoint           | Autenticación           | Descripción                              |
|--------|--------------------|-------------------------|------------------------------------------|
| GET    | `/`                | Usuario autenticado     | Listar favoritos del usuario             |
| POST   | `/{work_id}`       | Usuario autenticado     | Añadir obra a favoritos                  |
| DELETE | `/{work_id}`       | Usuario autenticado     | Remover obra de favoritos                |

## Uso rápido

```bash
# Registrar el primer usuario (será admin)
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","email":"admin@example.com","password":"Admin123!"}'

# Iniciar sesión
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login-json \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Admin123!"}' | jq -r .access_token)

# Crear una obra (requiere admin)
curl -X POST http://localhost:8000/api/catalog/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"1984","type":"book","genre":"distopico","author":"George Orwell","release_date":"1949-06-08"}'

# Listar obras (público)
curl http://localhost:8000/api/catalog/

# Añadir reseña (requiere auth)
curl -X POST "http://localhost:8000/api/reviews/?work_id=1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"rating":5,"content":"Una obra maestra."}'
```

## Estructura del proyecto

```
proyecto integrador/
├── alembic/                  # Migraciones de base de datos
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── app/
│   ├── core/                 # Configuración, enums, seguridad, dependencias
│   ├── crud/                 # Operaciones de base de datos (User, Work, Review, Favorite)
│   ├── database/             # Motor, sesión y base declarativa
│   ├── models/               # Modelos SQLAlchemy (User, Work, Review, Favorite)
│   ├── routers/              # Rutas de la API (auth, catalog, reviews, favorites)
│   ├── schemas/              # Esquemas Pydantic (entrada/salida)
│   └── main.py               # Punto de entrada de la aplicación
├── .env                      # Variables de entorno
├── .gitignore
├── alembic.ini
└── requirements.txt
```

## Tecnologías

| Tecnología         | Uso                                        |
|--------------------|--------------------------------------------|
| FastAPI            | Framework web principal                    |
| SQLAlchemy 2.0     | ORM y mapeo de base de datos               |
| Alembic            | Migraciones de base de datos               |
| Pydantic v2        | Validación y serialización de datos        |
| python-jose        | Generación y verificación de tokens JWT    |
| passlib + bcrypt   | Hash y verificación de contraseñas         |
| SQLite             | Base de datos (configurable vía `DATABASE_URL`) |
| Uvicorn            | Servidor ASGI                              |
