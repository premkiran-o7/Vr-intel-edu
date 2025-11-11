# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from agent import get_agent

app = FastAPI(title="VR Storytelling — Story Agent API", version="0.1.0")
agent = get_agent()


class ChatRequest(BaseModel):
    user_input: Optional[str] = ""


class ChatResponse(BaseModel):
    agent_reply: str


class EventRequest(BaseModel):
    event_id: Optional[str] = "evt-000"
    dialogue: Optional[str] = None
    choices: Optional[List[Dict[str, Any]]] = []


@app.get("/")
def root():
    return {"message": "Story Agent API running. Use /status, /chat or /event"}


@app.get("/status")
def status():
    """
    Quick health/status endpoint (human-friendly).
    """
    return {"status": "ok", "message": agent.status_message()}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    Ask the agent a short question — the agent will reply (via LLM if available)
    """
    try:
        reply = agent.chat_reply(req.user_input or "status")
        return ChatResponse(agent_reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/event")
def event(req: EventRequest):
    """
    Return a JSON event payload describing a scene update / action.
    Godot can POST to this endpoint (or we can push via WebSocket later),
    then consume this JSON to update the scene.
    """
    try:
        payload = agent.build_scene_event(
            event_id=req.event_id,
            dialogue=req.dialogue,
            choices=req.choices,
        )
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
