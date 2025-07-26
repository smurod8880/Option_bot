import numpy as np

class AIPredictor:
    def predict(self, features):
        # Упрощенная AI модель для Render
        weights = [0.3, 0.2, 0.15, 0.15, 0.2]  # Веса для признаков
        weighted_sum = sum(w * f for w, f in zip(weights, features))
        
        # Нормализация
        prediction = 1 / (1 + np.exp(-weighted_sum * 0.01))
        return min(max(prediction, 0.01), 0.99)
