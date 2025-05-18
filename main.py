import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from crewai import Agent, Task, Crew

os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "")

# Define agent
chat_agent = Agent(
    role="Conversationalist",
    goal="Chat with users and answer questions helpfully.",
    backstory="You are a helpful and knowledgeable AI assistant.",
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

    # Define a Task for this chat message
    task = Task(
        description=user_message,
        agent=chat_agent,
        expected_output="A helpful, conversational response."
    )

    # Run the Crew (even if it's just one agent+task)
    crew = Crew(
        agents=[chat_agent],
        tasks=[task],
        verbose=True,
    )
    result = crew.kickoff()
    reply_text = str(result) if isinstance(result, str) else result.final_output
    return JSONResponse({"reply": reply_text})

