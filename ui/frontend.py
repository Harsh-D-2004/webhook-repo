import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:5000/webhook/data"

if "data" not in st.session_state:
    st.session_state.data = None

@st.fragment(run_every=15)
def fetch_data_fragment():
    try:
        print("Fetching data from API...")
        res = requests.get(API_URL, timeout=5)
        res.raise_for_status()
        st.session_state.data = res.json()
        render_event_list()
    except Exception as e:
        st.error(f"API error: {e}")

def get_action_config(action):
    """Return icon, color, and label for each action type"""
    configs = {
        "PUSH": {"icon": "🚀", "color": "#4A90E2", "label": "Push"},
        "MERGE": {"icon": "🔀", "color": "#7B68EE", "label": "Merge"},
        "PULL_REQUEST": {"icon": "📬", "color": "#F39C12", "label": "Pull Request"}
    }
    return configs.get(action.upper(), {"icon": "📌", "color": "#95A5A6", "label": action})

def format_timestamp(dt_str):
    """Parse and format timestamp"""
    if not dt_str:
        return None

    try:
        dt_str_normalized = dt_str.replace('Z', '+00:00')
        dt = datetime.fromisoformat(dt_str_normalized)

        day = dt.day
        suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

        month = dt.strftime("%B")
        year = dt.year
        hour = int(dt.strftime("%I"))
        minute = dt.strftime("%M")
        am_pm = dt.strftime("%p")

        return f"{day}{suffix} {month} {year} - {hour}:{minute} {am_pm} UTC"
    
    except Exception:
        return None

def render_event_card(event, index):

    author = event.get('author', 'Unknown')
    action = event.get('action', 'ACTION')
    from_br = event.get('from_branch', 'unknown-branch')
    to_br = event.get('to_branch', 'unknown-branch')
    dt_str = event.get('timestamp', {}).get('$date')

    config = get_action_config(action)
    formatted_time = format_timestamp(dt_str)

    if action == "PUSH":
        message = f"pushed to **`{to_br}`**"
    elif action == "MERGE":
        message = f"merged **`{from_br}`** → **`{to_br}`**"
    elif action == "PULL_REQUEST":
        message = f"opened PR from **`{from_br}`** to **`{to_br}`**"
    else:
        message = f"performed {action.lower()}"

    with st.container():
        col1, col2 = st.columns([0.08, 0.92])

        with col1:
            st.markdown(f"<div style='font-size: 32px; text-align: center;'>{config['icon']}</div>",
                       unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div style='
                    padding: 16px;
                    border-left: 4px solid {config['color']};
                    background: linear-gradient(to right, {config['color']}15, transparent);
                    border-radius: 8px;
                    margin-bottom: 12px;
                '>
                    <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 4px;'>
                        <span style='
                            background: {config['color']};
                            color: white;
                            padding: 2px 8px;
                            border-radius: 4px;
                            font-size: 11px;
                            font-weight: 600;
                            text-transform: uppercase;
                        '>{config['label']}</span>
                        <span style='color: #666; font-size: 13px;'>
                            {formatted_time if formatted_time else 'Date unavailable'}
                        </span>
                    </div>
                    <div style='font-size: 16px; margin-top: 8px;'>
                        <strong style='color: {config['color']};'>{author}</strong> {message}
                    </div>
                </div>
            """, unsafe_allow_html=True)

def render_event_list():
    if st.session_state.data and st.session_state.data.get('data'):
        events = st.session_state.data['data']

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Events", len(events))
        with col2:
            merge_count = sum(1 for e in events if e.get('action') == 'MERGE')
            st.metric("Merges", merge_count)
        with col3:
            push_count = sum(1 for e in events if e.get('action') == 'PUSH')
            st.metric("Pushes", push_count)

        st.markdown("---")

        for idx, event in enumerate(events):
            render_event_card(event, idx)
    else:
        st.info("🔍 No events found. Waiting for GitHub webhook events...")

st.set_page_config(page_title="GitHub Events Feed", page_icon="📦", layout="wide")

col1, col2 = st.columns([8, 1])
with col1:
    st.title("📦 GitHub Events Feed")
    st.caption("Real-time monitoring of GitHub webhook events")

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()
        fetch_data_fragment()

st.markdown("---")
st.subheader("📊 Latest Events")

fetch_data_fragment()
