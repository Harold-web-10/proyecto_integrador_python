"""
Alembic env.py

Configura la conexión a la base de datos usando la configuración del proyecto
(app.core.config.settings) y registra todos los modelos SQLAlchemy definidos
en app/models para que Alembic pueda autogenerar migraciones.
"""

from __future__ import annotations

import os
import sys
from logging.config import fileConfig

# Añadir el directorio raíz al sys.path para que 'app' sea importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import pool, create_engine  # noqa: E402

from alembic import context  # noqa: E402

# Importar configuración del proyecto
from app.core.config import settings  # noqa: E402
from app.database.base import Base  # noqa: E402
from app.models import User, Work, Review  # noqa: E402,F401  — registrar modelos

# Configuración de Alembic
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Establecer la URL de la BD desde settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Metadata de los modelos
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Ejecutar migraciones en modo offline (sin conexión activa)."""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecutar migraciones en modo online (con conexión activa)."""
    connectable = create_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
