from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# Import your Base
from app.core.database import Base
# Import all models so Alembic knows about them
from app.models.category import Category
from app.models.product import Product  # example if you have it
from app.models.user.user import User
from app.models.user.user_role import UserRole

# Alembic config
config = context.config
fileConfig(config.config_file_name)

# Tell Alembic about metadata
target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
