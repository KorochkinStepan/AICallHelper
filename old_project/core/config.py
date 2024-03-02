from typing import Optional

from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv


class Settings(BaseSettings):
    # Настройки базы данных
    DB_USER: str = os.getenv("DB_USER", "empty_env")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "empty_env")
    DB_HOST: str = os.getenv("DB_HOST", "empty_env")
    DB_NAME: str = os.getenv("DB_NAME", "empty_env")
    DB_PORT: str = os.getenv("DB_PORT", "empty_env")

    # Настройки для подключения к внешним API
    GIGACHAT_BASE_URL: str = "https://api.gigachat.example.com"
    GIGACHAT_ACCESS_TOKEN: str = os.getenv("GIGACHAT_ACCESS_TOKEN", "KOD HERE")
    ELEVENLABS_BASE_URL: str = "https://api.elevenlabs.io"
    ELEVENLABS_ACCESS_TOKEN: str = os.getenv("ELEVENLABS_ACCESS_TOKEN", "KOD HERE")

    # Логирование
    LOGGING_LEVEL: str = os.getenv("LOGGING_LEVEL", "INFO")

    # Дополнительные настройки
    MAX_CONNECTIONS_COUNT: int = 10
    MIN_CONNECTIONS_COUNT: int = 10

    # Настройки безопасности
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change_this_to_a_secret_key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Настройки асинхронного клиента
    HTTPX_TIMEOUT: int = 10

    class Config:
        env_file = ".env"


# Различные конфигурации для сред выполнения
class DevelopmentSettings(Settings):
    LOGGING_LEVEL: str = "DEBUG"


class ProductionSettings(Settings):
    LOGGING_LEVEL: str = "ERROR"


class TestingSettings(Settings):
    LOGGING_LEVEL: str = "DEBUG"


def get_settings(environment: Optional[str] = None) -> Settings:
    """
    Функция для получения конфигураций в зависимости от среды выполнения.
    """
    if environment == "production":
        return ProductionSettings()
    elif environment == "testing":
        return TestingSettings()
    return DevelopmentSettings()


# Определение текущих настроек на основе переменной окружения APP_ENV

load_dotenv()

settings = get_settings(environment=os.getenv("APP_ENV", "production"))


