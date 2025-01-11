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
    allow_origins=["http://localhost:3000"],
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

@app.post("/chat_resume")
def chat_resume():
    try:
        # Read the project details from tic-tac-toe.json
        with open("backend/repos/tic-tac-toe.json", "r") as f:
            project_details = json.load(f)

        system_prompt = """You are a professional resume writer. When given project details, create:
1. A tech stack list
2. Three strong resume bullet points that:
   - Start with different action verbs (e.g., developed, implemented, optimized)
   - Include metrics when possible
   - Show impact
   - Are maximum 120 characters each
Format the response exactly as:
Tech Stack: [technologies]
Resume Bullet Points:
- [bullet 1]
- [bullet 2]
- [bullet 3]"""

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": str(project_details)}
            ]
        )

        return {"response": response.content}

    except FileNotFoundError:
        return {"error": "tic-tac-toe.json file not found"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in tic-tac-toe.json"}
    except Exception as e:
        return {"error": str(e)}
    
# Run the app using: uvicorn backend.main:app --reload
