from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from src.auth.models import User
from src.database import Base


class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(68), nullable=False, default="report")
    image = Column(String, nullable=False)
    report = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    create_at = Column(DateTime, default=func.now())

    user = relationship("User", foreign_keys="Report.user_id")

    def __repr__(self):
        return f"id: {self.id}, owner: {self.user_id}"
