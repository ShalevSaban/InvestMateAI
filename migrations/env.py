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

# מייבא את Base ואת כל המודלים
from app.database import Base
from app.models import agent, property, conversation

# Alembic config object
config = context.config

# מוודא ש-Alembic מקבל את DATABASE_URL מהסביבה
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL", "").replace("%", "%%"))

# הגדרת לוגים אם יש קובץ
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Alembic יסתכל על כל המודלים שלך כאן
target_metadata = Base.metadata


def run_migrations_offline() -> None:
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
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
