import numpy as np
class CarTypePredictor:
    def __init__(self):
        self.car_types = ["SUV", "Sedan", "Truck", "Heavy Truck"]

    def predict(self, image):
        return np.random.choice(self.car_types)