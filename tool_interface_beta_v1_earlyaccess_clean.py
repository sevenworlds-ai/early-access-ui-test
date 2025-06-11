import streamlit as st
import json
import datetime
import io

st.set_page_config(page_title="Early Access UI Test")
st.title("Early Access UI Test")

modes = {
    "Supportive Approach": "Gentle, measured, non-intrusive tone."
}
mode = "Supportive Approach"
st.markdown(f"**Access:** Early Access UI Test")
st.caption("Prototype for user feedback")

user_input = st.text_input("What would you like to ask the system?")

if 'session_history' not in st.session_state or not isinstance(st.session_state.session_history, list):
    st.session_state.session_history = []

# Load Checkpoint
uploaded_file = st.file_uploader("Load Session State (.json)", type="json")
if uploaded_file is not None:
    try:
        checkpoint_data = json.load(uploaded_file)
        if isinstance(checkpoint_data.get("session_history"), dict):
            checkpoint_data["session_history"] = [checkpoint_data["session_history"]]
        st.session_state.session_history = checkpoint_data.get("session_history", [])
        st.success("✅ Session state loaded successfully.")
    except Exception as e:
        st.error(f"❌ Failed to load session state: {e}")

# Append input to history (with debounce)
if user_input and (
    not st.session_state.session_history or
    st.session_state.session_history[-1].get("prompt") != user_input
):
    timestamp = datetime.datetime.now().isoformat()
    st.session_state.session_history.append({
        "prompt": user_input,
        "response": f"Response to: {user_input}",
        "mode": mode,
        "timestamp": timestamp
    })

# Show session history log
if st.checkbox("Show Session History"):
    st.markdown("### Export & Save Options")

    export_format = st.radio("Choose export format:", ["TXT", "JSON"])

    if st.button("Clear History Log"):
        st.session_state.session_history.clear()

    # Export logic
    if export_format == "TXT":
        export_data = ""
        for entry in st.session_state.session_history:
            export_data += f"Prompt: {entry.get('prompt', '')}\n"
            export_data += f"Response: {entry.get('response', '')}\n"
            export_data += f"Mode: {entry.get('mode', '')}\n"
            export_data += f"Timestamp: {entry.get('timestamp', '')}\n\n"
        file_data = io.StringIO(export_data)
        file_name = f"history_{datetime.datetime.now().isoformat().replace(':', '_')}.txt"
    else:
        file_data = io.StringIO(json.dumps(st.session_state.session_history, indent=2))
        file_name = f"history_{datetime.datetime.now().isoformat().replace(':', '_')}.json"

    st.download_button(
        label="Download History Log",
        data=file_data.getvalue().encode("utf-8"),
        file_name=file_name
    )

    st.download_button(
        label="Save Session State",
        data=json.dumps({"session_history": st.session_state.session_history}, indent=2).encode("utf-8"),
        file_name=f"checkpoint_{datetime.datetime.now().isoformat().replace(':', '_')}.json"
    )

    for i, entry in enumerate(st.session_state.session_history, 1):
        st.markdown(
            f"**Prompt:** {entry.get('prompt', '')}<br>"
            f"**Response:** {entry.get('response', '')}<br>"
            f"**Mode:** {entry.get('mode', '')}<br>"
            f"**Timestamp:** {entry.get('timestamp', '')}",
            unsafe_allow_html=True
        )
