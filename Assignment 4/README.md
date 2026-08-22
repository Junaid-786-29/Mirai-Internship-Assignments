# 🎨 AI IMAGE STUDIO - Assignment 4

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│  SESSION ID : MIRAI-ASSIGNMENT-04              BUILD  : v4.0.0-RELEASE       │
│  ENGINE     : Pollinations AI Diffusion API    HOST   : localhost:8501       │
│  RESOLUTION : 256x256 up to 1536x1536          STATUS : [ ONLINE / ACTIVE ]  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 💻 SYSTEM INFO

```text
       /\_/\          user@mirai-workstation:~/Assignment-4
      ( o.o )         -------------------------------------
       > ^ <          PROJECT   : AI Image Studio
                      TRACK     : MirAI Virtual Summer Internship 2026
                      MODULE    : Text-to-Image Generation & Media Pipeline
                      ENGINE    : Pollinations AI API
                      CORE      : app.py
                      STATUS    : RENDER_ENGINE_ONLINE
                      PORT      : 8501 (Default HTTP)
```

---

## ⚡ $ man image-studio

### 01. SYNOPSIS

```bash
$ image-studio --style "<ART_STYLE>" --resolution "<W>x<H>" --prompt "<QUERY>" [--magic-enhance]
```

**AI Image Studio** is an interactive web workstation built on **Streamlit** and the **Pollinations AI Image API**. It enables generative text-to-image synthesis with configurable artistic styles, custom dimensional scaling, heuristic prompt enhancement, randomized creative ideation, and direct high-resolution PNG downloads.

---

### 02. CORE CAPABILITIES

```text
[✓] POLLINATIONS AI INTEGRATION ── Serverless, zero-token generative image synthesis
[✓] 6 CURATED ART PRESETS ──────── Realistic, Anime, Fantasy, Cyberpunk, Oil Painting, Pixel Art
[✓] VARIABLE DIMENSION CONTROLS ── Custom width & height sliders (256px to 1536px, step=64)
[✓] ✨ MAGIC ENHANCE ENGINE ────── Automated prompt engineering for 8k quality and photorealism
[✓] 🎲 SURPRISE ME! IDEATION ───── Instant generation from a curated creative prompt bank
[✓] IN-MEMORY BINARY STREAMING ─── Zero-disk overhead using io.BytesIO and PIL.Image
[✓] ONE-CLICK ASSET DOWNLOAD ───── Built-in st.download_button for PNG exports
```

---

### 03. ART STYLE PRESET MATRIX

| Art Style Identifier | Output Aesthetic & Characteristics | Prompt Prefix Injector |
| :--- | :--- | :--- |
| **Realistic** | Photorealistic lighting, natural textures, depth of field | `Realistic style, ...` |
| **Anime** | Vibrant cel-shading, Japanese animation aesthetics | `Anime style, ...` |
| **Fantasy** | Mythical lighting, atmospheric scenery, surreal fantasy art | `Fantasy style, ...` |
| **Cyberpunk** | Neon-lit palettes, futuristic cityscapes, synthwave vibe | `Cyberpunk style, ...` |
| **Oil Painting** | Classical canvas textures, rich impasto brush strokes | `Oil Painting style, ...` |
| **Pixel Art** | 16-bit / 32-bit retro arcade raster styling | `Pixel Art style, ...` |

---

### 04. MAGIC ENHANCE & SYNTHESIS SPECS

When enabled via the sidebar checkbox (`✨ Enable Magic Enhance`), the prompt synthesis engine automatically appends high-fidelity stylistic modifiers:

```text
Full Prompt = f"{art_style} style, {user_prompt}, masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"
```

#### Resolution Configuration Parameters:
```text
  MIN RESOLUTION : 256 x 256 px
  DEFAULT        : 1024 x 1024 px
  MAX RESOLUTION : 1536 x 1536 px (Step: 64px)
```

---

### 05. GENERATION & ASSET PIPELINE

