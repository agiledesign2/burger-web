from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from datetime import datetime

from configs.Database import engine

# Base Entity Model Schema
EntityMeta = declarative_base()


def init():
    EntityMeta.metadata.create_all(bind=engine)
    
class BaseModel():
    __allow_unmapped__ = True

    # id: int = Field(primary_key=True)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = Column(
        DateTime(timezone=True), onupdate=func.now()
    )
    
"""
from sqlalchemy import Column, DateTime, text
from sqlalchemy.sql import func
from sqlmodel import Field, SQLModel

class BaseModel(SQLModel):
    id: int = Field(primary_key=True)
    created_at: datetime = Field(sa_column=Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    ))
    updated_at: datetime = Field(sa_column=Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP")
    ))
"""
