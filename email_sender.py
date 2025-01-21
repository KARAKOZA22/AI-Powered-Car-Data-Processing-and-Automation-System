import smtplib  # Library for sending emails using SMTP
import os  # Library for interacting with the file system
from email.mime.text import MIMEText  # For creating text email content
from email.mime.multipart import MIMEMultipart  # For creating multipart emails (text + attachments)
from email.mime.image import MIMEImage  # For attaching images to emails

class EmailSender:
    """
    A class to handle sending emails with optional image attachments.

    Attributes:
        sender_email (str): The email address of the sender.
        sender_password (str): The password for the sender's email account.
        smtp_server (str, optional): Custom SMTP server address. If not provided, it is determined automatically.
        smtp_port (int, optional): Custom SMTP server port. If not provided, it is determined automatically.
    """

    def __init__(self, sender_email, sender_password, smtp_server=None, smtp_port=None):
        """
        Initializes the EmailSender with sender email, password, and optional SMTP server details.

        Args:
            sender_email (str): The email address of the sender.
            sender_password (str): The password for the sender's email account.
            smtp_server (str, optional): Custom SMTP server address. Defaults to None.
            smtp_port (int, optional): Custom SMTP server port. Defaults to None.
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def _get_smtp_details(self):
        """
        Determines the SMTP server and port based on the sender's email domain.

        Returns:
            tuple: A tuple containing the SMTP server address and port number.

        Raises:
            ValueError: If the email provider is not supported (e.g., not Outlook, Gmail, Hotmail, or Yahoo).
        """
        if "@outlook.com" in self.sender_email or "@hotmail.com" in self.sender_email:
            return "smtp.office365.com", 587  # Outlook/Hotmail SMTP details
        elif "@gmail.com" in self.sender_email:
            return "smtp.gmail.com", 587  # Gmail SMTP details
        elif "@yahoo.com" in self.sender_email:
            return "smtp.mail.yahoo.com", 465  # Yahoo SMTP details (uses SSL)
        else:
            raise ValueError("Unsupported email provider. Please use Outlook, Gmail, Hotmail, or Yahoo.")

    def send_email(self, subject, body, recipient_email, image_path=None):
        """
        Sends an email with the provided subject, body, and optional image attachment.

        Args:
            subject (str): The subject of the email.
            body (str): The body text of the email.
            recipient_email (str): The email address of the recipient.
            image_path (str, optional): The file path to an image to attach. Defaults to None.

        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """
        try:
            # Determine SMTP server and port if not provided
            smtp_server, smtp_port = self.smtp_server or self._get_smtp_details()

            # Create a multipart email message
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = recipient_email
            message["Subject"] = subject

            # Attach the body text to the email
            message.attach(MIMEText(body, "plain"))

            # Attach the image if provided and the file exists
            if image_path and os.path.exists(image_path):
                with open(image_path, "rb") as image_file:
                    img = MIMEImage(image_file.read())  # Read the image file
                    img.add_header("Content-Disposition", f"attachment; filename={os.path.basename(image_path)}")
                    message.attach(img)  # Attach the image to the email

            # Send the email using the appropriate SMTP protocol
            if smtp_port == 465:  # Use SSL for Yahoo
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    server.login(self.sender_email, self.sender_password)  # Log in to the SMTP server
                    server.sendmail(self.sender_email, recipient_email, message.as_string())  # Send the email
            else:  # Use TLS for Outlook and Gmail
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()  # Start TLS encryption
                    server.login(self.sender_email, self.sender_password)  # Log in to the SMTP server
                    server.sendmail(self.sender_email, recipient_email, message.as_string())  # Send the email

            print("Email sent successfully!")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False