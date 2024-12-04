import os
from dotenv import load_dotenv
load_dotenv()
from alembic import context
from sqlalchemy import engine_from_config, pool
from app.base import Base
from app.database import engine  # Import SQLAlchemy engine



# This line tells Alembic what metadata to use for the migration detection
target_metadata = Base.metadata

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:galena2612@localhost/healthmate")

config = context.config  # This will grab the Alembic configuration
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Connectable will hold the engine connection
connectable = engine_from_config(
    config.get_section(config.config_ini_section),
    prefix='sqlalchemy.',
    poolclass=pool.NullPool,
)

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_options={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
