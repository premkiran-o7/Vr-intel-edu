# agent.py
from typing import Dict, Any
from pydantic import BaseModel
from server.secrets import load_env


from langchain.chat_models import init_chat_model
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.system import SystemMessage


class StoryAgent:
    """
    Minimal StoryAgent that:
      - Initializes the Groq LLaMA model via LangChain
      - Provides: status text, short chat generation, and builds scene-event JSON payloads
    """

    def __init__(self, model_name: str = "llama3-70b"):
        groq_key = load_env()
        

        # Initialize the model client (lightweight wrapper used by agent)
        self.llm = init_chat_model(model="openai/gpt-oss-20b", groq_api_key=groq_key, model_provider="groq")

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
    context: str = None,
    emotion_tag: str = "neutral",
) -> Dict[str, Any]:
    """
    Build a dynamic event JSON using LLM output for dialogue and choices.
    Godot will consume this for scene rendering.

    The LLM response is expected to include 'dialogue' and optionally 'choices'.
    """

    # Prepare the LLM prompt
    prompt = f"""
    You are generating a narrative scene event for a game.

    Context:
    {context or "A short story involving a hare and a tortoise."}

    Task:
    - Generate a short, emotionally expressive dialogue for this scene.
    - Optionally suggest 2–3 player choices if relevant.
    - Each choice should be concise and advance the story logically.
    - Return only valid JSON with fields 'dialogue' and 'choices'.
    - Example:
      {{
        "dialogue": "The hare laughs: 'You’ll never beat me!'",
        "choices": ["Challenge him", "Ignore him and start running"]
      }}
    """

    try:
        res = self.llm.invoke(prompt)
        llm_output = res.get("output", res) if isinstance(res, dict) else res

        # Parse JSON if returned as string
        if isinstance(llm_output, str):
            import json
            llm_output = json.loads(llm_output)

        dialogue = llm_output.get("dialogue", "The story continues...")
        choices = llm_output.get("choices", [])

    except Exception as e:
        # Fallback to dummy values if LLM fails
        dialogue = f"An error occurred while generating scene: {str(e)}"
        choices = []

    # Construct event structure
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
