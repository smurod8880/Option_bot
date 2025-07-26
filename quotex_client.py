import asyncio
import logging
from quotexpy import Quotex

logger = logging.getLogger(__name__)

class QuotexData:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.client = None
        
    async def connect(self):
        self.client = Quotex(email=self.email, password=self.password)
        await self.client.connect()
        logger.info("✅ Quotex подключен")
        
    async def get_ohlcv(self, asset, timeframe, count):
        try:
            candles = await self.client.get_candles(asset, timeframe, count)
            return candles if len(candles) >= count else None
        except Exception as e:
            logger.error(f"Ошибка получения данных: {e}")
            return None
