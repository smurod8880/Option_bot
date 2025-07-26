import asyncio
from datetime import datetime
from integration.quotex_client import QuotexData
from core.signal_analyzer import AdvancedSignalAnalyzer
from core.risk_manager import RiskManager
from integration.telegram_bot import TelegramBotHandler
from utils.database import Database

class QuotexProBot:
    def __init__(self, config):
        self.config = config
        self.quotex = QuotexData(config['QUOTEX_EMAIL'], config['QUOTEX_PASSWORD'])
        self.analyzer = AdvancedSignalAnalyzer()
        self.risk_manager = RiskManager()
        self.telegram = TelegramBotHandler(config['BOT_TOKEN'], config['CHAT_ID'])
        self.database = Database()

    async def initialize(self):
        await self.quotex.connect()
        await self.telegram.initialize()
        await self.database.initialize()
        print("🚀 Quantum Quotex Pro Bot Initialized")

    async def start_trading(self):
        while True:
            for asset in self.config['QUOTEX_ASSETS']:
                for expiry in self.config['QUOTEX_EXPIRIES']:
                    await self.process_asset(asset, expiry)
            
            await asyncio.sleep(10)

    async def process_asset(self, asset, expiry):
        candles = await self.quotex.get_ohlcv(asset, self._timeframe_map(expiry), 100)
        if not candles or len(candles) < 50:
            return
            
        signal = self.analyzer.analyze(asset, candles, expiry)
        
        if signal and self.risk_manager.validate_signal(signal):
            await self.telegram.send_signal(signal)
            await self.database.save_signal(signal)
            self.risk_manager.record_signal()

    def _timeframe_map(self, expiry):
        return {60: "1m", 300: "5m", 900: "15m", 3600: "1h"}.get(expiry, "1m")
