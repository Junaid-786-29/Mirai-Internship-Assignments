import json
import os
import urllib.parse
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from gtts import gTTS

load_dotenv()

st.set_page_config(
    page_title="AI Visual Novel · Groq",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(160deg, #0f0c29, #302b63, #24243e);
    }

    .scene-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 1.6rem 2rem;
        margin-bottom: 1.2rem;
        backdrop-filter: blur(10px);
    }

    .story-text {
        font-family: 'Lora', serif;
        font-size: 1.08rem;
        line-height: 1.85;
        color: #e8e0ff;
    }

    .scene-label {
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #a78bfa;
        margin-bottom: 0.4rem;
    }

    .choice-header {
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #818cf8;
        margin: 1.2rem 0 0.6rem;
    }

    div.stButton > button {
        background: rgba(139, 92, 246, 0.18);
        border: 1px solid rgba(139, 92, 246, 0.45);
        border-radius: 10px;
        color: #e8e0ff;
        font-family: 'Lora', serif;
        font-size: 0.97rem;
        padding: 0.55rem 1rem;
        transition: all 0.18s ease;
    }
    div.stButton > button:hover {
        background: rgba(139, 92, 246, 0.38);
        border-color: rgba(167, 139, 250, 0.8);
        color: #ffffff;
        transform: translateY(-1px);
    }

    [data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.85);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

ASSETS_DIR = Path("assets")
IMAGES_DIR = ASSETS_DIR / "images"
AUDIO_DIR  = ASSETS_DIR / "audio"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

POLLINATIONS_BASE = (
    "https://image.pollinations.ai/prompt/{prompt}"
    "?width=832&height=468&nologo=true&model=flux"
)

IMAGE_TIMEOUT = 45
TTS_LANG      = "en"

@st.cache_resource
def get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error(
            "🔑 **GROQ_API_KEY not found.**  "
            "Please add `GROQ_API_KEY=your_key_here` to your `.env` file "
            "and restart the app."
        )
        st.stop()
    return Groq(api_key=api_key)

GROQ_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """
You are the narrator of an interactive AI visual novel.

Your ONLY job is to respond with a single, valid JSON object.
Never return markdown.
Never wrap your answer inside ```json ... ```.
Never add any text before or after the JSON object.
Return ONLY the raw JSON.

The JSON object must follow this exact schema:

{
  "story_text": "<120-180 word narrative passage in second-person (you/your)>",
  "image_prompt": "<detailed, cinematic scene description for an image model; include lighting, mood, art style token, composition, foreground and background detail>",
  "options": [
    "<choice 1>",
    "<choice 2>",
    "<choice 3>"
  ]
}

Rules:
- story_text   : 120-180 words, immersive, second-person point-of-view.
- image_prompt : at least 40 words; must reference the art style and genre.
- options      : 2-3 meaningful, distinct choices that advance the story.
- Weave the genre and art style naturally into every scene.
- Keep scenes narratively consistent with prior conversation history.
""".strip()

def init_session_state() -> None:
    defaults: dict = {
        "messages"      : [],
        "story_history" : [],
        "current_scene" : None,
        "genre"         : "Fantasy",
        "art_style"     : "Anime",
        "story_started" : False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def init_groq_messages() -> list[dict]:
    return [{"role": "system", "content": SYSTEM_PROMPT}]

def generate_scene(user_message: str) -> str:
    client = get_groq_client()
    st.session_state.messages.append({"role": "user", "content": user_message})

    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=st.session_state.messages,
        temperature=0.9,
        max_tokens=700,
    )

    raw_text = completion.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": raw_text})
    return raw_text

def parse_scene_json(raw_text: str) -> dict | None:
    try:
        return json.loads(raw_text.strip())
    except (json.JSONDecodeError, ValueError):
        st.warning(
            f"⚠️ The model returned unexpected output and the scene could not be parsed.\n\n"
            f"Raw response (first 300 chars): `{raw_text[:300]}`",
            icon="⚠️",
        )
        return None

def fetch_scene_image(image_prompt: str, scene_index: int) -> str | None:
    save_path = IMAGES_DIR / f"scene_{scene_index:03d}.png"

    if save_path.exists():
        return str(save_path)

    try:
        encoded_prompt = urllib.parse.quote(image_prompt)
        url = POLLINATIONS_BASE.format(prompt=encoded_prompt)

        response = requests.get(url, timeout=IMAGE_TIMEOUT)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type:
            raise ValueError(f"Unexpected Content-Type: {content_type}")

        save_path.write_bytes(response.content)
        return str(save_path)

    except Exception:
        st.toast("🖼️ Image server is busy, skipping visual...", icon="⚠️")
        return None

def generate_tts_audio(story_text: str, scene_index: int) -> str | None:
    save_path = AUDIO_DIR / f"scene_{scene_index:03d}.mp3"

    if save_path.exists():
        return str(save_path)

    try:
        tts = gTTS(text=story_text, lang=TTS_LANG, slow=False)
        tts.save(str(save_path))
        return str(save_path)

    except Exception:
        st.toast("🔇 Narration unavailable.", icon="⚠️")
        return None

def enrich_scene(scene: dict, scene_index: int) -> dict:
    if "image_path" not in scene:
        with st.spinner("🎨 Generating scene image…"):
            scene["image_path"] = fetch_scene_image(
                scene["image_prompt"], scene_index
            )

    if "audio_path" not in scene:
        with st.spinner("🔊 Generating narration…"):
            scene["audio_path"] = generate_tts_audio(
                scene["story_text"], scene_index
            )

    return scene

