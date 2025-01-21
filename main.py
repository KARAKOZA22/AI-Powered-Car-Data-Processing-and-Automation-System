import gradio as gr  # Gradio library for creating the web interface
import time  # For measuring the time taken to process the request
from car_data_processor import CarDataProcessor  # Module to process car data
from email_sender import EmailSender  # Module to send emails
from car_information_extractor import CarInformationExtractor  # Module to extract car information using AI

def on_submit(car_description, sender_email, sender_pass, reciever_email, car_image):
    """
    Handles the submission of car data, processes it, and sends an email with the results.

    Args:
        car_description (str): Description of the car provided by the user.
        sender_email (str): Email address of the sender.
        sender_pass (str): Password for the sender's email account.
        reciever_email (str): Email address of the receiver.
        car_image (numpy.ndarray): Image of the car uploaded by the user.

    Returns:
        tuple: A tuple containing:
            - Predicted car type (str).
            - Status message (str) indicating whether the email was sent successfully and the time taken.
    """
    # Record the start time to measure the total processing time
    start_time = time.time()

    # Initialize the CarDataProcessor to handle car data
    processor = CarDataProcessor()
    # Process the inputs (save the image and predict the car type)
    _ = processor.process_inputs(car_description, sender_email, sender_pass, reciever_email, car_image)

    # Initialize the EmailSender to send emails
    email_sender = EmailSender(sender_email, sender_pass)

    # Define the email subject
    subject = "The Car Image with the Generated JSON"

    # Extract car information and predict the car type using CarInformationExtractor
    body, predicted_car_type = CarInformationExtractor().process_car_info(input_text=car_description, car_image="")

    # Send the email with the extracted information and car image
    email_sent = email_sender.send_email(subject, body, reciever_email, image_path=processor.image_path)

    # Record the end time and calculate the total time taken
    end_time = time.time()
    time_taken = round(end_time - start_time, 2)

    # Return the results based on whether the email was sent successfully
    if email_sent:
        return predicted_car_type, f"Email sent successfully! Time taken: {time_taken} seconds"
    else:
        return predicted_car_type, "Failed to send email. Please check your details and try again."

# Create a Gradio interface for the web application
demo = gr.Interface(
    fn=on_submit,  # Function to call when the user submits the form
    inputs=[
        gr.Textbox(label="Car Description", lines=4),  # Input for car description
        gr.Textbox(label="Sender Email"),  # Input for sender's email
        gr.Textbox(label="Sender Email Password (Use App password for more security don't use your actual Password)"),  # Input for sender's email password
        gr.Textbox(label="Receiver Email"),  # Input for receiver's email
        gr.Image(label="Upload Car Image")  # Input for uploading car image
    ],
    outputs=[
        gr.Textbox(label="Predicted Car Type"),  # Output for predicted car type
        gr.Textbox(label="Time Taken")  # Output for time taken to process the request
    ]
)

# Launch the Gradio interface with sharing enabled
demo.launch(share=True)