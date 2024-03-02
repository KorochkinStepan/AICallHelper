from fastapi import HTTPException
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
import logging
from datetime import datetime, timedelta
from typing import Any, Dict
import re

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Основные константы
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# Функция логирования ошибок
def log_error(error: Exception):
    """Логирует детали исключения."""
    logger.error(f"Error: {str(error)}")

# Обработчик исключений для FastAPI
def http_exception_handler(request, exc: HTTPException):
    """Обработчик HTTP исключений для FastAPI."""
    log_error(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Валидация email
def is_valid_email(email: str) -> bool:
    """Проверяет, является ли строка валидным email адресом."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

# Декодирование JWT токена
def decode_jwt(token: str) -> Dict[str, Any]:
    """Декодирует JWT токен, возвращая его payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        log_error(e)
        raise HTTPException(status_code=403, detail="Token is invalid or expired")

# Функции для работы с датами
def format_datetime(value: datetime) -> str:
    """Форматирует объект datetime в строку."""
    return value.strftime("%Y-%m-%d %H:%M:%S")

def days_between(d1: datetime, d2: datetime) -> int:
    """Возвращает количество дней между двумя датами."""
    return abs((d2 - d1).days)

# Санитизация входных данных
def sanitize_html(data: str) -> str:
    """Удаляет потенциально опасные HTML теги из строки."""
    tag_re = re.compile(r'<[^>]+>')
    return tag_re.sub('', data)

# Добавьте дополнительные утилиты и функции по мере необходимости
