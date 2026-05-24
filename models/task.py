from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String

from database import Base


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(255))
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    due_date = Column(Date)
    owner_id = Column(
        Integer,
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False)
