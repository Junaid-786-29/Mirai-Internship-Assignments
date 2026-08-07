import os
import streamlit as st
import pandas as pd
from ai import generate_ai_coaching_and_image

REQUIRED_COLUMNS = ["Date", "App_Name", "Category", "Minutes_Used"]

st.set_page_config(
    page_title="Life-OS | Digital Wellbeing & Screen-Time Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_time_col(df: pd.DataFrame):
    possible_time_cols = [
        "Minutes_Used", "Screen Time (min)", "Screen Time", "Usage (min)", 
        "Duration", "Time Spent (min)", "Usage", "Usage_Minutes"
    ]
    for col in possible_time_cols:
        if col in df.columns:
            return col
    numeric_cols = df.select_dtypes(include=["number"]).columns
    return numeric_cols[0] if len(numeric_cols) > 0 else None

def get_app_col(df: pd.DataFrame):
    possible_app_cols = ["App_Name", "App", "Application", "App Name", "AppName"]
    for col in possible_app_cols:
        if col in df.columns:
            return col
    object_cols = [c for c in df.columns if c not in ["Date", "Category", "App Category"]]
    return object_cols[0] if len(object_cols) > 0 else None

def get_category_col(df: pd.DataFrame):
    possible_cat_cols = ["Category", "App Category", "App_Category", "Type"]
    for col in possible_cat_cols:
        if col in df.columns:
            return col
    return None

def load_data_with_debugging(filepath: str = "screentime.csv"):
    abs_path = os.path.abspath(filepath)

    st.write(f"📂 **Exact File Path**: `{abs_path}`")

    file_exists = os.path.exists(abs_path)
    st.write(f"📌 **File Exists**: `{'Yes' if file_exists else 'No'}`")

    if not file_exists:
        st.error(f"❌ **FileNotFoundError**: Could not locate dataset file at `{abs_path}`. Please verify that `screentime.csv` exists in the project directory.")
        return None

    try:
        if os.path.getsize(abs_path) == 0:
            st.warning(f"⚠️ **EmptyDataError**: The file `{abs_path}` is empty (0 bytes). It contains no headers or rows. Please populate `screentime.csv` with valid dataset records.")
            return None

        df = pd.read_csv(abs_path)

        if df.empty:
            st.warning(f"⚠️ **EmptyDataError**: The CSV file `{abs_path}` contains header definitions but 0 data rows. Please add records to `screentime.csv`.")
            return None

        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

        st.write(f"📊 **Dataframe Shape**: `{df.shape[0]}` rows × `{df.shape[1]}` columns")

        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            st.warning(
                f"⚠️ **Missing Columns Warning**: The dataset is missing required column(s): `{missing_cols}`. "
                f"Expected columns: `{REQUIRED_COLUMNS}`. Found columns: `{list(df.columns)}`."
            )

        st.markdown("##### 📄 First 5 Rows Preview")
        st.dataframe(df.head(5), use_container_width=True)

        return df

    except FileNotFoundError:
        st.error(f"❌ **FileNotFoundError**: The file `{abs_path}` could not be found.")
        return None
    except pd.errors.EmptyDataError:
        st.warning(f"⚠️ **EmptyDataError**: The file `{abs_path}` is empty (0 bytes). Please populate it with CSV data containing {REQUIRED_COLUMNS}.")
        return None
    except Exception as e:
        st.error(f"❌ **Error Loading CSV**: An unexpected error occurred while reading `{abs_path}`: {e}")
        return None

def render_header():
    with st.container():
        st.title("⚡ Life-OS — Screen-Time & Wellbeing Analytics")
        st.caption("A modern SaaS dashboard for monitoring digital habits, daily screen-time goals, and AI-driven coaching.")
        st.divider()

def render_sidebar(df: pd.DataFrame):
    st.sidebar.title("🎛️ Dashboard Controls")
    st.sidebar.caption("Filter data & set your daily limits")

    if df is None or df.empty:
        st.sidebar.warning("No data available to filter.")
        screen_time_goal = st.sidebar.slider(
            "🎯 Daily Screen Time Goal (minutes)",
            min_value=30,
            max_value=720,
            value=240,
            step=15
        )
        return pd.DataFrame(), screen_time_goal

    filtered_df = df.copy()

    if "Date" in df.columns and not df.empty:
        unique_days = df["Date"].dt.date.dropna().unique()
        if len(unique_days) > 0:
            selected_day = st.sidebar.selectbox("📅 Select Day", options=unique_days)
            filtered_df = df[df["Date"].dt.date == selected_day]

    st.sidebar.divider()

    screen_time_goal = st.sidebar.slider(
        "🎯 Daily Screen Time Goal (minutes)",
        min_value=30,
        max_value=720,
        value=240,
        step=15,
        help="Target limit for maximum screen time per day."
    )

    st.sidebar.divider()
    st.sidebar.caption("Powered by Life-OS AI Engine v1.0")

    return filtered_df, screen_time_goal

def calculate_kpis(filtered_df: pd.DataFrame, goal_minutes: int):
    if filtered_df is None or filtered_df.empty:
        return 0, "N/A", 0

    time_col = get_time_col(filtered_df)
    app_col = get_app_col(filtered_df)

    total_screen_time = int(filtered_df[time_col].sum()) if time_col else 0

    if time_col and app_col:
        most_used_app = filtered_df.groupby(app_col)[time_col].sum().idxmax()
    elif app_col and not filtered_df[app_col].empty:
        most_used_app = filtered_df[app_col].mode().iloc[0]
    else:
        most_used_app = "N/A"

    diff_vs_goal = total_screen_time - goal_minutes

    return total_screen_time, most_used_app, diff_vs_goal

def render_kpis(total_time: int, most_used_app: str, diff_vs_goal: int):
    with st.container():
        st.subheader("📌 Key Performance Indicators")
        st.caption("Real-time summary of today's digital consumption and goal alignment.")
        
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="Total Screen Time Today",
                value=f"{total_time} mins",
                help="Sum of all application screen-time today"
            )

        with col2:
            st.metric(
                label="Most Used Application",
                value=str(most_used_app),
                help="Application with highest total usage duration today"
            )

        with col3:
            st.metric(
                label="Difference vs Daily Goal",
                value=f"{diff_vs_goal:+} mins",
                delta=f"{diff_vs_goal:+} mins",
                delta_color="inverse",
                help="Difference between actual screen time and target goal"
            )

