import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    TELEGRAM_BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME", "InvestMateAI_bot")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    MAX_CACHED_CRITERIA = int(os.getenv("MAX_CACHED_CRITERIA", "100"))
    CRITERIA_TTL_DAYS = int(os.getenv("CRITERIA_TTL_DAYS", "7"))

