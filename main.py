import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from crewai import Agent

# Set your OpenAI key in the environment for CrewAI to use
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "")

# Define a simple CrewAI agent
chat_agent = Agent(
    role="Conversationalist",
    goal="Help users by chatting with them in a friendly, informative way.",
    backstory="You are a helpful, knowledgeable AI agent always available to chat.",
    verbose=True,
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html") as f:
        return HTMLResponse(f.read())

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    # Use CrewAI agent to generate a reply
    reply = chat_agent.chat(user_message)
    return JSONResponse({"reply": reply})
