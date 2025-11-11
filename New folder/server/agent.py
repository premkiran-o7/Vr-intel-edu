# agent.py
from typing import Dict, Any
from pydantic import BaseModel
from secrets import load_env

# Try/except guard so import-time errors are clearer in dev
try:
    from langchain_groq import ChatGroq
    from langchain.schema import HumanMessage, SystemMessage
except Exception as e:
    # If you don't have langchain_groq installed during quick local edits,
    # this makes the error clearer rather than failing with an ImportError stack trace later.
    ChatGroq = None  # type: ignore
    HumanMessage = None  # type: ignore
    SystemMessage = None  # type: ignore
    _IMPORT_ERROR = e  # keep for debugging

class StoryAgent:
    """
    Minimal StoryAgent that:
      - Initializes the Groq LLaMA model via LangChain
      - Provides: status text, short chat generation, and builds scene-event JSON payloads
    """

    def __init__(self, model_name: str = "llama3-70b"):
        groq_key = load_env()
        if ChatGroq is None:
            raise RuntimeError(
                "langchain_groq (or dependent packages) not available. Import error: "
                f"{getattr(globals(), '_IMPORT_ERROR', 'unknown')}"
            )

        # Initialize the model client (lightweight wrapper used by agent)
        self.llm = ChatGroq(model=model_name, groq_api_key=groq_key)

        # A short system prompt to keep responses consistent
        self.system_prompt = (
            "You are the backend story agent for a kid-friendly Godot storytelling project. "
            "Keep messages short, friendly, and clear. When asked for status, confirm work-in-progress "
            "and say integration with Godot scenes is upcoming."
        )

    def status_message(self) -> str:
        """Return a short human-friendly status (static, safe fallback)."""
        return (
            "We’re still working on the story server. "
            "Soon this agent will send JSON scene events directly to Godot to control scenes and narration."
        )

    def chat_reply(self, user_input: str) -> str:
        """
        Use the LLM to craft a short reply. If LLM not available or errors, fall back to a status message.
        """
        try:
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=f"User: {user_input}\n\nReply briefly as the Story Agent:"),
            ]
            res = self.llm.invoke(messages)
            return getattr(res, "content", str(res))  # res.content is expected
        except Exception:
            # graceful fallback
            return self.status_message()

    def build_scene_event(
        self,
        event_id: str = "evt-000",
        scene_type: str = "scene_update",
        dialogue: str = None,
        choices: list = None,
        emotion_tag: str = "neutral",
    ) -> Dict[str, Any]:
        """
        Build the canonical event JSON that Godot will consume.

        Keep fields optional and minimal. Godot will ignore unknown keys.
        """
        # Default dialogue if none provided
        dialogue = dialogue or "We’re still building the live integration. Scenes will be available soon."
        choices = choices or []

        event = {
            "id": event_id,
            "type": scene_type,
            "bg": "forest_day.png",
            "left": {"sprite": "tortoise_idle.png", "pos": [120, 250], "emotion": "calm"},
            "right": {"sprite": "hare_idle.png", "pos": [420, 250], "emotion": "arrogant"},
            "dialogue": dialogue,
            "tts": {"voice": "sara-child", "rate": 0.95},
            "choices": choices,
            "delay": 2.5,
            "metadata": {"emotion_tag": emotion_tag, "difficulty": "easy"},
        }

        return event


# Provide a singleton agent instance for easy importing
_agent_instance: StoryAgent = None

def get_agent() -> StoryAgent:
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = StoryAgent()
    return _agent_instance
