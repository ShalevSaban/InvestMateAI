import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# מוסיף את תיקיית הבסיס ל-PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# טוען משתני סביבה מקובץ .env
from dotenv import load_dotenv
load_dotenv()

# מייבא את Flask app וה־SQLAlchemy db
from app import create_app, db
from app.models import *

# יוצר את האפליקציה (ב־Flask Factory pattern)
app = create_app()

# Alembic config object
config = context.config

# הגדרת לוגים אם יש קובץ
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# מגדיר את המטאדאטה של המודלים לצורך autogenerate
target_metadata = db.metadata


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
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# בוחר את מצב הריצה (online/offline)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
