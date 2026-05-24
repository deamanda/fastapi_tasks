from sqlalchemy import Column, Date, Integer, String

from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    hashed_password = Column(String(255))
    created_at = Column(Date)
