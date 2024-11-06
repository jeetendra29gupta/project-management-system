from datetime import datetime
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from database import get_db
from main_app import app
from models import ProjectManagementSystem


@pytest.fixture
def mock_db_session():
    # Create a mock for the database session
    mock_db = MagicMock()
    yield mock_db


@pytest.fixture
def client(mock_db_session):
    app.dependency_overrides[get_db] = lambda: mock_db_session
    client = TestClient(app)
    return client


# Create Project Tests --> Positive Test Case
def test_create_project(client, mock_db_session):
    project_data = {
        "project_name": "New Project",
        "project_description": "A test project",
        "project_start_date": "2024-11-01T00:00:00",
        "project_end_date": "2024-12-01T00:00:00",
    }

    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = None

    response = client.post("/projects/", json=project_data)

    assert response.status_code == 201
    assert "Project created successfully. Project ID" in response.json()["message"]
    assert response.json()["project"]["project_name"] == "New Project"


# Create Project Tests --> Negative Test Case
def test_create_project_error(client):
    # Invalid project name (empty string)
    project_data = {
        "project_description": "A test project",
        "project_start_date": "2024-11-01T00:00:00",
        "project_end_date": "2024-12-01T00:00:00",
    }

    response = client.post("/projects/", json=project_data)
    # Validation error due to empty project_name
    assert response.status_code == 422


# Create Project Tests --> Test Invalid Date Format
def test_create_project_invalid_date_format(client):
    # Invalid date format
    invalid_data = {
        "project_name": "Invalid Date Project",
        "project_description": "Project with invalid date",
        "project_start_date": "invalid-date",
        "project_end_date": "2024-12-12T00:00:00"
    }

    response = client.post("/projects/", json=invalid_data)
    # Unprocessable Entity
    assert response.status_code == 422


# Get All Projects Tests --> Positive Test Case
def test_get_all_projects(client, mock_db_session):
    mock_db_session.query().all.return_value = [
        ProjectManagementSystem(id=1, project_name="Project 1", project_description="Description",
                                project_start_date=datetime(2024, 11, 1), project_end_date=datetime(2024, 12, 1)),
        ProjectManagementSystem(id=2, project_name="Project 2", project_description="Description",
                                project_start_date=datetime(2024, 11, 1), project_end_date=datetime(2024, 12, 1)),
    ]

    response = client.get("/projects/")

    assert response.status_code == 200
    assert len(response.json()["projects"]) == 2
    assert "Successfully fetched the list of projects." in response.json()["message"]


# Get All Projects Tests --> Negative Test Case
def test_get_all_projects_error(client, mock_db_session):
    mock_db_session.query().all.side_effect = Exception("Database error")

    response = client.get("/projects/")
    assert response.status_code == 500
    assert "Unable to retrieve projects at the moment." in response.json()["detail"]


# Get All Projects Tests --> Test Get All Projects with Empty Database
def test_get_all_projects_empty_db(client, mock_db_session):
    mock_db_session.query().all.return_value = []

    response = client.get("/projects/")

    assert response.status_code == 200
    assert "Successfully fetched the list of projects." in response.json()["message"]
    # No projects returned
    assert len(response.json()["projects"]) == 0


# Get Project by ID Tests --> Positive Test Case
def test_get_project_by_id(client, mock_db_session):
    project = ProjectManagementSystem(id=1, project_name="Project 1", project_description="Description",
                                      project_start_date=datetime(2024, 11, 1), project_end_date=datetime(2024, 12, 1))
    mock_db_session.query().filter().first.return_value = project

    response = client.get("/projects/1")

    assert response.status_code == 200
    assert response.json()["project"]["project_name"] == "Project 1"
    assert "Project with ID 1 retrieved successfully." in response.json()["message"]


# Get Project by ID Tests --> Negative Test Case (Project Not Found)
def test_get_project_by_id_not_found(client, mock_db_session):
    mock_db_session.query().filter().first.return_value = None

    response = client.get("/projects/999")

    assert response.status_code == 404
    assert "Project with ID 999 not found." in response.json()["detail"]


# Get Project by ID Tests --> Negative Test Case (Database Error)
def test_get_project_by_id_error(client, mock_db_session):
    mock_db_session.query().filter().first.side_effect = Exception("Database error")

    response = client.get("/projects/1")

    assert response.status_code == 500
    assert "An unexpected error occurred while fetching the project." in response.json()["detail"]


# Update Project Tests --> Positive Test Case
def test_update_project(client, mock_db_session):
    project_data = {
        "project_name": "Updated Project Name",
        "project_description": "Updated Description",
        "project_start_date": "2024-11-15T00:00:00",
        "project_end_date": "2024-12-15T00:00:00",
    }

    project = ProjectManagementSystem(id=1, project_name="Old Project", project_description="Old Description",
                                      project_start_date=datetime(2024, 11, 1), project_end_date=datetime(2024, 12, 1))
    mock_db_session.query().filter().first.return_value = project

    response = client.put("/projects/1", json=project_data)

    assert response.status_code == 200
    assert "Project with ID 1 updated successfully." in response.json()["message"]
    assert response.json()["project"]["project_name"] == "Updated Project Name"


# Update Project Tests --> Negative Test Case (Project Not Found)
def test_update_project_not_found(client, mock_db_session):
    project_data = {
        "project_name": "Updated Project Name",
        "project_description": "Updated Description",
        "project_start_date": "2024-11-15T00:00:00",
        "project_end_date": "2024-12-15T00:00:00",
    }

    mock_db_session.query().filter().first.return_value = None

    response = client.put("/projects/999", json=project_data)

    assert response.status_code == 404
    assert "Failed to update project with ID 999." in response.json()["detail"]


# Update Project Tests --> Negative Test Case (Database Error)
def test_update_project_error(client, mock_db_session):
    project_data = {
        "project_name": "Updated Project Name",
        "project_description": "Updated Description",
        "project_start_date": "2024-11-15T00:00:00",
        "project_end_date": "2024-12-15T00:00:00",
    }

    mock_db_session.query().filter().first.side_effect = Exception("Database error")

    response = client.put("/projects/1", json=project_data)

    assert response.status_code == 500
    assert "Failed to update project with ID 1. Please verify the data and try again." in response.json()["detail"]


# Delete Project Tests --> Positive Test Case
def test_delete_project(client, mock_db_session):
    project = ProjectManagementSystem(id=1, project_name="Project to Delete", project_description="Description",
                                      project_start_date=datetime(2024, 11, 1), project_end_date=datetime(2024, 12, 1))
    mock_db_session.query().filter().first.return_value = project

    response = client.delete("/projects/1")

    assert response.status_code == 200
    assert "Project with ID 1 deleted successfully." in response.json()["message"]


# Delete Project Tests --> Negative Test Case (Project Not Found)
def test_delete_project_not_found(client, mock_db_session):
    mock_db_session.query().filter().first.return_value = None

    response = client.delete("/projects/999")

    assert response.status_code == 404
    assert "Unable to delete project with ID 999. Please try again later." in response.json()["detail"]


# Delete Project Tests --> Negative Test Case (Database Error)
def test_delete_project_error(client, mock_db_session):
    mock_db_session.query().filter().first.side_effect = Exception("Database error")

    response = client.delete("/projects/1")

    assert response.status_code == 500
    assert "Unable to delete project with ID 1. Please try again later." in response.json()["detail"]
