# core/signal_analyzer.py
import numpy as np
import pandas as pd
from datetime import datetime
from .indicators import TechnicalIndicators
from .ai_model import AIPredictor

class QuantumSignalAnalyzer:
    def __init__(self):
        self.indicators = TechnicalIndicators()
        self.ai = AIPredictor()

    def analyze(self, asset, candles, expiry):
        if len(candles) < 50:
            return None

        df = self._candles_to_df(candles)
        if df.isnull().values.any():
            return None

        price = df['close'].iloc[-1]
        indicators = self.indicators.calculate_all_indicators(df)
        if not indicators:
            return None

        level1 = self._level1_momentum_impulse(df, indicators)
        level2 = self._level2_indicator_convergence(indicators)
        level3 = self._level3_ai_prediction(df, indicators)

        if level1['valid'] and level2['valid'] and level3['valid']:
            direction = "CALL" if level3['direction'] == "UP" else "PUT"
            confidence = (level1['score'] + level2['score'] + level3['score']) / 3 * 100
            return {
                "asset": asset,
                "action": direction,
                "expiry": expiry,
                "price": round(price, 5),
                "confidence": round(min(confidence, 99.9), 1),
                "indicators": indicators,
                "timestamp": datetime.utcnow().isoformat()
            }
        return None

    def _candles_to_df(self, candles):
        df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        return df.astype(float)

    def _level1_momentum_impulse(self, df, indicators):
        volume_ok = indicators.get('volume_tsunami', 0) > 2.0
        price_change = abs(df['close'].pct_change().iloc[-1]) > 0.002
        return {'valid': volume_ok and price_change, 'score': 0.8}

    def _level2_indicator_convergence(self, indicators):
        macd_ok = indicators.get('macd_histogram', 0) > 0
        vwap_ok = abs(indicators.get('vwap_gradient', 0)) > 0.002
        rsi_ok = 30 < indicators.get('quantum_rsi', 50) < 70
        return {'valid': macd_ok and vwap_ok and rsi_ok, 'score': 0.85}

    def _level3_ai_prediction(self, df, indicators):
        features = [
            df['close'].iloc[-1],
            indicators.get('rsi', 50),
            indicators.get('vwap_gradient', 0),
            indicators.get('volume_tsunami', 1),
            indicators.get('macd_histogram', 0)
        ]
        features = [float(f) if not np.isnan(f) else 0.0 for f in features]
        prediction = self.ai.predict(features)
        return {
            'valid': prediction > 0.85,
            'score': prediction,
            'direction': "UP" if prediction > 0.5 else "DOWN"
        }
