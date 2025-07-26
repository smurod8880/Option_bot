import asyncio
import logging
from core.quotex_core import QuotexProBot
from utils.config_loader import load_config
from utils.keep_alive import start_keep_alive_server

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

async def run_bot():
    config = load_config()
    bot = QuotexProBot(config)
    await bot.initialize()
    
    # Запуск в фоновом режиме
    asyncio.create_task(bot.start_trading())
    logger.info("🚀 Бот запущен в фоновом режиме")

if __name__ == "__main__":
    # Запуск HTTP сервера для поддержания активности
    start_keep_alive_server()
    
    # Запуск бота
    asyncio.run(run_bot())
    
    # Бесконечный цикл для поддержания работы
    asyncio.get_event_loop().run_forever()
