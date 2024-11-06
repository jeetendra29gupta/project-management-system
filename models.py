from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from database import engine

Base = declarative_base()


class ProjectManagementSystem(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, index=True)
    project_description = Column(String)
    project_start_date = Column(Date)
    project_end_date = Column(Date)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def to_dict(self):
        """Convert SQLAlchemy model instance to a dictionary."""

        return {
            "id": self.id,
            "project_name": self.project_name,
            "project_description": self.project_description,
            "project_start_date": self.project_start_date,
            "project_end_date": self.project_end_date,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None
        }


def init_db():
    Base.metadata.create_all(bind=engine)
