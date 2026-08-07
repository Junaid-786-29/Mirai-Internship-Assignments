import os
import requests
import urllib.parse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_pollinations_image_url(prompt: str) -> str:
    """Encodes an image prompt and returns the Pollinations.ai image URL."""
    clean_prompt = prompt.strip().strip('"').strip("'")
    encoded_prompt = urllib.parse.quote(clean_prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=450&nologo=true"

def generate_digital_lifestyle_prompt(total_time: int, goal_minutes: int, usage_summary: str) -> str:
    """
    Generates a short image prompt describing the user's current digital lifestyle based on screen time.
    """
    api_key = os.getenv("GROQ_API_KEY") or os.getenv("GEMINI_API_KEY")
    diff = total_time - goal_minutes

    # Default fallback prompts if API call fails
    fallback_prompt = (
        "A tired zombie scrolling endlessly on a glowing smartphone in a dark room" 
        if diff > 0 else 
        "A disciplined programmer reading books peacefully at a sunlit desk"
    )

    if not api_key:
        return fallback_prompt

    system_prompt = (
        "You are a creative prompt engineer. Based on a user's daily screen time and goal, "
        "generate a short, vivid image prompt (max 15 words) describing their current digital lifestyle.\n"
        "Examples:\n"
        "- If user spent too much screen time: 'A tired zombie scrolling endlessly on a glowing smartphone in dark room'\n"
        "- If user met their goal: 'A disciplined programmer reading physical books at a sunlit desk'\n\n"
        "Return ONLY the plain text image prompt with no extra commentary, quotes, or markdown."
    )

    user_prompt = f"Total screen time: {total_time} mins (Goal: {goal_minutes} mins). Usage summary:\n{usage_summary}"

    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=60
        )
        res_prompt = completion.choices[0].message.content.strip()
        return res_prompt if res_prompt else fallback_prompt
    except Exception:
        # HTTP fallback
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 60
        }
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=20)
            if res.status_code == 200:
                prompt_res = res.json()["choices"][0]["message"]["content"].strip()
                return prompt_res if prompt_res else fallback_prompt
            else:
                return fallback_prompt
        except Exception:
            return fallback_prompt

def generate_ai_coaching(usage_summary: str, total_time: int, goal_minutes: int) -> str:
    """
    Generates AI coaching insights using Groq based on today's category-wise screen usage.
    Acts as a brutally honest but supportive productivity coach.
    """
    api_key = os.getenv("GROQ_API_KEY") or os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "⚠️ **Error**: Groq API key not found. Please ensure `GROQ_API_KEY` is set inside your `.env` file."

    system_prompt = (
        "You are a brutally honest but supportive productivity and digital wellbeing coach for 'Life-OS'. "
        "Your goal is to evaluate the user's daily screen time usage and category breakdown, giving actionable, direct, "
        "and encouraging feedback.\n\n"
        "You MUST structure your response with the following sections clearly formatted in Markdown:\n"
        "1. 📊 **Today's Usage Analysis**: A brutally honest breakdown of how they spent their screen time.\n"
        "2. ✅ **Productive Habits**: Highlight what they did well or healthy patterns observed.\n"
        "3. ⚠️ **Unhealthy Habits**: Call out wasted time, excessive usage, or potential doomscrolling.\n"
        "4. 🌿 **Offline Replacements**: Suggest 2-3 specific, engaging offline activities to substitute screen time.\n"
        "5. 🎯 **Tomorrow's Challenge**: Give 1 realistic, actionable micro-challenge for tomorrow.\n"
        "6. 💪 **Final Note**: End on an encouraging, motivating, and positive note.\n\n"
        "Keep your tone empathetic yet direct and concise."
    )

    user_prompt = f"""
Here is the user's screen-time usage report for today:
- Total Screen Time Today: {total_time} minutes
- Daily Screen Time Goal: {goal_minutes} minutes
- Difference vs Goal: {total_time - goal_minutes:+} minutes

Category-wise Usage Breakdown:
{usage_summary}

Please provide your AI coaching evaluation based on this data.
"""

    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return completion.choices[0].message.content
    except Exception:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"⚠️ **Groq API Error** ({response.status_code}): {response.text}"
        except Exception as req_err:
            return f"⚠️ **Connection Error**: Could not connect to Groq API ({req_err})."

def generate_ai_coaching_and_image(usage_summary: str, total_time: int, goal_minutes: int):
    """
    Generates both AI coaching feedback and Pollinations image prompt + URL.
    Returns: (coaching_text, image_prompt, image_url)
    """
    coaching_text = generate_ai_coaching(usage_summary, total_time, goal_minutes)
    image_prompt = generate_digital_lifestyle_prompt(total_time, goal_minutes, usage_summary)
    image_url = get_pollinations_image_url(image_prompt)
    return coaching_text, image_prompt, image_url
