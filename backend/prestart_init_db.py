import asyncio
import logging

from app import crud, schemas
from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models import Vulnerability
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_admin(db: AsyncSession) -> None:
    user = await crud.crud_user.get_by_email_or_username(
        db, email=settings.FIRST_SUPERUSER_EMAIL, username=settings.FIRST_SUPERUSER_USERNAME)
    if not user:
        user_in = schemas.UserCreate(
            username=settings.FIRST_SUPERUSER_USERNAME,
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_admin=True
        )
        user = await crud.crud_user.create(db, obj_in=user_in)


async def init_user(db: AsyncSession) -> None:
    user = await crud.crud_user.get_by_email_or_username(
        db, email=settings.FIRST_USER_EMAIL, username=settings.FIRST_USER_USERNAME)
    if not user:
        user_in = schemas.UserCreate(
            username=settings.FIRST_USER_USERNAME,
            email=settings.FIRST_USER_EMAIL,
            password=settings.FIRST_USER_PASSWORD,
            is_admin=False
        )
        user = await crud.crud_user.create(db, obj_in=user_in)


async def init_lookup_status(db: AsyncSession) -> None:
    statuses = await crud.crud_lookup.get_multi_by_type(
        db, type=settings.LOOKUP_TYPE_STATUS)
    if len(statuses) != 5:
        waiting_status = schemas.LookupCreate(
            id=1,
            type=settings.LOOKUP_TYPE_STATUS,
            name="WAITING",
            description="Status when the task/scan request is created but not processed (for both Scan Request and Task)."
        )
        await crud.crud_lookup.create(db, obj_in=waiting_status)
        running_status = schemas.LookupCreate(
            id=2,
            type=settings.LOOKUP_TYPE_STATUS,
            name="RUNNING",
            description="Status when the task/scan request is being processed (for both Scan Request and Task)."
        )
        await crud.crud_lookup.create(db, obj_in=running_status)
        done_status = schemas.LookupCreate(
            id=3,
            type=settings.LOOKUP_TYPE_STATUS,
            name="DONE",
            description="Status when the task/scan request is completed (for both Scan Request and Task)."
        )
        await crud.crud_lookup.create(db, obj_in=done_status)
        killed_status = schemas.LookupCreate(
            id=4,
            type=settings.LOOKUP_TYPE_STATUS,
            name="KILLED",
            description="Status when the task is killed when user click the stop task button, right before the task is done (for Task only)."
        )
        await crud.crud_lookup.create(db, obj_in=killed_status)
        paused_status = schemas.LookupCreate(
            id=9,
            type=settings.LOOKUP_TYPE_STATUS,
            name="PAUSED",
            description="Status when the task is paused when user click the pause task button (for Task only)."
        )
        await crud.crud_lookup.create(db, obj_in=paused_status)


async def init_lookup_severity(db: AsyncSession) -> None:
    severity_levels = await crud.crud_lookup.get_multi_by_type(
        db, type=settings.LOOKUP_TYPE_SEVERITY_LEVEL)
    if len(severity_levels) != 3:
        low_level = schemas.LookupCreate(
            id=5,
            type=settings.LOOKUP_TYPE_SEVERITY_LEVEL,
            name="LOW",
            description="Low severity level"
        )
        await crud.crud_lookup.create(db, obj_in=low_level)
        medium_level = schemas.LookupCreate(
            id=6,
            type=settings.LOOKUP_TYPE_SEVERITY_LEVEL,
            name="MEDIUM",
            description="Medium severity level"
        )
        await crud.crud_lookup.create(db, obj_in=medium_level)
        high_level = schemas.LookupCreate(
            id=7,
            type=settings.LOOKUP_TYPE_SEVERITY_LEVEL,
            name="HIGH",
            description="High severity level"
        )
        await crud.crud_lookup.create(db, obj_in=high_level)


