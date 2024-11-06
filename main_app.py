import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from models import init_db
from projects_routes import projects_router

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the database
init_db()


@app.get("/", response_model=dict, status_code=status.HTTP_200_OK)
async def index() -> dict:
    """Welcome endpoint.

    Returns:
        dict: A welcome message for the Pizza Delivery API.
    """
    return {
        "message": "Welcome to the Project Management System API!",
    }


app.include_router(projects_router)

if __name__ == '__main__':
    uvicorn.run("main_app:app", host="0.0.0.0", port=8181, reload=True)
