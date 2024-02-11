import logging
from typing import Dict, Any

from emails import Message
from emails.template import JinjaTemplate
from src.app.core.config import paths, stmp_settings, app_settings


async def _send_email(
    email_to: str,
    params: Dict[str, Any],
    subject: str = "",
    html_template: str = "",
) -> None:
    message = Message(
        subject=JinjaTemplate(subject),
        html=JinjaTemplate(html_template),
        mail_from=(app_settings.PROJECT_NAME, app_settings.PROJECT_EMAIL),
    )
    response = message.send(
        to=email_to,
        render=params,
        smtp={
            "host": stmp_settings.STMP_HOST,
            "port": stmp_settings.STMP_PORT,
            "user": stmp_settings.STMP_USER,
            "password": stmp_settings.STMP_PASSWORD,
        },
    )
    logging.info(f"Send email result: {response}")


async def send_reset_password_email(
    email_to: str, token: str, username: str
) -> None:
    subject = f"Password recowery for user {username}"
    with open(
        paths.EMAIL_TEMPLATES_PATH / "reset_password.html", encoding="utf-8"
    ) as file:
        template_str = file.read()
    link = f"{app_settings.SERVER_HOST}/password-reset?token={token}"
    await _send_email(
        email_to=email_to,
        subject=subject,
        html_template=template_str,
        params={
            "email_to": email_to,
            "username": username,
            "link": link,
            "valid_hours": 24,
        },
    )


async def send_new_account_email(email_to: str, username: str) -> None:
    subject = f"New account for user {username}"
    with open(
        paths.EMAIL_TEMPLATES_PATH / "new_account.html", encoding="utf-8"
    ) as file:
        template_str = file.read()
    link = app_settings.SERVER_HOST
    await _send_email(
        email_to=email_to,
        subject=subject,
        html_template=template_str,
        params={
            "email_to": "email_to",
            "username": username,
            "link": link,
        },
    )
