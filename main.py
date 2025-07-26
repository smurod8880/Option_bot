import asyncio
from core.quotex_core import QuotexProBot
from utils.config_loader import load_config

async def run_bot():
    config = load_config()
    bot = QuotexProBot(config)
    await bot.initialize()
    await bot.start_trading()

if __name__ == "__main__":
    asyncio.run(run_bot())
