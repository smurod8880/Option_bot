import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    def __init__(self):
        self.bot = None
        self.signals_count = 0
        self.start_time = datetime.now()
        
    def set_bot(self, bot):
        self.bot = bot
        
    def record_signal(self):
        self.signals_count += 1
        
    async def run(self):
        while True:
            await asyncio.sleep(1800)  # 30 минут
            
            if not self.bot or not self.bot.is_running:
                continue
                
            uptime = datetime.now() - self.start_time
            stats = (
                f"📊 **ПРОИЗВОДИТЕЛЬНОСТЬ**\n\n"
                f"⏱ Аптайм: {str(uptime).split('.')[0]}\n"
                f"📈 Сигналов: {self.signals_count}\n"
                f"🔄 Циклов: {self.bot.risk_manager.signal_counts['hour']}/час"
            )
            
            try:
                await self.bot.telegram.send_message(stats)
                logger.info("Отчет производительности отправлен")
            except Exception as e:
                logger.error(f"Ошибка отправки отчета: {e}")
