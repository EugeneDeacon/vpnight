from sqlalchemy import Integer, String
from sqlalchemy.orm import declarative_base, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import TIMESTAMP

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True, autoincrement=False)
    first_name = mapped_column(String(64), nullable=True)
    last_name = mapped_column(String(120), nullable=True)
    username = mapped_column(String(120), nullable=True)
    language_code = mapped_column(String(2), nullable=True)

    created_at = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now()
    )
