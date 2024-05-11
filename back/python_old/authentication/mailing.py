import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(recipient: str, subject: str, body_text: str) -> None:
    message = MIMEMultipart()
    message['From'] = os.getenv("SMTP_ROOT_EMAIL")
    message['To'] = recipient
    message['Subject'] = subject
    body = MIMEText(body_text, 'plain')
    message.attach(body)

    server = smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT")))
    server.starttls()

    try:
        server.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
        server.sendmail(os.getenv("SMTP_ROOT_EMAIL"), recipient, message.as_string())
    except Exception as e:
        raise Exception(f"Failed sending email: {str(e)}")
    finally:
        server.close()
