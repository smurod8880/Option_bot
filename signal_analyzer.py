import numpy as np
from utils.indicators import TechnicalIndicators

class AdvancedSignalAnalyzer:
    def __init__(self):
        self.indicators = TechnicalIndicators()
        
    def analyze(self, asset, candles, expiry):
        if len(candles) < 50:
            return None
            
        # Преобразование в DataFrame
        df = self._candles_to_df(candles)
        price = df['close'].iloc[-1]
        
        # Расчет индикаторов
        indicators = self.indicators.calculate_all_indicators(df)
        
        # Трехуровневая проверка
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
                "price": price,
                "confidence": min(confidence, 99.9),
                "indicators": indicators
            }
        return None

    def _candles_to_df(self, candles):
        # Преобразование свечей в DataFrame
        # ...
