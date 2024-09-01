from sqlalchemy import Column, String, Integer, Boolean, DateTime, func

from src.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(48), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=func.now())
    password_hash = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f'id: {self.id}, username: {self.username}'
