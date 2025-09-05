from logging.config import fileConfig
import importlib
import pkgutil
import pathlib
import sys

from sqlalchemy import engine_from_config, pool
from alembic import context

# Import your core stuff
from core.config import settings
from core.database import Base

# -------------------------------------------------------------------
# Alembic Config object
# -------------------------------------------------------------------
config = context.config

# Logging config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -------------------------------------------------------------------
# Model discovery
# -------------------------------------------------------------------
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Dynamically import all models inside modules/*
for _, module_name, _ in pkgutil.iter_modules([str(BASE_DIR / "modules")]):
    try:
        importlib.import_module(f"modules.{module_name}.models")
    except ModuleNotFoundError:
        pass

# Now Alembic knows about all metadata
target_metadata = Base.metadata

# -------------------------------------------------------------------
# Database URL from our config
# -------------------------------------------------------------------
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
