import logging

from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from log_config import setup_logging
from models import ProjectManagementSystem
from schemas import ProjectCreate, ProjectUpdate

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)


def create_project_service(db: Session, project: ProjectCreate):
    try:
        db_project = ProjectManagementSystem(
            project_name=project.project_name,
            project_description=project.project_description,
            project_start_date=project.project_start_date,
            project_end_date=project.project_end_date,
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    except Exception as e:
        logger.error(f"Error in create_project_service: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create the project. Please verify the data and try again.",
        )


def get_projects_service(db: Session):
    try:
        return db.query(ProjectManagementSystem).all()
    except Exception as e:
        logger.error(f"Error in get_projects_service: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve projects at the moment. Please try again later.",
        )


def get_project_by_id_service(db: Session, project_id: int):
    try:
        return db.query(ProjectManagementSystem).filter(ProjectManagementSystem.id == project_id).first()
    except Exception as e:
        logger.error(f"Error in get_project_by_id_service for project ID {project_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the project. Please try again later.",
        )


def update_project_service(db: Session, project_id: int, project: ProjectUpdate):
    try:
        db_project = get_project_by_id_service(db=db, project_id=project_id)
        if not db_project:
            return None
        if project.project_name:
            db_project.project_name = project.project_name
        if project.project_description:
            db_project.project_description = project.project_description
        if project.project_start_date:
            db_project.project_start_date = project.project_start_date
        if project.project_end_date:
            db_project.project_end_date = project.project_end_date
        db.commit()
        db.refresh(db_project)
        return db_project
    except Exception as e:
        logger.error(f"Error in update_project_service for project ID {project_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update project with ID {project_id}. Please verify the data and try again.",
        )


def delete_project_service(db: Session, project_id: int):
    try:
        db_project = get_project_by_id_service(db=db, project_id=project_id)
        if not db_project:
            return False
        db.delete(db_project)
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Error in delete_project_service for project ID {project_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to delete project with ID {project_id}. Please try again later.",
        )
