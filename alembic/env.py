from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Alembic Config object
config = context.config

from app.core.config import settings

config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL.replace("+asyncpg", "")
)



#  config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Import all models to populate Base.metadata for Alembic
# Base metadata
from app.db.base import Base  
import app.db.base_imports

target_metadata = Base.metadata


def get_sync_database_url() -> str:
    """
    Convert async DB URL to sync URL for Alembic
    """
    url = config.get_main_option("sqlalchemy.url")
    if url and url.startswith("postgresql+asyncpg"):
        return url.replace("postgresql+asyncpg", "postgresql")
    if url is None:
        raise ValueError("The database URL must not be None.")
    return url


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_sync_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        {
            **(config.get_section(config.config_ini_section) or {}),
            "sqlalchemy.url": get_sync_database_url(),
        },
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
