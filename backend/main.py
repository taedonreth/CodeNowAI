from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from dotenv import load_dotenv
import os
import anthropic

# Load environment variables from .env
load_dotenv()

# Initialize Anthropic client with API key
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Initialize FastAPI app
app = FastAPI()

# Allow frontend to interact with backend (CORS setup)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL (e.g., http://localhost:3000)
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

# Define the request body schema for /chat
class ChatRequest(BaseModel):
    query: str

# Chat endpoint with Anthropic Claude integration
@app.post("/chat")
def chat(request: ChatRequest):
    try:
        query = request.query
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",  # Replace with your available model
            max_tokens=1024,
            messages=[
                {"role": "user", "content": query}  # Pass the user query
            ]
        )

        return {"response": response.content}  # Access the `content` attribute directly

    except Exception as e:
        return {"error": str(e)}


# Run the app using: uvicorn backend.main:app --reload
