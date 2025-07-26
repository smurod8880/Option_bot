import sqlite3
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.conn = None
        
    async def initialize(self):
        try:
            self.conn = sqlite3.connect('trading_signals.db')
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS signals (
                    id INTEGER PRIMARY KEY,
                    asset TEXT,
                    action TEXT,
                    expiry INTEGER,
                    price REAL,
                    confidence REAL,
                    timestamp DATETIME
                )
            ''')
            self.conn.commit()
            logger.info("📊 База данных инициализирована")
        except Exception as e:
            logger.error(f"Ошибка БД: {e}")
            
    async def save_signal(self, signal):
        if not self.conn:
            return
            
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO signals (asset, action, expiry, price, confidence, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                signal['asset'],
                signal['action'],
                signal['expiry'],
                signal['price'],
                signal['confidence'],
                signal['timestamp']
            ))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Ошибка сохранения сигнала: {e}")
