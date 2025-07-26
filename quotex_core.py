import asyncio
import logging
from datetime import datetime
from integration.quotex_client import QuotexData
from core.signal_analyzer import QuantumSignalAnalyzer
from core.risk_manager import AdvancedRiskManager
from integration.telegram_bot import TelegramBotHandler
from utils.database import Database
from utils.performance_monitor import PerformanceMonitor

logger = logging.getLogger(__name__)

class QuotexProBot:
    def __init__(self, config):
        self.config = config
        self.quotex = None
        self.analyzer = QuantumSignalAnalyzer()
        self.risk_manager = AdvancedRiskManager()
        self.telegram = TelegramBotHandler(config['BOT_TOKEN'], config['CHAT_ID'])
        self.database = Database()
        self.monitor = PerformanceMonitor()
        self.is_running = False
        self.start_time = None
        
    async def initialize(self):
        await self._connect_services()
        self.monitor.set_bot(self)
        asyncio.create_task(self.monitor.run())
        logger.info("🚀 Quantum Quotex Pro Bot Initialized")
        
    async def _connect_services(self):
        try:
            self.quotex = QuotexData(
                self.config['QUOTEX_EMAIL'],
                self.config['QUOTEX_PASSWORD']
            )
            await self.quotex.connect()
            await self.telegram.initialize()
            await self.database.initialize()
        except Exception as e:
            logger.error(f"Ошибка подключения: {e}")
            await self.telegram.send_error("Initialization", str(e))
            
    async def start_trading(self):
        if self.is_running:
            return
            
        self.is_running = True
        self.start_time = datetime.now()
        
        await self.telegram.send_message(
            "🟢 ТОРГОВЛЯ НАЧАТА\n\n"
            f"⏰ Время запуска: {self.start_time.strftime('%H:%M:%S')}\n"
            "Режим: Quantum Precision V2"
        )
        
        while self.is_running:
            try:
                for asset in self.config['QUOTEX_ASSETS']:
                    for expiry in self.config['QUOTEX_EXPIRIES']:
                        await self.process_asset(asset, expiry)
                
                await asyncio.sleep(10)
            except Exception as e:
                logger.error(f"Ошибка в основном цикле: {e}")
                await asyncio.sleep(30)
                
    async def process_asset(self, asset, expiry):
        try:
            candles = await self.quotex.get_ohlcv(asset, self._timeframe_map(expiry), 100)
            if not candles or len(candles) < 50:
                return
                
            signal = self.analyzer.analyze(asset, candles, expiry)
            
            if signal and self.risk_manager.validate_signal(signal):
                await self.telegram.send_signal(signal)
                await self.database.save_signal(signal)
                self.risk_manager.record_signal()
                self.monitor.record_signal()
        except Exception as e:
            logger.error(f"Ошибка обработки {asset}: {e}")
            
    def _timeframe_map(self, expiry):
        return {60: "1m", 300: "5m", 900: "15m", 3600: "1h"}.get(expiry, "1m")
        
    async def shutdown(self):
        self.is_running = False
        await self.telegram.send_message("🔴 ТОРГОВЛЯ ОСТАНОВЛЕНА")
        logger.info("Бот остановлен")
