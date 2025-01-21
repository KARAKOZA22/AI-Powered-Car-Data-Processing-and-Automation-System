# Orion360 Project

This project processes car descriptions and images to predict car types and extract structured information. It also sends an email with the processed data.



## Table of Contents
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Modules](#modules)
- [Dependencies](#dependencies)
  

## Setup

1. **Clone the repository:**
   
   ```bash
   !git clone https://github.com/yourusername/Orion360.git
   cd Orion360
   ```
2. **Install the required libraries:**

   ```bash
    !pip install -r requirements.txt
   ```
3. **Set up environment variables:**
   
    - Create a .env file in the root directory (Make Sure to name it KEY.env and add its path for the load_dotenv("your-path")).</li>
    - Add your OpenAI API key and Azure endpoint:</li>
  
  
   ```bash
    OPENAI_API_KEY=your_openai_api_key
    AZURE_OPENAI_ENDPOINT=your_azure_endpoint
   ```

    - Make sure to add path of image where it will be saved and where it will uploaded from (you can access it and modify it from the CarDataProcessor class)
    
   ```bash
    self.image_path = "your-path"
   ```

## Running the Application

   ```bash
      !python main.py
   ```

## Project Structure

Orion360/<br>
│<br>
├── README.md<br>
├── requirements.txt<br>
├── car_classifier.py<br>
├── car_data_processor.py<br>
├── car_information_extractor.py<br>
├── email_sender.py<br>
├── Notebook.ipynb<br>
└── main.py<br>

## Modules


1. **car_classifier.py**

- Contains the CarTypePredictor class which predicts the type of car based on an image.


2. **car_data_processor.py**

- Contains the CarDataProcessor class which processes car descriptions and images.

3. **car_information_extractor.py**
   
- Contains the CarInformationExtractor class which extracts structured information from car descriptions using Azure OpenAI.

4. **email_sender.py**
   
- Contains the EmailSender class which handles sending emails with the processed car information.

5. **main.py**

- The main script that runs the Gradio interface and integrates all the modules.

## Dependencies

**The project requires the following Python libraries:** <br>

- gradio

- langchain-openai

- python-dotenv

- numpy

- smtplib

- requests

- Pillow
