from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Allow frontend to interact with backend (CORS setup)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with frontend URL (e.g., http://localhost:3000)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to CodeNowAI API"}

# Load project data (example route for projects)
@app.get("/projects")
def get_projects():
    with open("backend/repos/todo_list.json", "r") as f:
        projects = json.load(f)
    return {"projects": [projects]}

# Chat functionality placeholder
@app.post("/chat")
def chat(query: str):
    # Placeholder logic, replace with OpenAI integration later
    return {"response": f"You asked: {query}. Chat functionality coming soon!"}

# Run the app: uvicorn backend.main:app --reload
