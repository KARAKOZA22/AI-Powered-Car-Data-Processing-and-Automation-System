from PIL import Image
from car_classifier import CarTypePredictor

class CarDataProcessor:
    def __init__(self):
        self.car_description = ""
        self.car_image = None
        self.sender_email = ""
        self.sender_pass = ""
        self.reciever_email = ""
        self.image_path = "/content/saved_image.jpg"
        self.predictor = CarTypePredictor()

    def process_inputs(self, car_description, sender_email, sender_pass, reciever_email, car_image):
        self.car_description = car_description
        self.car_image = car_image
        self.sender_email = sender_email
        self.sender_pass = sender_pass
        self.reciever_email = reciever_email

        self.tmp_img = Image.fromarray(car_image)
        self.tmp_img.save(self.image_path)

        return self.predictor.predict(car_image)