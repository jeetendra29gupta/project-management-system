from datetime import date
from typing import Optional

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    project_name: str
    project_description: str
    project_start_date: date
    project_end_date: date


class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    project_description: Optional[str] = None
    project_start_date: Optional[date] = None
    project_end_date: Optional[date] = None