```text
  ┌───────────────────────┐       ┌────────────────────────┐
  │ Sidebar: Art Style    │       │ Sidebar: Width & Height│
  └───────────┬───────────┘       └───────────┬────────────┘
              │                               │
              └───────────────┬───────────────┘
                              ▼
        ┌───────────────────────────────────────────┐
        │ User Prompt OR 🎲 "Surprise Me!" Selection│
        └─────────────────────┬─────────────────────┘
                              │
                              ▼
        ┌───────────────────────────────────────────┐
        │  Prompt Synthesizer & URL Encoder         │
        │  - Prefix: {art_style} style              │
        │  - Infix: {prompt}                        │
        │  - Suffix (if enabled): Magic Enhance tags│
        │  - urllib.parse.quote(full_prompt)        │
        └─────────────────────┬─────────────────────┘
                              │
                              ▼
        ┌───────────────────────────────────────────┐
        │ Pollinations AI GET Request               │
        │ https://image.pollinations.ai/prompt/...  │
        └─────────────────────┬─────────────────────┘
                              │
                              ▼
        ┌───────────────────────────────────────────┐
        │ In-Memory Binary Stream (BytesIO & PIL)   │
        └─────────────────────┬─────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
        ┌─────────────────────┐┌─────────────────────┐
        │ st.image() Display  ││ st.download_button()│
        │ Responsive Canvas   ││ PNG File Export     │
        └─────────────────────┘└─────────────────────┘
```

---

### 06. EXECUTION & SETUP GUIDE

```bash
# [Step 1] Navigate to Assignment 4 directory
cd "Assignment 4"

# [Step 2] Initialize and activate virtual environment
# Windows (PowerShell):
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS:
python3 -m venv venv
source venv/bin/activate

# [Step 3] Install package dependencies
pip install -r requirements.txt

# [Step 4] Launch application
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
Assignment 4/
├── 📄 .gitignore          # Excludes venv/, bytecode, and cached files
├── 📄 app.py              # Core Streamlit app & Pollinations AI image pipeline
├── 📄 requirements.txt    # Project dependencies (streamlit, requests, pillow)
└── 📄 README.md           # Terminal style project documentation
```

---

### 08. SYSTEM SOURCE OVERVIEW

```python
import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import urllib.parse
import random

st.set_page_config(page_title="AI Image Studio", page_icon="🎨", layout="wide")

surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A dragon reading a newspaper in a coffee shop",
    "A giant cat ruling a medieval kingdom",
    "A floating island with waterfalls in the sky"
]

st.title("🎨 AI Image Studio")
st.write("Generate stunning AI images using Pollinations AI.")

st.sidebar.header("⚙️ Settings")
art_style = st.sidebar.selectbox("Choose Art Style", ["Realistic", "Anime", "Fantasy", "Cyberpunk", "Oil Painting", "Pixel Art"])
width = st.sidebar.slider("Image Width", min_value=256, max_value=1536, value=1024, step=64)
height = st.sidebar.slider("Image Height", min_value=256, max_value=1536, value=1024, step=64)
magic_enhance = st.sidebar.checkbox("✨ Enable Magic Enhance")

prompt = st.text_input("Describe your image", placeholder="Example: A futuristic city at sunset...")
generate = st.button("🎨 Generate Image")
surprise = st.button("🎲 Surprise Me!")

def generate_image(user_prompt):
    full_prompt = f"{art_style} style, {user_prompt}"
    if magic_enhance:
        full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"

    encoded_prompt = urllib.parse.quote(full_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}"

    with st.spinner("🎨 Generating your AI image..."):
        response = requests.get(url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            st.image(image, caption="Generated AI Image", use_container_width=True)
            st.download_button(
                label="⬇️ Download Image",
                data=response.content,
                file_name=f"{art_style}_image.png",
                mime="image/png"
            )
        else:
            st.error("❌ Failed to generate image. Please try again.")

if generate:
    if prompt.strip() == "":
        st.warning("Please enter a prompt.")
    else:
        generate_image(prompt)

if surprise:
    random_prompt = random.choice(surprise_prompts)
    st.info(f"🎲 Surprise Prompt:\n\n**{random_prompt}**")
    generate_image(random_prompt)
```

---

### 09. TELEMETRY & LEARNING OUTCOMES

```text
[OK] REST API Integration  : Invoking generative image endpoints via requests
[OK] URL Encoding          : Sanitizing complex prompt strings with urllib.parse
[OK] In-Memory IO          : Handling binary image payloads via io.BytesIO and PIL
[OK] st.download_button()  : Client-side file delivery without server storage
[OK] Responsive Layouts    : Configuring wide-mode displays and container scaling
[OK] Heuristic Prompts     : Automated quality enhancement tagging
```

```text
────────────────────────────────────────────────────────────────────────────────
[ IMAGE STUDIO SYNTHESIS READY — MIRAI SCHOOL OF TECHNOLOGY SUMMER 2026 ]
────────────────────────────────────────────────────────────────────────────────
```
