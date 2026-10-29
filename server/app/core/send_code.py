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
    message.add_alternative(
        f"""
        <!doctype html>
        <html lang="ru">
          <head>
            <meta name="color-scheme" content="light only">
            <meta name="supported-color-schemes" content="light only">
            <style>
              :root {{ color-scheme: light only; }}
              @media (prefers-color-scheme: dark) {{
                .page {{ background-color: #f4f4f4 !important; }}
                .card {{ background-color: #fff4d6 !important; }}
                .code-box {{ background-color: #fffaf0 !important; }}
                .title, .text {{ color: #4b4b7c !important; }}
                .accent {{ color: #d94f59 !important; }}
                .muted {{ color: #a96d72 !important; }}
              }}
            </style>
          </head>
          <body class="page" bgcolor="#f4f4f4" style="margin:0; padding:0; background-color:#f4f4f4 !important; color-scheme:light only;">
            <table class="page" role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#f4f4f4" style="background-color:#f4f4f4 !important;">
              <tr>
                <td align="center" style="padding:32px 12px;">
                  <table class="card" role="presentation" width="420" cellspacing="0" cellpadding="0" border="0" bgcolor="#fff4d6" style="width:100%; max-width:420px; background-color:#fff4d6 !important;">
                    <tr>
                      <td align="center" style="padding:30px 28px 12px;">
                        <table role="presentation" cellspacing="0" cellpadding="0" border="0">
                          <tr>
                            <td class="accent" align="center" width="48" height="48" style="width:48px; height:48px; border:3px solid #ff8e9d; border-radius:50%; color:#ff8e9d !important; font-family:Georgia,'Times New Roman',serif; font-size:31px; font-weight:bold; line-height:42px;">✽</td>
                          </tr>
                        </table>
                        <h1 class="title" style="margin:14px 0 0; color:#4b4b7c !important; font-family:Georgia,'Times New Roman',serif; font-size:25px; line-height:1.3; font-weight:bold;">Моя аптечка</h1>
                      </td>
                    </tr>
                    <tr>
                      <td align="center" style="padding:10px 28px 8px;">
                        <p class="accent" style="margin:0 0 10px; color:#d94f59 !important; font-family:Georgia,'Times New Roman',serif; font-size:17px; line-height:1.45;">Код для входа</p>
                        <table class="code-box" role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#fffaf0" style="background-color:#fffaf0 !important; border-radius:5px;">
                          <tr>
                            <td class="title" align="center" style="padding:16px 12px; color:#4b4b7c !important; font-family:Georgia,'Times New Roman',serif; font-size:32px; font-weight:bold; letter-spacing:8px; line-height:1.2;">{code}</td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                    <tr>
                      <td align="center" style="padding:12px 30px 30px;">
                        <p class="text" style="margin:0 0 8px; color:#4b4b7c !important; font-family:Georgia,'Times New Roman',serif; font-size:15px; line-height:1.5;">Введите код в приложении.<br>Он действует 5 минут.</p>
                        <p class="muted" style="margin:0; color:#a96d72 !important; font-family:Georgia,'Times New Roman',serif; font-size:12px; line-height:1.45;">Если вы не запрашивали код, просто проигнорируйте письмо.</p>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </body>
        </html>
        """,
        subtype="html",
    )

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(MAIL_USERNAME, MAIL_KEY)
            server.send_message(message)
    except smtplib.SMTPAuthenticationError as error:
        raise RuntimeError("Invalid MAIL_USERNAME or MAIL_KEY") from error
    except Exception as error:
        raise RuntimeError(f"Failed to send email: {error}") from error
