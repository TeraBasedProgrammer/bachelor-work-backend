import smtplib
from email.message import EmailMessage

from pydantic import EmailStr

from app.config.settings.base import settings


def get_email_template_dashboard(
    user_email: EmailStr, user_full_name: str, reset_link: str
) -> EmailMessage:
    email = EmailMessage()
    email["Subject"] = "Password reset request"
    email["From"] = settings.SMTP_USER
    email["To"] = user_email

    email.set_content(
        f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h2 style="color: #333;">Hello, {user_full_name}</h2>
                <p style="font-size: 16px; color: #555;">
                    You have requested to reset your password. To proceed, please click the button below:
                </p>
                <p style="text-align: center;">
                    <a href="{reset_link}"
                       style="display: inline-block; padding: 12px 24px; font-size: 16px; color: #fff;
                              background-color: #1a73e8; text-decoration: none; border-radius: 6px;">
                        Reset Password
                    </a>
                </p>
                <p style="font-size: 14px; color: #777;">
                    If you did not request this, simply ignore this email.
                </p>
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="font-size: 14px; color: #555;">Best regards,</p>
                <p style="font-size: 14px; color: #555;">Illia Dronov</p>
            </div>
        </body>
        </html>
        """,
        subtype="html",
    )

    return email


def send_email_report_dashboard(user_email: EmailStr, user_name: str, reset_link: str):
    email = get_email_template_dashboard(user_email, user_name, reset_link)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email)
