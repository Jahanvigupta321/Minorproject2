import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from io import BytesIO

def send_email(sender_email, sender_password, receiver_email, subject, body, attachment_file):
    # Fixed subject and body content
    subject = "Fixed Subject"
    body = "This is the fixed body content of the email."

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach text message
    msg.attach(MIMEText(body, 'plain'))

    # Attach image
    if attachment_file is not None:
        attachment_data = attachment_file.read()
        attachment_filename = attachment_file.name
        attachment_mime = MIMEImage(attachment_data)
        attachment_mime.add_header('Content-Disposition', 'attachment', filename=attachment_filename)
        msg.attach(attachment_mime)

    # Connect to SMTP server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print(f"Email sent successfully to {receiver_email}!")
    except Exception as e:
        print(f"Error sending email to {receiver_email}: {e}")
    finally:
        server.quit()
