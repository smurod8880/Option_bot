import numpy as np
import pandas as pd

class TechnicalIndicators:
    def calculate_all_indicators(self, data):
        if len(data) < 50:
            return {}
            
        return {
            'rsi': self._calculate_rsi(data),
            'macd_histogram': self._calculate_macd(data),
            'vwap_gradient': self._calculate_vwap_gradient(data),
            'volume_tsunami': self._calculate_volume_tsunami(data),
            'neural_macd': self._calculate_neural_macd(data),
            'quantum_rsi': self._calculate_quantum_rsi(data)
        }
        
    def _calculate_rsi(self, data, period=14):
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs)).iloc[-1]
        
    def _calculate_macd(self, data):
        ema12 = data['close'].ewm(span=12).mean()
        ema26 = data['close'].ewm(span=26).mean()
        macd_line = ema12 - ema26
        macd_signal = macd_line.ewm(span=9).mean()
        return (macd_line - macd_signal).iloc[-1]
        
    def _calculate_vwap_gradient(self, data):
        typical_price = (data['high'] + data['low'] + data['close']) / 3
        vwap = (typical_price * data['volume']).cumsum() / data['volume'].cumsum()
        gradient = vwap.diff().rolling(window=5).mean().iloc[-1]
        return gradient / data['close'].iloc[-1] * 100
        
    def _calculate_volume_tsunami(self, data):
        volume_sma = data['volume'].rolling(window=20).mean().iloc[-1]
        return data['volume'].iloc[-1] / volume_sma if volume_sma > 0 else 1.0
        
    def _calculate_neural_macd(self, data):
        macd = self._calculate_macd(data)
        volatility = data['close'].pct_change().rolling(window=14).std().iloc[-1]
        return macd + volatility * 0.5
        
    def _calculate_quantum_rsi(self, data):
        rsi = self._calculate_rsi(data)
        volume_factor = (data['volume'].iloc[-1] / data['volume'].rolling(window=20).mean().iloc[-1]) * 0.1
        return min(max(rsi + volume_factor, 0), 100)
