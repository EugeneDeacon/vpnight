from sqlalchemy import BigInteger, String, TIMESTAMP, ForeignKey, Numeric
from sqlalchemy.orm import mapped_column, relationship, Mapped, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    first_name: Mapped[str] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str] = mapped_column(String(120), nullable=True)
    username: Mapped[str] = mapped_column(String(120), nullable=True)
    language_code: Mapped[str] = mapped_column(String(2), nullable=True)

    balance: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0.00)

    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    referrer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)

    referrals: Mapped[list["User"]] = relationship(
        "User",
        back_populates="referrer",
        cascade="all, delete-orphan"
    )

    referrer: Mapped["User"] = relationship(
        "User",
        remote_side=[id],
        back_populates="referrals"
    )
