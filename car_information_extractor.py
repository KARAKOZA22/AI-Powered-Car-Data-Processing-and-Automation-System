import os  # Library for interacting with the file system
import re  # Library for regular expressions
from dotenv import load_dotenv  # Library for loading environment variables from a .env file
from langchain_openai import AzureChatOpenAI  # Library for interacting with Azure OpenAI models
from langchain.schema.output_parser import OutputParserException  # Exception for handling output parsing errors
from car_classifier import CarTypePredictor  # Module for predicting car types

class CarInformationExtractor:
    """
    A class to extract structured information from car descriptions using Azure OpenAI.

    Attributes:
        model_name (str): The name of the Azure OpenAI model to use.
        azure_chat_model (AzureChatOpenAI): The Azure OpenAI model instance.
    """

    def __init__(self, openai_api_key=None, model_name="gpt-4o-mini", azure_endpoint=None):
        """
        Initializes the CarInformationExtractor with the Azure OpenAI model.

        Args:
            openai_api_key (str, optional): The OpenAI API key. If not provided, it is loaded from the .env file.
            model_name (str, optional): The name of the Azure OpenAI model. Defaults to "gpt-4o-mini".
            azure_endpoint (str, optional): The Azure OpenAI endpoint. If not provided, it is loaded from the .env file.

        Raises:
            ValueError: If the OpenAI API key or Azure OpenAI endpoint is missing.
        """
        # Load environment variables from the .env file
        load_dotenv("/content/KEY.env")

        # Set the OpenAI API key (either provided or loaded from .env)
        if not openai_api_key:
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OpenAI API key is required. Please provide it or set it in the .env file.")

        # Set the Azure OpenAI endpoint (either provided or loaded from .env)
        if not azure_endpoint:
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            if not azure_endpoint:
                raise ValueError("Azure OpenAI endpoint is required. Please provide it or set it in the .env file.")

        # Initialize the Azure OpenAI model
        self.model_name = model_name
        self.azure_chat_model = AzureChatOpenAI(
            openai_api_key=openai_api_key,
            model=self.model_name,
            openai_api_version="2024-08-01-preview"
        )

    def generate_prompt(self, structure, text):
        """
        Generates a prompt for the Azure OpenAI model to extract structured data from the car description.

        Args:
            structure (dict): The JSON structure that the output should follow.
            text (str): The car description text to process.

        Returns:
            list: A list of tuples containing the system message and the car description text.
        """
        system_message = (
            f"You are an expert at extracting structured data from text. \n"
            f"Your task is to convert the provided car description into a JSON format that matches the following structure: {structure}. "
            f"Ensure all values in the output JSON strictly adhere to the specified types in the structure. \n"
            f"Determine whether the price mentioned in the text is a direct price or an estimated price. Use the field name 'price' if it is explicitly stated as a price, or 'estimated_price' if it is described as an estimate. Convert the price to an integer amount in the smallest currency unit (e.g., 220K L.E. becomes 220000). \n"
            f"Pay close attention to details like numbers, strings, and nested structures. \n"
            f"Here is the text to process:\n\n{text}\n\n"
            f"Provide only the JSON output as a string without any additional explanation or commentary. "
        )
        return [("system", system_message), ("human", text)]

    def replace_body_type(self, llm_output, predicted_body_type):
        """
        Replaces the "body_type" field in the JSON output with the predicted car type.

        Args:
            llm_output (str): The JSON output from the Azure OpenAI model.
            predicted_body_type (str): The predicted car type from the CarTypePredictor.

        Returns:
            str: The updated JSON string with the predicted body type.
        """
        pattern = r'\"body_type\":\s*\"(.*?)\"'
        updated_json_string = re.sub(pattern, f'\"body_type\": \"{predicted_body_type}\"', llm_output)
        return updated_json_string

    def process_car_info(self, input_text, car_image, json_structure=None):
        """
        Processes the car description and image to extract structured information.

        Args:
            input_text (str): The car description text.
            car_image (numpy.ndarray): The car image (used to predict the car type).
            json_structure (dict, optional): The JSON structure for the output. Defaults to a predefined structure.

        Returns:
            tuple: A tuple containing:
                - The updated JSON string with the predicted body type.
                - The predicted car type.
        """
        # Default JSON structure if not provided
        if json_structure is None:
            json_structure = {
                "car": {
                    "body_type": "Unknown",
                    "color": "string",
                    "brand": "string",
                    "model": "string",
                    "manufactured_year": "integer",
                    "motor_size_cc": "integer",
                    "tires": {
                        "type": "string",
                        "manufactured_year": "integer"
                    },
                    "windows": "string",
                    "notices": [
                        {
                            "type": "string",
                            "description": "string"
                        }
                    ],
                    "price_or_estimated_price": {
                        "amount": "integer",
                        "currency": "string"
                    }
                }
            }

        # Generate the prompt for the Azure OpenAI model
        prompt = self.generate_prompt(json_structure, input_text)

        try:
            # Invoke the Azure OpenAI model to process the car description
            response = self.azure_chat_model.invoke(prompt)
            model_output = response.content

            # Predict the car type using the CarTypePredictor
            predicted_body_type = CarTypePredictor().predict(car_image)

            # Replace the "body_type" field in the JSON output with the predicted car type
            updated_json_string = self.replace_body_type(model_output, predicted_body_type)

            return updated_json_string, predicted_body_type

        except OutputParserException as e:
            # Handle errors in parsing the model's output
            print("Error parsing the model's output:", e)
            return {}, ""
        except Exception as e:
            # Handle any other exceptions
            print("An error occurred:", e)
            return {}, ""