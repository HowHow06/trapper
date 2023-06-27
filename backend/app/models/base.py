from datetime import datetime
from typing import Optional

from sqlalchemy import text
from sqlmodel import Field, SQLModel


class TimestampModel(SQLModel):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("(CURRENT_TIMESTAMP)")
        }
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        }
    )

    deleted_at: Optional[datetime] = Field(default=None)
