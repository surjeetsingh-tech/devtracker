from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped,mapped_column, relationship
from app.database import Base

class User(Base):
    __tablename__= "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    tasks: Mapped[list["Task"]] = relationship(back_populates="owner", cascade="all, delete-orphan")


class Task(Base):
    __tablename__= "tasks"

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title : Mapped[str] = mapped_column(String(200), nullable=False)
    description : Mapped[str] = mapped_column(String(500), nullable=True)
    status : Mapped[str] = mapped_column(String(20), default="pending")
    github_link : Mapped[str] = mapped_column(String(250), nullable=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    owner : Mapped["User"] = relationship(back_populates="tasks")



