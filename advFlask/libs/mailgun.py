from typing import List
from requests import Response, post


class Mailgun:
    MAILGUN_DOMAIN = "sandbox23f2c3abc7694493bd6e5f8b76a819b2.mailgun.org"
    MAILGUN_API_KEY = "13dd4f28fde2a0c4476f22fbb0c604fe-898ca80e-3ba42076"
    FROM_TITLE = "Stores REST API"
    FROM_EMAIL = (
        "postmaster@sandbox23f2c3abc7694493bd6e5f8b76a819b2.mailgun.org"
    )

    def send_email(
        cls, email: List[str], subject: str, text: str, html: str
    ) -> Response:
        return post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )
