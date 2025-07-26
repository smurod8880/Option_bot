import os
from dotenv import load_dotenv

load_dotenv()

def load_config():
    return {
        'QUOTEX_EMAIL': os.getenv('QUOTEX_EMAIL', 'your_email@example.com'),
        'QUOTEX_PASSWORD': os.getenv('QUOTEX_PASSWORD', 'your_password'),
        'BOT_TOKEN': os.getenv('BOT_TOKEN', 'your_telegram_bot_token'),
        'CHAT_ID': os.getenv('CHAT_ID', 'your_chat_id'),
        'QUOTEX_ASSETS': os.getenv('TRADING_PAIRS', 'EURUSD,GBPUSD,USDJPY').split(','),
        'QUOTEX_EXPIRIES': [int(x) for x in os.getenv('TRADING_EXPIRIES', '60,300').split(',')]
    }
