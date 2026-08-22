# ⚡ LIFE-OS: SCREEN-TIME & WELLBEING ANALYTICS - Assignment 7

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│  SESSION ID : MIRAI-ASSIGNMENT-07              BUILD  : v7.0.0-RELEASE       │
│  ENGINES    : Pandas + Streamlit + Groq LLM + Pollinations AI                │
│  ANALYTICS  : KPI Telemetry | Time-Series Trends | AI Lifestyle Visualizer   │
│  RUNTIME    : Python 3.8+ / Streamlit          STATUS : [ ONLINE / ACTIVE ]  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 💻 SYSTEM INFO

```text
       /\_/\          user@mirai-workstation:~/Assignment-7
      ( o.o )         -------------------------------------
       > ^ <          PROJECT   : Life-OS Digital Wellbeing Dashboard
                      TRACK     : MirAI Virtual Summer Internship 2026
                      MODULE    : Data Analytics & Multimodal AI Coaching
                      DATASET   : screentime.csv (14-Day App Usage Log)
                      AI COACH  : llama-3.3-70b-versatile (Groq Cloud)
                      IMAGE GEN : Pollinations AI (800x450 Lifestyle Persona)
                      CORE      : app.py / ai.py
                      STATUS    : TELEMETRY_ONLINE
                      PORT      : 8501 (Default HTTP)
```

---

## ⚡ $ man life-os

### 01. SYNOPSIS

```bash
$ life-os --data screentime.csv --goal <MINUTES> [--analyze-trends] [--ai-coach]
```

**Life-OS** is an intelligent digital wellbeing command center and productivity dashboard. It combines **Pandas analytics**, **Streamlit visualization**, **Groq Llama 3.3 70B AI coaching**, and **Pollinations generative art** to ingest screen-time logs, calculate daily health KPIs, plot 14-day behavioral trends, deliver brutal habit evaluations, and generate digital lifestyle persona artwork.

---

### 02. CORE CAPABILITIES

```text
[✓] ROBUST CSV DIAGNOSTIC INSPECTOR ── Auto-checks file presence, byte size, schema & shapes
[✓] REAL-TIME KPI COMPUTATION ──────── Total screen time, top used app, and delta vs daily goal
[✓] 14-DAY TIME-SERIES VISUALS ────── Aggregated daily usage trends & category bar charts
[✓] 6-PART AI COACHING EVALUATION ─── In-depth habit critique powered by Llama 3.3 70B
[✓] GENERATIVE LIFESTYLE ARTWORK ──── Auto-synthesizes visual metaphors based on daily habits
[✓] RESILIENT REST API FALLBACKS ──── Dual Groq SDK + direct HTTP requests with fallback prompts
[✓] INTERACTIVE DATE FILTERING ────── Per-day slice-and-dice data exploration
```

---

### 03. CSV DATASET SCHEMA SPECIFICATION

