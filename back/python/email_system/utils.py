import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(recipient: str, subject: str, html_content: str) -> None:
    message = MIMEMultipart("alternative")
    message['From'] = os.getenv("SMTP_ROOT_EMAIL")
    message['To'] = recipient
    message['Subject'] = subject

    body = MIMEText(html_content, 'html')
    message.attach(body)

    server = smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT")))

    try:
        server.starttls()
        server.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
        server.send_message(message)
    except Exception as e:
        raise Exception(f"Failed sending email: {str(e)}")
    finally:
        server.close()
