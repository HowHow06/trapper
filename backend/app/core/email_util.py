
from pathlib import Path
from typing import Any, Dict

import emails
from app.core.config import settings
from emails.template import JinjaTemplate


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    # if settings.SMTP_TLS:
    #     smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)


def send_complete_scan_email(email_to: str, task_name: str, task_id: int) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Scan Task Completed"
    template_path = Path(settings.EMAIL_TEMPLATES_DIR) / "complete_scan.html"
    print(template_path)
    with open(template_path) as f:
        template_str = f.read()
    server_host = settings.VITE_CONSOLE_PANEL_URL
    link = f"{server_host}/tasks/{task_id}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "task_name": task_name,
            "email": email_to,
            "link": link,
        },
    )
