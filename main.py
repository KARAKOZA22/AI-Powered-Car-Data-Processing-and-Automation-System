import gradio as gr
import time
from car_data_processor import CarDataProcessor
from email_sender import EmailSender
from car_information_extractor import CarInformationExtractor

def on_submit(car_description, sender_email, sender_pass, reciever_email, car_image):
    start_time = time.time()

    processor = CarDataProcessor()
    _ = processor.process_inputs(car_description, sender_email, sender_pass, reciever_email, car_image)
    email_sender = EmailSender(sender_email, sender_pass)

    subject = "The Car Image with the Generated JSON"
    body, predicted_car_type = CarInformationExtractor().process_car_info(input_text=car_description, car_image="")

    email_sent = email_sender.send_email(subject, body, reciever_email, image_path=processor.image_path)

    end_time = time.time()
    time_taken = round(end_time - start_time, 2)

    if email_sent:
        return predicted_car_type, f"Email sent successfully! Time taken: {time_taken} seconds"
    else:
        return predicted_car_type, "Failed to send email. Please check your details and try again."

demo = gr.Interface(
    fn=on_submit,
    inputs=[
        gr.Textbox(label="Car Description", lines=4),
        gr.Textbox(label="Sender Email"),
        gr.Textbox(label="Sender Email Password (Use App password for more security don't use your actual Password)"),
        gr.Textbox(label="Receiver Email"),
        gr.Image(label="Upload Car Image")
    ],
    outputs=[
        gr.Textbox(label="Predicted Car Type"),
        gr.Textbox(label="Time Taken")
    ]
)

demo.launch(share=True)