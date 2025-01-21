from PIL import Image  # Library for image processing
from car_classifier import CarTypePredictor  # Module for predicting car types

class CarDataProcessor:
    """
    A class to process car data, including saving the car image and predicting the car type.

    Attributes:
        car_description (str): The description of the car provided by the user.
        car_image (numpy.ndarray): The car image provided by the user.
        sender_email (str): The email address of the sender.
        sender_pass (str): The password for the sender's email account.
        reciever_email (str): The email address of the receiver.
        image_path (str): The file path where the car image is saved.
        predictor (CarTypePredictor): An instance of the CarTypePredictor class for predicting car types.
    """

    def __init__(self):
        """
        Initializes the CarDataProcessor with default values.
        """
        self.car_description = ""  # Placeholder for car description
        self.car_image = None  # Placeholder for car image
        self.sender_email = ""  # Placeholder for sender's email
        self.sender_pass = ""  # Placeholder for sender's email password
        self.reciever_email = ""  # Placeholder for receiver's email
        self.image_path = "/content/saved_image.jpg"  # Default path to save the car image
        self.predictor = CarTypePredictor()  # Initialize the car type predictor

    def process_inputs(self, car_description, sender_email, sender_pass, reciever_email, car_image):
        """
        Processes the inputs provided by the user, including saving the car image and predicting the car type.

        Args:
            car_description (str): The description of the car provided by the user.
            sender_email (str): The email address of the sender.
            sender_pass (str): The password for the sender's email account.
            reciever_email (str): The email address of the receiver.
            car_image (numpy.ndarray): The car image provided by the user.

        Returns:
            str: The predicted car type (e.g., "SUV", "Sedan", "Truck", "Heavy Truck").
        """
        # Save the inputs to the class attributes
        self.car_description = car_description
        self.car_image = car_image
        self.sender_email = sender_email
        self.sender_pass = sender_pass
        self.reciever_email = reciever_email

        # Convert the numpy array image to a PIL image and save it to the specified path
        self.tmp_img = Image.fromarray(car_image)
        self.tmp_img.save(self.image_path)

        # Predict the car type using the CarTypePredictor
        return self.predictor.predict(car_image)