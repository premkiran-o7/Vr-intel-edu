# Vr-intel-edu

Download godot from [here](https://godotengine.org/download/windows), the one above


You will get two:
- Godot_v4.5.1-stable_win64_console.exe
- Godot\Godot_v4.5.1-stable_win64.exe


this Godot\Godot_v4.5.1-stable_win64.exe creates a applicationa nd can open the app with this

screen for project selection will be there 

select this
`New folder\tortoise-and-hare-scene`


Then There will be `Project` above 
Go there then

> Project settings
> Run (second option)
> select main scene 

There will be a scene named story_controller.tscn , select that

In the bottom left space click on that file and press Function6 (F6)


All the scenes will be in scenes folder in the bottom left panel

Click on AnimPlayer on the top left panel after selecting a scene 


In teh bottom there will be output debug Animation

After clicking animation, teher will be a small bar which has animations, select them and click pay






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

```

  ┌───────────────────────────────┐
  │        LangGraph Agent        │
  │  (Generates story events)     │
  └──────────────┬────────────────┘
                 │ JSON (actions)
                 │
  ...............▼.................................
  :             FastAPI Bridge                     :
  :  (Receives events, exposes API)                :
  :................................................:
                 │ HTTP / WebSocket
                 │
  ┌──────────────▼────────────────┐
  │          Godot Engine         │
  │  - HTTP Listener (main.gd)    │
  │  - Scene Manager (2D/VR)      │
  └──────────────┬────────────────┘
                 │ Visual / Audio Output
                 │
        ┌────────▼────────┐
        │     VR User     │
        │ (Headset View)  │
        └─────────────────┘
```

```
  Start
    │
    ▼
  Load Story JSON
    │
    ▼
  Initialize FastAPI + Godot Listener
    │
    ▼
  LangGraph Reads Event
    │
    ▼
  Send Event → FastAPI (/update_scene)
    │
    ▼
  Godot Fetches Event (/get_event)
    │
    ▼
  Interpret Action (move / color / speak)
    │
    ▼
  Update Scene Objects
    │
    ▼
  Render Scene in VR
    │
    ├──► More Events? ──► Yes → Loop Back
    │
    └──► No → End

```



