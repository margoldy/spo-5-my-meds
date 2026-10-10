import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv


load_dotenv()

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_KEY = os.getenv("MAIL_KEY")
MAIL_FROM = os.getenv("MAIL_FROM", MAIL_USERNAME)
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.mail.ru")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))


def send_auth_code(email: str, code: str) -> None:
    if not MAIL_USERNAME or not MAIL_KEY or not MAIL_FROM:
        raise RuntimeError("Mail settings are not configured")

    message = EmailMessage()
    message["Subject"] = "Код для входа в «Мою аптечку»"
    message["From"] = MAIL_FROM
    message["To"] = email
    message.set_content(
        f"Ваш код для входа: {code}\n\n"
        "Код действует 5 минут. Если вы его не запрашивали, "
        "просто проигнорируйте письмо."
    )

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(MAIL_USERNAME, MAIL_KEY)
            server.send_message(message)
    except smtplib.SMTPAuthenticationError as error:
        raise RuntimeError("Invalid MAIL_USERNAME or MAIL_KEY") from error
    except Exception as error:
        raise RuntimeError(f"Failed to send email: {error}") from error
