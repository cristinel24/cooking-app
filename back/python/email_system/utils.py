import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from constants import SMTP_PASSWORD, SMTP_PORT, SMTP_ROOT_EMAIL, SMTP_SERVER, SMTP_USERNAME, ErrorCodes, COMPILED_EMAIL_VALIDATION_REGEX


def send_email(recipient: str, subject: str, html_content: str) -> None:
    message = MIMEMultipart("alternative")
    message['From'] = SMTP_ROOT_EMAIL
    message['To'] = recipient
    message['Subject'] = subject

    body = MIMEText(html_content, 'html')
    message.attach(body)

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    except Exception:
        raise Exception(ErrorCodes.SMTP_CONNECTION_FAILED.value)
    try:
        try:
            server.starttls()
        except Exception:
            raise Exception(ErrorCodes.SMTP_TTLS_FAILED.value)
        try:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
        except Exception:
            raise Exception(ErrorCodes.SMTP_LOGIN_FAILED.value)
        try:
            server.send_message(message)
        except Exception:
            raise Exception(ErrorCodes.SMTP_SEND_EMAIL_FAILED.value)
    except Exception as e:
        server.close()
        raise e
    server.close()


def validate_email(email: str) -> bool:
    return re.match(COMPILED_EMAIL_VALIDATION_REGEX, email) is not None
