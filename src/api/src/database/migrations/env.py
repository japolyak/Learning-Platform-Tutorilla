from alembic import context
import logging
import os
import sys
from sqlalchemy import engine_from_config, pool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..')))

from src.core.config import connection_string, schema_name
from src.api.src.database.models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

config.set_main_option("sqlalchemy.url", connection_string)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
log = logging.getLogger(__name__)

target_metadata = Base.metadata


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool
    )

    log.info("Migrating...")
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            version_table_schema=schema_name
        )

        with context.begin_transaction():
            context.run_migrations()

    log.info("Migrations applied.")


if context.is_offline_mode():
    log.info("Can't run migrations offline")
else:
    log.info("Run migrations online")
    run_migrations_online()
