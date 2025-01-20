import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

class EmailSender:
    def __init__(self, sender_email, sender_password, smtp_server=None, smtp_port=None):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def _get_smtp_details(self):
        if "@outlook.com" in self.sender_email or "@hotmail.com" in self.sender_email:
            return "smtp.office365.com", 587
        elif "@gmail.com" in self.sender_email:
            return "smtp.gmail.com", 587
        elif "@yahoo.com" in self.sender_email:
            return "smtp.mail.yahoo.com", 465
        else:
            raise ValueError("Unsupported email provider. Please use Outlook, Gmail, Hotmail, or Yahoo.")

    def send_email(self, subject, body, recipient_email, image_path=None):
        try:
            smtp_server, smtp_port = self.smtp_server or self._get_smtp_details()

            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = recipient_email
            message["Subject"] = subject

            message.attach(MIMEText(body, "plain"))

            if image_path and os.path.exists(image_path):
                with open(image_path, "rb") as image_file:
                    img = MIMEImage(image_file.read())
                    img.add_header("Content-Disposition", f"attachment; filename={os.path.basename(image_path)}")
                    message.attach(img)

            if smtp_port == 465:
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    server.login(self.sender_email, self.sender_password)
                    server.sendmail(self.sender_email, recipient_email, message.as_string())
            else:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(self.sender_email, self.sender_password)
                    server.sendmail(self.sender_email, recipient_email, message.as_string())

            print("Email sent successfully!")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False