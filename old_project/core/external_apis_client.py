import httpx
from cachetools import TTLCache
from httpx import HTTPStatusError

# Класс для асинхронного клиента GigaChat
class GigaChatAsyncClient:
    # Кеширование токенов для оптимизации аутентификации
    tokens_cache = TTLCache(maxsize=100, ttl=3600)  # Пример кеша на 100 токенов с TTL в 1 час

    def __init__(self, base_url: str, access_token: str):
        """
        Инициализация клиента с базовым URL и токеном доступа.
        """
        self.base_url = base_url
        # Использование кешированного токена, если он доступен
        self.access_token = self.tokens_cache.get("gigachat_token", access_token)
        self.client = httpx.AsyncClient(base_url=base_url)

    async def chat(self, request_data: dict) -> dict:
        """
        Отправка сообщения в чат и получение ответа.
        """
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = await self.client.post("/chat/", json=request_data, headers=headers)
            response.raise_for_status()
            return response.json()
        except HTTPStatusError as e:
            # Добавление логики обработки ошибок HTTP
            print(f"Ошибка HTTP при запросе к GigaChat: {e.response.status_code}")
            raise

    async def aclose(self):
        """
        Закрытие асинхронного клиента.
        """
        await self.client.aclose()

# Класс для асинхронного клиента TTS, интегрированного с Eleven Labs
class TTSClient:
    def __init__(self, base_url: str, access_token: str):
        """
        Инициализация клиента TTS.
        """
        self.base_url = base_url
        self.access_token = access_token
        self.client = httpx.AsyncClient(base_url=base_url)

    async def synthesize_speech(self, text: str, voice_id: str, speech_rate: float = 1.0, pitch: float = 1.0, **kwargs) -> bytes:
        """
        Синтез речи из текста с возможностью настройки параметров.
        """
        headers = {"Authorization": f"Bearer {self.access_token}"}
        payload = {
            "text": text,
            "voice_id": voice_id,
            "speech_rate": speech_rate,
            "pitch": pitch,
            **kwargs
        }
        response = await self.client.post("/synthesize/", json=payload, headers=headers)
        response.raise_for_status()
        return response.content

    async def aclose(self):
        """
        Закрытие асинхронного клиента.
        """
        await self.client.aclose()
