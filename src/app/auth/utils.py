async def _send_email() -> None:
    ...


async def send_reset_password_email(email_to: str, token: str) -> None:  # noqa
    await _send_email()
