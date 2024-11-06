import logging
from datetime import datetime

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from log_config import setup_logging
from schemas import ProjectCreate, ProjectUpdate
from services import create_project_service
from services import delete_project_service
from services import get_projects_service, get_project_by_id_service
from services import update_project_service

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize the router
projects_router = APIRouter(
    prefix="/projects",
    tags=['projects']
)


@projects_router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    try:
        created_project = create_project_service(db=db, project=project)
        return {
            "message": f"Project created successfully. Project ID: {created_project.id}.",
            "project": created_project.to_dict(),
            "date_time": datetime.now().isoformat(),
        }
    except HTTPException as e:
        # Reraise the exception that was raised in the service
        raise e
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create the project. Please verify the data and try again.",
        )


@projects_router.get("/", response_model=dict, status_code=status.HTTP_200_OK)
async def get_projects(db: Session = Depends(get_db)):
    try:
        projects = get_projects_service(db=db)
        return {
            "message": "Successfully fetched the list of projects.",
            "projects": [project.to_dict() for project in projects],
            "date_time": datetime.now().isoformat(),
        }
    except HTTPException as e:
        # Reraise the exception that was raised in the service
        raise e
    except Exception as e:
        logger.error(f"Error fetching projects: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve projects at the moment. Please try again later.",
        )



@projects_router.get("/{project_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def get_project_by_id(project_id: int, db: Session = Depends(get_db)):
    try:
        project = get_project_by_id_service(db=db, project_id=project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with ID {project_id} not found. Please ensure the ID is correct and try again.",
            )
        return {
            "message": f"Project with ID {project_id} retrieved successfully.",
            "project": project.to_dict(),
            "date_time": datetime.now().isoformat(),
        }
    except HTTPException as e:
        # Reraise the exception that was raised in the service
        raise e
    except Exception as e:
        logger.error(f"Error fetching project with ID {project_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the project. Please try again later.",
        )


@projects_router.put("/{project_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)):
    try:
        updated_project = update_project_service(db=db, project_id=project_id, project=project)
        if not updated_project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Failed to update project with ID {project_id}. Please verify the data and try again.",
            )
        return {
            "message": f"Project with ID {project_id} updated successfully.",
            "project": updated_project.to_dict(),
            "date_time": datetime.now().isoformat(),
        }
    except HTTPException as e:
        # Reraise the exception that was raised in the service
        raise e
    except Exception as e:
        logger.error(f"Error updating project with ID {project_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update project with ID {project_id}. Please verify the data and try again.",
        )


@projects_router.delete("/{project_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    try:
        success = delete_project_service(db=db, project_id=project_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unable to delete project with ID {project_id}. Please try again later.",
            )
        return {
            "message": f"Project with ID {project_id} deleted successfully.",
            "date_time": datetime.now().isoformat(),
        }
    except HTTPException as e:
        # Reraise the exception that was raised in the service
        raise e
    except Exception as e:
        logger.error(f"Error deleting project with ID {project_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to delete project with ID {project_id}. Please try again later.",
        )
