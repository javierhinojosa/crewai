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

    task = Task(
        description=user_message,
        agent=chat_agent,
        expected_output="A helpful, conversational response."
    )

    crew = Crew(
        agents=[chat_agent],
        tasks=[task],
        verbose=True,
    )
    result = crew.kickoff()
    # Robust extraction of the response
    if hasattr(result, "output"):
        reply_text = result.output
    elif hasattr(result, "result"):
        reply_text = result.result
    else:
        reply_text = str(result)
    return JSONResponse({"reply": reply_text})