def render_sidebar() -> tuple[str, str]:
    with st.sidebar:
        st.title("📖 Story Settings")
        st.divider()

        genre = st.selectbox(
            label="Story Genre",
            options=["Fantasy", "Horror", "Sci-Fi", "Mystery", "Adventure"],
            index=["Fantasy", "Horror", "Sci-Fi", "Mystery", "Adventure"].index(
                st.session_state.genre
            ),
            help="Sets the narrative genre of your visual novel.",
        )

        art_style = st.selectbox(
            label="Art Style",
            options=["Anime", "Realistic", "Watercolor", "Cyberpunk", "Pixel Art"],
            index=["Anime", "Realistic", "Watercolor", "Cyberpunk", "Pixel Art"].index(
                st.session_state.art_style
            ),
            help="Determines the visual style of generated scene images.",
        )

        st.divider()
        st.caption("Changing settings after starting a story will restart it.")

        if st.session_state.story_started:
            st.divider()
            if st.button(
                "🔄 Restart Story",
                type="secondary",
                use_container_width=True,
                help="Clear the current story and begin fresh with the same settings.",
            ):
                st.session_state.messages      = []
                st.session_state.story_history = []
                st.session_state.current_scene = None
                st.session_state.story_started = False
                st.rerun()

    return genre, art_style

def render_scene_media(scene: dict) -> None:
    image_path = scene.get("image_path")
    audio_path = scene.get("audio_path")

    if image_path:
        st.image(image_path, use_container_width=True)
    else:
        st.info("🖼️ Scene image could not be generated.", icon="🎨")

    if audio_path:
        st.audio(audio_path, format="audio/mp3")
    else:
        st.caption("🔇 Audio narration unavailable for this scene.")

def render_past_scene(scene: dict, scene_index: int) -> None:
    st.markdown(f"<p class='scene-label'>📜 Scene {scene_index}</p>", unsafe_allow_html=True)
    render_scene_media(scene)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"<div class='story-text'>{scene['story_text']}</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<p class='choice-header'>Choices presented</p>", unsafe_allow_html=True)
    for i, option in enumerate(scene["options"], start=1):
        st.markdown(f"&nbsp;&nbsp;**{i}.** {option}")

    st.divider()

def render_latest_scene(scene: dict, scene_index: int) -> None:
    st.markdown(
        f"<p class='scene-label'>📜 Scene {scene_index} &nbsp;·&nbsp; <em>current</em></p>",
        unsafe_allow_html=True,
    )
    render_scene_media(scene)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"<div class='story-text'>{scene['story_text']}</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p class='choice-header'>🔀 What will you do?</p>", unsafe_allow_html=True)

    for opt_idx, option in enumerate(scene["options"]):
        button_key = f"choice_s{scene_index}_o{opt_idx}"
        if st.button(label=option, key=button_key, use_container_width=True):
            with st.spinner("✍️ Continuing the story…"):
                raw_response = generate_scene(option)

            next_scene = parse_scene_json(raw_response)
            if next_scene is None:
                st.stop()

            next_scene_index = scene_index + 1
            next_scene = enrich_scene(next_scene, next_scene_index)

            st.session_state.story_history.append(next_scene)
            st.session_state.current_scene = next_scene

            st.toast("✅ New scene loaded!", icon="✅")
            st.rerun()

def main() -> None:
    init_session_state()
    genre, art_style = render_sidebar()

    if genre != st.session_state.genre or art_style != st.session_state.art_style:
        st.session_state.genre         = genre
        st.session_state.art_style     = art_style
        st.session_state.messages      = []
        st.session_state.story_history = []
        st.session_state.current_scene = None
        st.session_state.story_started = False

    st.title("🌌 AI Visual Novel")
    st.caption(
        f"Genre: **{st.session_state.genre}** · Art Style: **{st.session_state.art_style}**"
    )
    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.story_started:
        st.markdown(
            "Welcome! Choose your **Genre** and **Art Style** in the sidebar, "
            "then press **Start Story** to begin your adventure."
        )
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("▶ Start Story", type="primary", use_container_width=True):
            st.session_state.messages = init_groq_messages()

            opening_instruction = (
                f"Begin a brand-new {st.session_state.genre} visual novel story. "
                f"The art style for all image prompts must be {st.session_state.art_style}. "
                "Generate the very first scene. "
                "Remember: respond ONLY with the raw JSON object."
            )

            with st.spinner("✍️ Writing the opening scene…"):
                raw_response = generate_scene(opening_instruction)

            scene = parse_scene_json(raw_response)
            if scene is None:
                st.stop()

            scene = enrich_scene(scene, scene_index=1)

            st.session_state.story_history.append(scene)
            st.session_state.current_scene = scene
            st.session_state.story_started = True

            st.toast("✅ Your story has begun!", icon="📖")
            st.rerun()

    if st.session_state.story_started and st.session_state.story_history:
        history    = st.session_state.story_history
        last_index = len(history) - 1

        for i, scene in enumerate(history):
            scene_number = i + 1

            if i < last_index:
                render_past_scene(scene, scene_number)
            else:
                render_latest_scene(scene, scene_number)

if __name__ == "__main__":
    main()
