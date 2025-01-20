import os
import re
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.schema.output_parser import OutputParserException
from car_classifier import CarTypePredictor

class CarInformationExtractor:
    def __init__(self, openai_api_key=None, model_name="gpt-4o-mini", azure_endpoint=None):
        load_dotenv("/content/KEY.env")

        if not openai_api_key:
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OpenAI API key is required. Please provide it or set it in the .env file.")

        if not azure_endpoint:
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            if not azure_endpoint:
                raise ValueError("Azure OpenAI endpoint is required. Please provide it or set it in the .env file.")

        self.model_name = model_name
        self.azure_chat_model = AzureChatOpenAI(
            openai_api_key=openai_api_key,
            model=self.model_name,
            openai_api_version="2024-08-01-preview"
        )

    def generate_prompt(self, structure, text):
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
        pattern = r'\"body_type\":\s*\"(.*?)\"'
        updated_json_string = re.sub(pattern, f'\"body_type\": \"{predicted_body_type}\"', llm_output)
        return updated_json_string

    def process_car_info(self, input_text, car_image, json_structure=None):
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

        prompt = self.generate_prompt(json_structure, input_text)
        try:
            response = self.azure_chat_model.invoke(prompt)
            model_output = response.content
            predicted_body_type = CarTypePredictor().predict(car_image)
            updated_json_string = self.replace_body_type(model_output, predicted_body_type)

            return updated_json_string, predicted_body_type

        except OutputParserException as e:
            print("Error parsing the model's output:", e)
            return {},""
        except Exception as e:
            print("An error occurred:", e)
            return {},""