async def init_lookup_vulnerability_type(db: AsyncSession) -> None:
    vuln_types = await crud.crud_lookup.get_multi_by_type(
        db, type=settings.LOOKUP_TYPE_VULNERABILITY_TYPE)
    if len(vuln_types) != 1:
        xss_type = schemas.LookupCreate(
            id=8,
            type=settings.LOOKUP_TYPE_VULNERABILITY_TYPE,
            name="XSS",
            description="Cross site scripting vulnerability (XSS)"
        )
        await crud.crud_lookup.create(db, obj_in=xss_type)


async def init_xss_vulnerability(db: AsyncSession) -> None:
    condition = Vulnerability.type_id == 8  # meaning is xss vuln type
    vulns = await crud.crud_vulnerability.get_multi(
        db, where=condition)
    if len(vulns) != 3:
        reflected_xss = schemas.VulnerabilityCreate(
            id=1,
            name="Reflected XSS",
            description="Reflected Cross-Site Scripting (XSS) vulnerabilities occur when unvalidated user input is directly included in a webpage and is immediately returned by the server in an error message, search result, or any other response that includes some or all of the input provided by the user. This type of vulnerability is called \"reflected\" because the server reflects the malicious script back to the user's browser. The user unknowingly runs the script in their own browser, which can lead to various harmful outcomes.",
            type_id=8,  # XSS
            patch_suggestion="Implement proper input validation and sanitization. User-provided data should never be used directly in the generation of the webpage without ensuring it's secure. A common method is to HTML-encode user input so that potentially harmful characters are made safe. Additionally, consider implementing a robust Content Security Policy (CSP) to mitigate the impact of any potential XSS attacks.",
            severity_level_id=7  # HIGH
        )
        await crud.crud_vulnerability.create(db, obj_in=reflected_xss)
        stored_xss = schemas.VulnerabilityCreate(
            id=2,
            name="Stored XSS",
            description="Stored Cross-Site Scripting (XSS) vulnerabilities occur when malicious user input is stored on the target server (e.g., in a database, message forum, visitor log, comment field, etc.) and later served to users. When other users load affected pages, the malicious script executes, typically leading to unauthorized access, cookie theft, or other harmful effects.",
            type_id=8,  # XSS
            patch_suggestion="Similar to reflected XSS, input validation and sanitization are key. Stored data that originated from users should be treated as potentially harmful and HTML-encoded or otherwise sanitized before being served to users. You should also be cautious with user-generated files or content. CSP is also beneficial in this scenario.",
            severity_level_id=7  # HIGH
        )
        await crud.crud_vulnerability.create(db, obj_in=stored_xss)
        DOM_xss = schemas.VulnerabilityCreate(
            id=3,
            name="DOM XSS",
            description="Document Object Model Cross-Site Scripting (DOM XSS) vulnerabilities occur when a script manipulates the page's DOM in an unsafe way. The page's script itself can be safe, but if it interacts with the DOM without properly sanitizing user input, it can inadvertently allow the user to inject executable code. As the malicious payload is executed as a result of modifying the DOM \"on the fly,\" it's possible for the payload to be never sent to the server, making it a client-side attack.",
            type_id=8,  # XSS
            patch_suggestion="To mitigate DOM XSS, use element.textContent instead of element.innerHTML when manipulating DOM elements with user-provided data. When you need to dynamically create HTML, consider using safer methods like element.setAttribute or element.createElement. Avoid using dangerous JavaScript functions like eval(), document.write(), and innerHTML as they can introduce DOM XSS if used with untrusted data. Also, be sure to apply proper output encoding when inserting user-controlled data into the page.",
            severity_level_id=6  # MEDIUM
        )
        await crud.crud_vulnerability.create(db, obj_in=DOM_xss)


async def init() -> None:
    async with AsyncSessionLocal() as db:
        await init_admin(db)
        await init_user(db)
        await init_lookup_status(db)
        await init_lookup_severity(db)
        await init_lookup_vulnerability_type(db)
        await init_xss_vulnerability(db)


async def main() -> None:
    logger.info("Creating initial data")
    await init()
    logger.info("Initial data created")

if __name__ == "__main__":
    asyncio.run(main())
