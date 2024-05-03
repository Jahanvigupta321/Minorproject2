import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
class EmailSender:
    def __init__(self):
        # Gmail SMTP configuration
        self.email = "jarus6124@gmail.com"  
        self.password = "psvm wukp vbnl tnlv"     
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_email(self, to_email, subject, body, attachment_path):
        server = None  # Initialize the server variable
        try:
            # Create a secure SSL context
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)

            # Create message container - the correct MIME type is multipart/alternative
            message = MIMEMultipart()
            message['From'] = self.email
            message['To'] = to_email
            message['Subject'] = subject

            # Attach body text
            message.attach(MIMEText(body, 'plain'))

            # Attach file
            if attachment_path:
                filename = os.path.basename(attachment_path)
                attachment = open(attachment_path, "rb")
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename= {filename}")
                message.attach(part)

            # Send email
            print
            server.sendmail(self.email, to_email, message.as_string())
            print(f"Email sent successfully to {to_email}")
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            # Close connection
            if server:
                server.quit()