The dataset parser reads [`screentime.csv`](file:///c:/Users/Junaid%20Khan/Desktop/Mirai%20Internship%20Assignments/Assignment%207/screentime.csv) with flexible column-matching fallback routines:

| Required Column | Data Type | Description |
| :--- | :--- | :--- |
| `Date` | `YYYY-MM-DD` | Timestamp / recording date (parsed with `pd.to_datetime`) |
| `App_Name` | `String` | Target mobile or desktop application |
| `Category` | `String` | Categorical classification (*Social Media*, *Productivity*, *Entertainment*, *Gaming*, etc.) |
| `Minutes_Used` | `Integer` | Total elapsed runtime in minutes |

---

### 04. KPI TELEMETRY & METRIC FORMULAS

```text
1. TOTAL SCREEN TIME (T) = Σ Minutes_Used [Filtered Date]
2. TOP APPLICATION       = Mode(App_Name) OR Argmax(Σ Minutes_Used per App)
3. DELTA VS DAILY GOAL   = Total Screen Time - Daily Goal (mins)
                           ├─ Negative (Green) : Under goal limit (Healthy)
                           └─ Positive (Red)   : Exceeded goal limit (Overconsumption)
```

---

### 05. 6-PART AI COACHING FRAMEWORK

When the user triggers **Generate AI Coaching Insights**, Groq Llama 3.3 70B evaluates the daily summary against the target goal across six structured sections:

```text
  1. 📊 Today's Usage Analysis  : Honest breakdown of category allocation
  2. ✅ Productive Habits       : Highlighting positive workflows and discipline
  3. ⚠️ Unhealthy Habits        : Calling out wasted time and doomscrolling patterns
  4. 🌿 Offline Replacements    : 2-3 specific real-world activity alternatives
  5. 🎯 Tomorrow's Challenge    : 1 actionable, realistic micro-habit challenge
  6. 💪 Final Note              : Uplifting, high-energy motivational closing
```

---

### 06. ARCHITECTURE & ANALYTICS PIPELINE

```text
                ┌──────────────────────────────────────────────┐
                │         screentime.csv Data Ingestion        │
                └──────────────────────┬───────────────────────┘
                                       │
                                       ▼
                ┌──────────────────────────────────────────────┐
                │ CSV Diagnostic Inspector & Schema Validation │
                │ (Shape check, empty-file check, preview)     │
                └──────────────────────┬───────────────────────┘
                                       │
                      ┌────────────────┴────────────────┐
                      ▼                                 ▼
       ┌──────────────────────────────┐  ┌──────────────────────────────┐
       │ 14-Day Line Trend Chart      │  │ Selected Day KPI & Bar Chart │
       │ (Full timeline aggregation)  │  │ (Date filtered breakdown)    │
       └──────────────────────────────┘  └──────────────┬───────────────┘
                                                        │
                                                        ▼
                                         ┌──────────────────────────────┐
                                         │ Generate Usage Summary Table │
                                         │ - Category minutes           │
                                         │ - Goal difference (± mins)   │
                                         └──────────────┬───────────────┘
                                                        │
                                                        ▼
                                         ┌──────────────────────────────┐
                                         │ Groq LLM (Llama 3.3 70B)     │
                                         └──────────────┬───────────────┘
                                                        │
                                       ┌────────────────┴────────────────┐
                                       ▼                                 ▼
                        ┌──────────────────────────────┐  ┌──────────────────────────────┐
                        │ 6-Part Coaching Text Report  │  │ 15-Word Persona Art Prompt   │
                        │ (st.info / st.warning)       │  │ (e.g. "Disciplined scholar") │
                        └──────────────────────────────┘  └──────────────┬───────────────┘
                                                                         │
                                                                         ▼
                                                          ┌──────────────────────────────┐
                                                          │ Pollinations AI Image Render │
                                                          │ (800x450 Lifestyle Artwork)  │
                                                          └──────────────────────────────┘
```

---

### 07. EXECUTION & SETUP GUIDE

```bash
# [Step 1] Navigate to Assignment 7 directory
cd "Assignment 7"

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

# [Step 4] Install package dependencies
pip install -r requirements.txt

# [Step 5] Launch dashboard
streamlit run app.py
```

```text
  You can now view your Streamlit app in your browser.

  Local URL:    http://localhost:8501
  Network URL:  http://192.168.x.x:8501
```

---

### 08. DIRECTORY STRUCTURE

```text
Assignment 7/
├── 📄 .env                # Private API credentials (GROQ_API_KEY)
├── 📄 .gitignore          # Excludes .env, venv/, and bytecode caches
├── 📄 ai.py               # AI coaching & generative lifestyle visualizer
├── 📄 app.py              # Main dashboard UI, data loader, KPIs & charts
├── 📄 requirements.txt    # Project dependencies (streamlit, pandas, groq, requests)
├── 📄 screentime.csv      # 14-day sample screen-time dataset
└── 📄 README.md           # Terminal style project documentation
```

---

### 09. SYSTEM SOURCE OVERVIEW

#### 1. Multimodal AI Coaching Dispatch ([`ai.py`](file:///c:/Users/Junaid%20Khan/Desktop/Mirai%20Internship%20Assignments/Assignment%207/ai.py))
```python
def generate_ai_coaching_and_image(usage_summary: str, total_time: int, goal_minutes: int):
    # Generates structured 6-part habit critique
    coaching_text = generate_ai_coaching(usage_summary, total_time, goal_minutes)

    # Synthesizes digital lifestyle prompt based on goal delta
    image_prompt = generate_digital_lifestyle_prompt(total_time, goal_minutes, usage_summary)

    # Generates 800x450 concept artwork URL
    image_url = get_pollinations_image_url(image_prompt)

    return coaching_text, image_prompt, image_url
```

#### 2. KPI Computation ([`app.py`](file:///c:/Users/Junaid%20Khan/Desktop/Mirai%20Internship%20Assignments/Assignment%207/app.py))
```python
def calculate_kpis(filtered_df: pd.DataFrame, goal_minutes: int):
    time_col = get_time_col(filtered_df)
    app_col = get_app_col(filtered_df)

    total_screen_time = int(filtered_df[time_col].sum()) if time_col else 0
    most_used_app = filtered_df.groupby(app_col)[time_col].sum().idxmax()
    diff_vs_goal = total_screen_time - goal_minutes

    return total_screen_time, most_used_app, diff_vs_goal
```

---

### 10. TELEMETRY & LEARNING OUTCOMES

```text
[OK] Defensive Data Ingestion : Comprehensive error handling for missing/empty CSVs
[OK] Pandas Data Wrangling    : Aggregating, grouping, and filtering time-series records
[OK] Streamlit Metrics & KPIs : Responsive cards with delta color inversions
[OK] Dynamic Visualization   : Native line chart trends & category bar breakdowns
[OK] Multimodal AI Feedback   : Generating both text critiques and lifestyle art metaphors
[OK] API Fault Tolerance      : Dual SDK & REST request fallback architecture
```

```text
────────────────────────────────────────────────────────────────────────────────
[ LIFE-OS TELEMETRY & ANALYTICS ACTIVE — MIRAI INTERNSHIP 2026 ]
────────────────────────────────────────────────────────────────────────────────
```
