from .config import settings
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, SecretStr


class EmailUtility:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=SecretStr(settings.MAIL_PASSWORD),
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
            MAIL_STARTTLS=settings.MAIL_STARTTLS,
            USE_CREDENTIALS=settings.MAIL_USE_CREDENTIALS,
            TEMPLATE_FOLDER=settings.BASE_DIR / "templates",
        )
        self.fm = FastMail(self.conf)

    async def send_email(
        self, email: EmailStr, subject: str, template_name: str, context: dict
    ):
        """
        Schedule email sending in the background automatically.
        """
        message = MessageSchema(
            subject=subject,
            recipients=[email],
            subtype=MessageType.html,
            template_body=context,
        )

        await self.fm.send_message(message=message, template_name=template_name)


async def test_send_email():
    email_utility = EmailUtility()

    email = "hello@alicestone.me"
    subject = "Welcome to Serious Connection!"
    template_name = "emails/auth/welcome.html"
    context = {
        "name": "Alice Stone",
        "project_name": settings.PROJECT_NAME,
        "year": 2025,
    }

    await email_utility.send_email(
        email=email, template_name=template_name, context=context, subject=subject
    )