def render_charts(full_df: pd.DataFrame, filtered_df: pd.DataFrame):
    with st.container():
        st.subheader("📈 Visual Analytics")
        st.caption("Compare long-term usage trends against today's category breakdown.")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 📅 Total Screen Time Trend (All Days)")
            st.caption("14-day aggregated screen-time trajectory")
            if full_df is not None and not full_df.empty:
                time_col = get_time_col(full_df)
                if time_col and "Date" in full_df.columns:
                    daily_trend = full_df.groupby(full_df["Date"].dt.date)[time_col].sum().reset_index()
                    daily_trend.columns = ["Date", "Screen Time (min)"]
                    st.line_chart(daily_trend.set_index("Date"), use_container_width=True)
                else:
                    st.info("No timeline data available for trend chart.")
            else:
                st.info("No data available for line chart.")

        with col2:
            st.markdown("##### 📊 Today's Usage by Category")
            st.caption("Category distribution for the selected day")
            if filtered_df is not None and not filtered_df.empty:
                time_col = get_time_col(filtered_df)
                cat_col = get_category_col(filtered_df)
                app_col = get_app_col(filtered_df)

                if time_col and cat_col:
                    cat_breakdown = filtered_df.groupby(cat_col)[time_col].sum().reset_index()
                    cat_breakdown.columns = [cat_col, "Screen Time (min)"]
                    st.bar_chart(cat_breakdown.set_index(cat_col), use_container_width=True)
                elif time_col and app_col:
                    app_breakdown = filtered_df.groupby(app_col)[time_col].sum().reset_index()
                    app_breakdown.columns = [app_col, "Screen Time (min)"]
                    st.bar_chart(app_breakdown.set_index(app_col), use_container_width=True)
                else:
                    st.info("No category/app breakdown data available.")
            else:
                st.info("No data available for today's category breakdown.")

def render_ai_coaching_section(filtered_df: pd.DataFrame, total_time: int, goal_minutes: int):
    with st.container():
        st.subheader("AI Productivity Coach")
        st.caption("Brutally honest feedback, habit evaluation, and digital lifestyle concept artwork.")

        if filtered_df is None or filtered_df.empty:
            st.info("No screen time data available for AI coaching today.")
            return

        time_col = get_time_col(filtered_df)
        cat_col = get_category_col(filtered_df) or get_app_col(filtered_df)

        if time_col and cat_col:
            summary_df = filtered_df.groupby(cat_col)[time_col].sum().reset_index()
            usage_summary = "\n".join(
                [f"- {row[cat_col]}: {row[time_col]} mins" for _, row in summary_df.iterrows()]
            )
        else:
            usage_summary = f"- Total screen time: {total_time} mins"

        if st.button("Generate AI Coaching Insights & Lifestyle Visual 🧠🎨", type="primary", use_container_width=True):
            with st.spinner("AI Coach is analyzing your habits & generating your digital lifestyle visual..."):
                coaching_text, image_prompt, image_url = generate_ai_coaching_and_image(
                    usage_summary=usage_summary,
                    total_time=total_time,
                    goal_minutes=goal_minutes
                )
                st.session_state["coaching_feedback"] = coaching_text
                st.session_state["lifestyle_image_prompt"] = image_prompt
                st.session_state["lifestyle_image_url"] = image_url

        if "coaching_feedback" in st.session_state and st.session_state["coaching_feedback"]:
            coaching_text = st.session_state["coaching_feedback"]
            
            if total_time <= goal_minutes:
                st.info(coaching_text)
            else:
                st.warning(coaching_text)

            if "lifestyle_image_url" in st.session_state and st.session_state["lifestyle_image_url"]:
                st.markdown("##### 🖼️ Digital Lifestyle Persona Visualization")
                st.image(
                    st.session_state["lifestyle_image_url"],
                    caption=f"AI Generated Concept: \"{st.session_state.get('lifestyle_image_prompt', '')}\"",
                    use_container_width=True
                )
                st.caption("Visual generated dynamically via Pollinations AI based on today's screen time.")

def render_dataset_view(filtered_df: pd.DataFrame):
    with st.container():
        st.subheader("📋 Filtered Dataset View")
        st.caption("Detailed view of application usage records for the selected day.")
        if filtered_df is not None and not filtered_df.empty:
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.info("No records to display for the current selection.")

def main():
    render_header()

    with st.container():
        st.subheader("🔍 CSV Dataset Inspector & Debugger")
        st.caption("Verifying `screentime.csv` status, path, shape, preview, and schema requirements.")
        df = load_data_with_debugging()
        st.divider()

    filtered_df, screen_time_goal = render_sidebar(df)

    total_time, most_used_app, diff_vs_goal = calculate_kpis(filtered_df, screen_time_goal)
    render_kpis(total_time, most_used_app, diff_vs_goal)

    st.divider()

    render_charts(df, filtered_df)

    st.divider()

    render_ai_coaching_section(filtered_df, total_time, screen_time_goal)

    st.divider()

    render_dataset_view(filtered_df)

if __name__ == "__main__":
    main()
