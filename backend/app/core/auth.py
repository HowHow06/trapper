import random
import string
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional, Union

import jwt
from app.core.config import settings
from app.core.email_util import send_email
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.ACCESS_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    template_path = Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html"
    print(template_path)
    with open(template_path) as f:
        template_str = f.read()
    server_host = settings.VITE_CONSOLE_PANEL_URL
    link = f"{server_host}/auth/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


# No longer using the function below
def send_reset_password_success_email(email_to: str, email: str, new_password: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password Reset Successful for user {email}"
    template_path = Path(settings.EMAIL_TEMPLATES_DIR) / \
        "reset_password_success.html"
    print(template_path)
    with open(template_path) as f:
        template_str = f.read()
    server_host = settings.VITE_CONSOLE_PANEL_URL
    link = f"{server_host}/auth/login"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "new_password": new_password,
            "link": link,
        },
    )


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.ACCESS_TOKEN_SECRET_KEY, algorithm=ALGORITHM,
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(
            token, settings.ACCESS_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token["sub"]  # user's email
    except (jwt.PyJWTError) as error:
        return None


def generate_password(length: int = 8):
    """Generate a random password of a given length"""
    all_chars = string.ascii_letters + string.digits
    password = ''.join(random.choice(all_chars) for i in range(length))
    return password
