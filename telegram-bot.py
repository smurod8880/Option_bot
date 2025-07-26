import requests, os

class TelegramBotHandler:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    async def initialize(self):
        pass

    async def send_signal(self, signal):
        emoji = "🟢" if signal['action'] == "CALL" else "🔴"
        
        # Детализированное сообщение
        msg = (f"{emoji} **QUANTUM QUOTEX SIGNAL** {emoji}\n\n"
               f"• Ассет: `{signal['asset']}`\n"
               f"• Действие: `{signal['action']}`\n"
               f"• Экспирация: `{signal['expiry']}s`\n"
               f"• Цена: `{signal['price']:.6f}`\n"
               f"• Точность: `{signal['confidence']:.1f}%`\n\n"
               f"📊 **Технические показатели:**\n"
               f"- RSI: `{signal['indicators'].get('rsi', 0):.2f}`\n"
               f"- MACD: `{signal['indicators'].get('macd_histogram', 0):.4f}`\n"
               f"- Объем: `{signal['indicators'].get('volume_ratio', 0):.2f}x`\n\n"
               f"_Сгенерировано Quantum Quotex Pro Bot_")
        
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        requests.post(url, json={'chat_id': self.chat_id, 'text': msg, 'parse_mode': 'Markdown'})
