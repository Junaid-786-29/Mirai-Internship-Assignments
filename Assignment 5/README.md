# 🌌 AI VISUAL NOVEL (MULTIMODAL ENGINE) - Assignment 5

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│  SESSION ID : MIRAI-ASSIGNMENT-05              BUILD  : v5.0.0-RELEASE       │
│  ENGINES    : Groq (Llama 3.3 70B) + Pollinations (Flux) + gTTS Narration    │
│  PIPELINE   : Text Narrative ➔ Image Synthesis ➔ Voice Narration             │
│  RUNTIME    : Python 3.8+ / Streamlit          STATUS : [ ONLINE / ACTIVE ]  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 💻 SYSTEM INFO

```text
       /\_/\          user@mirai-workstation:~/Assignment-5
      ( o.o )         -------------------------------------
       > ^ <          PROJECT   : Multimodal AI Visual Novel
                      TRACK     : MirAI Virtual Summer Internship 2026
                      MODULE    : Multimodal AI Orchestration (LLM + CV + TTS)
                      LLM CORE  : llama-3.3-70b-versatile (Groq Cloud)
                      IMAGE GEN : Pollinations AI (Flux Model / 832x468)
                      VOICE TTS : gTTS (Google Text-to-Speech Engine)
                      CACHE DIR : ./assets/{images,audio}
                      STATUS    : ADVENTURE_ENGINE_READY
                      PORT      : 8501 (Default HTTP)
```

---

## ⚡ $ man ai-visual-novel

### 01. SYNOPSIS

```bash
$ ai-visual-novel --genre "<GENRE>" --art-style "<STYLE>" [--tts-enabled] [--auto-cache]
```

**AI Visual Novel** is a next-generation interactive storytelling platform that orchestrates **three distinct AI modalities** in real time:
1. **Narrative Engine**: Groq Cloud LLM generating structured second-person branching story scenarios.
2. **Visual Synthesis**: Pollinations AI (Flux) rendering custom cinematic widescreen scene art.
3. **Audio Narration**: gTTS synthesizing voice narration audio for each generated passage.

---

### 02. CORE CAPABILITIES

```text
[✓] TRIPLE-AI MULTIMODAL STACK ── Groq LLM + Pollinations Flux + gTTS Audio
[✓] STRICT JSON CONTRACT ──────── Reliable schema enforcement without markdown leaks
[✓] PERSISTENT LOCAL CACHING ──── Auto-saves images (.png) & audio (.mp3) to assets/
[✓] BRANCHING ADVENTURE TREE ──── Real-time choice generation altering story trajectories
[✓] CHRONOLOGICAL SCENE REPLAY ── Persistent visual novel log preserving choices & media
[✓] DYNAMIC GENRE & ART MATRIX ── 5 story genres x 5 cinematic art styles
[✓] IMMERSIVE GLASSMORPHISM UI ── Custom CSS dark-mode theme with Lora & Inter typography
```

---

### 03. GENRE & ART STYLE MATRIX

```text
  GENRES:    [ Fantasy ]   [ Horror ]      [ Sci-Fi ]     [ Mystery ]   [ Adventure ]
  STYLES:    [ Anime ]     [ Realistic ]   [ Watercolor ] [ Cyberpunk ] [ Pixel Art ]
```

| Genre Option | Typical Narrative Theme | Recommended Art Style Pairing |
| :--- | :--- | :--- |
| **Fantasy** | High magic, ancient ruins, mythical beings | *Watercolor* or *Anime* |
| **Horror** | Psychological tension, eerie gothic environments | *Realistic* or *Cyberpunk* |
| **Sci-Fi** | Futuristic megacities, orbital stations, AI | *Cyberpunk* or *Realistic* |
| **Mystery** | Detective noir, unsolved enigmas, cryptic clues | *Realistic* or *Watercolor* |
| **Adventure** | Expeditions, uncharted territories, lost relics | *Pixel Art* or *Anime* |

---

### 04. STRICT JSON DATA CONTRACT

The Groq narrator is governed by strict system prompts enforcing raw JSON output:

```json
{
  "story_text": "A 120-180 word immersive narrative passage written in second-person perspective.",
  "image_prompt": "Cinematic visual description (40+ words) detailing scene lighting, mood, foreground, background, and art tokens.",
  "options": [
    "Investigate the glowing glyph on the stone archway.",
    "Draw your blade and advance into the misty cavern.",
    "Retreat toward the river bank to find another route."
  ]
}
```

