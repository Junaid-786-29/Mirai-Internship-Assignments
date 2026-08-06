import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import urllib.parse
import random

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="AI Image Studio",
    page_icon="🎨",
    layout="wide"
)

# -------------------------------------------------
# Surprise Prompts
# -------------------------------------------------
surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A dragon reading a newspaper in a coffee shop",
    "A giant cat ruling a medieval kingdom",
    "A floating island with waterfalls in the sky"
]

# -------------------------------------------------
# Title
# -------------------------------------------------
st.title("🎨 AI Image Studio")
st.write("Generate stunning AI images using Pollinations AI.")

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
st.sidebar.header("⚙️ Settings")

art_style = st.sidebar.selectbox(
    "Choose Art Style",
    [
        "Realistic",
        "Anime",
        "Fantasy",
        "Cyberpunk",
        "Oil Painting",
        "Pixel Art"
    ]
)

width = st.sidebar.slider(
    "Image Width",
    min_value=256,
    max_value=1536,
    value=1024,
    step=64
)

height = st.sidebar.slider(
    "Image Height",
    min_value=256,
    max_value=1536,
    value=1024,
    step=64
)

magic_enhance = st.sidebar.checkbox("✨ Enable Magic Enhance")

# -------------------------------------------------
# User Prompt
# -------------------------------------------------
prompt = st.text_input(
    "Describe your image",
    placeholder="Example: A futuristic city at sunset..."
)

# -------------------------------------------------
# Buttons
# -------------------------------------------------
generate = st.button("🎨 Generate Image")
surprise = st.button("🎲 Surprise Me!")

# -------------------------------------------------
# Image Generation Function
# -------------------------------------------------
def generate_image(user_prompt):

    # Combine Art Style + Prompt
    full_prompt = f"{art_style} style, {user_prompt}"

    # Magic Enhance
    if magic_enhance:
        full_prompt += (
            ", masterpiece, 8k resolution, highly detailed, "
            "trending on artstation, unreal engine 5 render"
        )

    # Encode Prompt
    encoded_prompt = urllib.parse.quote(full_prompt)

    # Assignment Task 1
    url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width={width}&height={height}"
    )

    with st.spinner("🎨 Generating your AI image..."):

        response = requests.get(url)

        if response.status_code == 200:

            image = Image.open(BytesIO(response.content))

            st.image(
                image,
                caption="Generated AI Image",
                use_container_width=True
            )

            # Assignment Task 2
            st.download_button(
                label="⬇️ Download Image",
                data=response.content,
                file_name=f"{art_style}_image.png",
                mime="image/png"
            )

        else:
            st.error("❌ Failed to generate image. Please try again.")

# -------------------------------------------------
# Generate Button Logic
# -------------------------------------------------
if generate:

    if prompt.strip() == "":
        st.warning("Please enter a prompt.")

    else:
        generate_image(prompt)

# -------------------------------------------------
# Surprise Me Button Logic
# -------------------------------------------------
if surprise:

    random_prompt = random.choice(surprise_prompts)

    st.info(f"🎲 Surprise Prompt:\n\n**{random_prompt}**")

    generate_image(random_prompt)