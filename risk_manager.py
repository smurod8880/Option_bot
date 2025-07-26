from datetime import datetime, timedelta

class RiskManager:
    def __init__(self):
        self.signal_counts = {'minute': 0, 'hour': 0, 'day': 0}
        self.last_signal_time = datetime.now()
        
    def validate_signal(self, signal):
        # Проверка лимитов
        current_time = datetime.now()
        
        # Сброс счетчиков
        if current_time.minute != self.last_signal_time.minute:
            self.signal_counts['minute'] = 0
            
        if current_time.hour != self.last_signal_time.hour:
            self.signal_counts['hour'] = 0
            
        if current_time.day != self.last_signal_time.day:
            self.signal_counts['day'] = 0
        
        # Проверка лимитов
        if (self.signal_counts['minute'] >= 2 or 
            self.signal_counts['hour'] >= 10 or 
            self.signal_counts['day'] >= 50):
            return False
            
        return True
        
    def record_signal(self):
        self.signal_counts['minute'] += 1
        self.signal_counts['hour'] += 1
        self.signal_counts['day'] += 1
        self.last_signal_time = datetime.now()
