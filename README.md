# Vr-intel-edu


Goal : Build a **VR-ready 2D storytelling system** for children — where a **LangGraph agent** in Python drives animations, character attributes, and scenes inside **Godot** through a **FastAPI bridge**.

| Layer             | Tool                                 | Purpose                                        |
| ----------------- | ------------------------------------ | ---------------------------------------------- |
| **Engine**        | **Godot 4.3+**                       | 2D/3D + VR support (OpenXR official plugin)    |
| **Backend**       | **FastAPI**                          | Communication bridge between LangGraph & Godot |
| **Logic**         | **LangGraph**                        | Story orchestration, object/scene control      |
| **Audio/Visuals** | Free2D / OpenGameArt / Kenney Assets | Sprites, sounds, environment art               |
| **Communication** | **WebSocket / HTTP (JSON)**          | Real-time AI → Engine event sync               |
| **VR Layer**      | OpenXR plugin (Meta Quest / PCVR)    | Immersive display and controls                 |



| Phase                                   | Goal                                         | Key Tasks                                          |
| --------------------------------------- | -------------------------------------------- | -------------------------------------------------- |
| **Phase 1 – Base Scene Setup**          | Create Godot 2D scene (forest, turtle, hare) | Build main_scene.tscn, add basic animation         |
| **Phase 2 – LangGraph Story Generator** | Output JSON story data                       | Build Python agent that emits event sequences      |
| **Phase 3 – Godot-Python Bridge**       | Send updates live (optional WebSocket)       | Use Godot HTTPRequest or Python socket             |
| **Phase 4 – Dynamic Animation**         | Animate based on agent data                  | Implement `move_character` and `dialogue` handlers |
| **Phase 5 – Narration**                 | Integrate TTS for voiceover                  | Generate `.wav` per dialogue, play in Godot        |
| **Phase 6 – Video Export & Polishing**  | Record scenes as lessons                     | Add transitions, titles, moral text overlays       |




