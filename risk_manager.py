from datetime import datetime, timedelta

class AdvancedRiskManager:
    def __init__(self):
        self.signal_counts = {'minute': 0, 'hour': 0, 'day': 0}
        self.last_signal_time = datetime.now()
        
    def validate_signal(self, signal):
        current_time = datetime.now()
        
        # Сброс счетчиков при смене периода
        if current_time.minute != self.last_signal_time.minute:
            self.signal_counts['minute'] = 0
        if current_time.hour != self.last_signal_time.hour:
            self.signal_counts['hour'] = 0
        if current_time.day != self.last_signal_time.day:
            self.signal_counts['day'] = 0
        
        # Проверка лимитов (5/час, 35/день)
        if (self.signal_counts['minute'] >= 2 or 
            self.signal_counts['hour'] >= 5 or 
            self.signal_counts['day'] >= 35):
            return False
            
        # Минимальная точность 75%
        if signal['confidence'] < 75.0:
            return False
            
        # Минимальный интервал 60 секунд
        if (current_time - self.last_signal_time).total_seconds() < 60:
            return False
            
        return True
        
    def record_signal(self):
        self.signal_counts['minute'] += 1
        self.signal_counts['hour'] += 1
        self.signal_counts['day'] += 1
        self.last_signal_time = datetime.now()
