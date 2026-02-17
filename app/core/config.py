import os


class Settings:
    APP_NAME = "AeroFleet Manager"
    APP_VERSION = "1.0.0"
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/aerofleet")
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 1440
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")


settings = Settings()

# Render.com uses postgres:// — SQLAlchemy needs postgresql://
if settings.DATABASE_URL.startswith("postgres://"):
    settings.DATABASE_URL = settings.DATABASE_URL.replace("postgres://", "postgresql://", 1)
