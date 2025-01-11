from fastapi import FastAPI, Query, HTTPException
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


def load_all_projects(repo_directory="repos"):
    """
    Load all JSON files from the given directory into a list of projects.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    repo_directory = os.path.join(current_dir, "repos")

    if not os.path.exists(repo_directory):
        raise FileNotFoundError(f"The directory {repo_directory} does not exist.")

    projects = []
    for filename in os.listdir(repo_directory):
        if filename.endswith(".json"):
            with open(os.path.join(repo_directory, filename), "r") as f:
                projects.append(json.load(f))
    return projects


@app.get("/search")
def search_projects(keywords: str = Query(...)):
    """
    Search for projects based on user input keywords.
    Accepts a comma-separated string of keywords.
    """
    user_input = [k.strip().lower() for k in keywords.split(",")]
    projects = load_all_projects()

    matching_projects = [
        project for project in projects
        if any(keyword in [k.lower() for k in project["keywords"]] for keyword in user_input)
    ]

    if not matching_projects:
        raise HTTPException(status_code=404, detail="No matching projects found.")

    return {"matches": matching_projects}


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to CodeNowAI API"}


# Define the request body schema for /chat
class ChatRequest(BaseModel):
    query: str


@app.post("/chat")
def chat(request: ChatRequest):
    """
    Chat endpoint using Anthropic Claude integration.
    Pass the user query and return the AI response.
    """
    try:
        query = request.query
        response = client.completions.create(
            model="claude-2",  # Replace with the correct Anthropic model name
            max_tokens_to_sample=1024,
            prompt=f"{anthropic.HUMAN_PROMPT} {query}{anthropic.AI_PROMPT}"
        )

        return {"response": response["completion"]}  # Return the completion content

    except Exception as e:
        return {"error": str(e)}


# Run the app using: uvicorn main:app --reload