---

### 05. MULTIMODAL PIPELINE & CACHE FLOW

```text
               ┌──────────────────────────────────────────────┐
               │         User Selects Choice Option           │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
               ┌──────────────────────────────────────────────┐
               │ 1. Groq LLM Dispatch (llama-3.3-70b)         │
               │    - Ingests full dialogue history           │
               │    - Returns verified JSON scene schema      │
               └──────────────────────┬───────────────────────┘
                                      │
                     ┌────────────────┴────────────────┐
                     ▼                                 ▼
      ┌─────────────────────────────┐   ┌─────────────────────────────┐
      │ 2. Visual Synthesis Worker  │   │ 3. Voice TTS Audio Worker   │
      │    - Pollinations AI (Flux) │   │    - gTTS (Google TTS)      │
      │    - Check assets/images/   │   │    - Check assets/audio/    │
      │    - Save scene_XXX.png     │   │    - Save scene_XXX.mp3     │
      └──────────────┬──────────────┘   └──────────────┬──────────────┘
                     │                                 │
                     └────────────────┬────────────────┘
                                      ▼
               ┌──────────────────────────────────────────────┐
               │ 4. Streamlit Interactive Screen Assembly     │
               │    ├─ st.image(scene.png)                    │
               │    ├─ st.audio(scene.mp3)                    │
               │    ├─ Custom HTML/CSS Narrative Box          │
               │    └─ Interactive Action Buttons             │
               └──────────────────────────────────────────────┘
```

---

### 06. EXECUTION & SETUP GUIDE

```bash
# [Step 1] Navigate to Assignment 5 directory
cd "Assignment 5"

# [Step 2] Initialize and activate virtual environment
# Windows (PowerShell):
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS:
python3 -m venv venv
source venv/bin/activate

# [Step 3] Configure Environment Variables (.env)
# Create a .env file with your Groq API Key:
echo GROQ_API_KEY="your_groq_api_key_here" > .env

# [Step 4] Install multimodal dependencies
pip install -r requirements.txt

# [Step 5] Launch visual novel engine
streamlit run app.py
```

```text
  You can now view your Streamlit app in your browser.

  Local URL:    http://localhost:8501
  Network URL:  http://192.168.x.x:8501
```

---

### 07. DIRECTORY STRUCTURE

```text
Assignment 5/
├── 📁 assets/
│   ├── 📁 audio/          # Cached scene voice files (scene_001.mp3, ...)
│   └── 📁 images/         # Cached generated visuals (scene_001.png, ...)
├── 📄 .env                # Secret credentials (GROQ_API_KEY)
├── 📄 .gitignore          # Ignores .env, venv/, and generated assets
├── 📄 app.py              # Multimodal engine orchestrator & Streamlit UI
├── 📄 requirements.txt    # Dependencies (streamlit, groq, gTTS, requests)
└── 📄 README.md           # Terminal style project documentation
```

---

### 08. SYSTEM SOURCE OVERVIEW

Key architecture components in [`app.py`](file:///c:/Users/Junaid%20Khan/Desktop/Mirai%20Internship%20Assignments/Assignment%205/app.py):

```python
# Multimodal Enrichment Pipeline
def enrich_scene(scene: dict, scene_index: int) -> dict:
    # 1. Image Synthesis with Local File Caching
    if "image_path" not in scene:
        scene["image_path"] = fetch_scene_image(scene["image_prompt"], scene_index)

    # 2. Text-to-Speech Narration Synthesis
    if "audio_path" not in scene:
        scene["audio_path"] = generate_tts_audio(scene["story_text"], scene_index)

    return scene
```

---

### 09. TELEMETRY & LEARNING OUTCOMES

```text
[OK] Multimodal Orchestration : Coordinating LLMs, Diffusion Models, and TTS Voice
[OK] JSON Output Enforcement  : Prompt engineering strict parsable schema boundaries
[OK] Asset Disk Caching       : Local disk caching preventing redundant API calls
[OK] Branching State Machine  : Session history buffer tracking decisions and scenes
[OK] Custom CSS & Typography  : High-end glassmorphic UI with Google Fonts injection
[OK] Error Resilience         : Non-blocking graceful fallbacks for busy external APIs
```

```text
────────────────────────────────────────────────────────────────────────────────
[ VISUAL NOVEL PROTOCOL ACTIVE — MIRAI SCHOOL OF TECHNOLOGY SUMMER 2026 ]
────────────────────────────────────────────────────────────────────────────────
```
