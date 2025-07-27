import aiohttp
import logging

logger = logging.getLogger(__name__)

class TelegramBotHandler:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.session = None

    async def initialize(self):
        self.session = aiohttp.ClientSession()
        url = f"https://api.telegram.org/bot{self.token}/getMe"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    logger.info("✅ Telegram подключен")
                else:
                    logger.error("❌ Ошибка подключения к Telegram")
        except Exception as e:
            logger.error(f"Ошибка Telegram: {e}")

    async def send_message(self, text):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        try:
            async with self.session.post(url, json={
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': 'Markdown'
            }) as resp:
                if resp.status != 200:
                    logger.error("Ошибка отправки сообщения в Telegram")
        except Exception as e:
            logger.error(f"Ошибка Telegram: {e}")

    async def send_signal(self, signal):
        emoji = "🟢" if signal['action'] == "CALL" else "🔴"
        indicators = signal['indicators']
        msg = (
            f"{emoji} **QUANTUM QUOTEX SIGNAL** {emoji}\n\n"
            f"• Ассет: `{signal['asset']}`\n"
            f"• Действие: `{signal['action']}`\n"
            f"• Экспирация: `{signal['expiry']}s`\n"
            f"• Цена: `{signal['price']:.5f}`\n"
            f"• Точность: `{signal['confidence']:.1f}%`\n\n"
            f"📊 **Технические показатели:**\n"
            f"- VWAP Gradient: `{indicators.get('vwap_gradient', 0):.4f}`\n"
            f"- Volume Tsunami: `{indicators.get('volume_tsunami', 0):.1f}x`\n"
            f"- Neural MACD: `{indicators.get('neural_macd', 0):.3f}`\n"
            f"- Quantum RSI: `{indicators.get('quantum_rsi', 0):.1f}`\n\n"
            f"_Сгенерировано Quantum Quotex Pro Bot_"
        )
        await self.send_message(msg)

    async def send_error(self, module, error):
        await self.send_message(f"❌ **Ошибка в {module}**\n`{error}`")
