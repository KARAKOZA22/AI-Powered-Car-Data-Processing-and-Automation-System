import numpy as np  # Library for numerical operations

class CarTypePredictor:
    """
    A class to predict the type of car based on an image.

    Attributes:
        car_types (list): A list of possible car types (e.g., "SUV", "Sedan", "Truck", "Heavy Truck").
    """

    def __init__(self):
        """
        Initializes the CarTypePredictor with a list of possible car types.
        """
        self.car_types = ["SUV", "Sedan", "Truck", "Heavy Truck"]  # List of supported car types

    def predict(self, image):
        """
        Predicts the type of car based on the provided image.

        Args:
            image (numpy.ndarray): The car image provided by the user.

        Returns:
            str: A randomly selected car type from the list of possible car types.
        """
        # Randomly select a car type from the list
        return np.random.choice(self.car_types)