import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from django.utils.crypto import get_random_string
from django.core.cache import caches
from configs.settings import env
from rest_framework.exceptions import APIException

OTP_LENGTH = 6
OTP_TTL = 15 * 60
SMTP_PORT = 587

class OTPService:
    def send_otp(self, email: str) -> None:
        random_str = get_random_string(OTP_LENGTH)
        self.save_otp(email, random_str)

        host = env.str('DEFAULT_EMAIL_HOST', '')
        password = env.str('DEFAULT_EMAIL_PASS', '')
        receiver_email = email

        # Create a multipart message
        message = MIMEMultipart()
        message['From'] = host
        message['To'] = receiver_email
        message['Subject'] = 'Joy Verification Code'

        body = 'Your verification code is ' + random_str
        message.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', SMTP_PORT)
            server.starttls()
            server.login(host, password)
            server.send_message(message)
            print('Email sent successfully!')
        except Exception as e:
            print(f'Failed to send email. Error: {str(e)}', e.__class__)
            raise APIException()
        finally:
            server.quit()  # Terminate the SMTP session

    @classmethod
    def save_otp(cls, email: str, otp: str) -> None:
        caches['default'].set(cls.generate_cache_key(email), otp, OTP_TTL)

    @classmethod
    def get_otp(cls, email: str) -> Optional[str]:
        return caches["default"].get(cls.generate_cache_key(email))

    @classmethod
    def generate_cache_key(cls, email: str) -> str:
        return email + ":otp"

    @classmethod
    def is_otp_valid(cls, otp: str, email: str):
        return cls.get_otp(email) == otp
