import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Email Classifier",
    page_icon="📧",
    layout="wide"
)

# Color mappings
URGENCY_COLORS = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
SENTIMENT_COLORS = {"Positive": "😊", "Neutral": "😐", "Negative": "😠"}
CATEGORY_COLORS = {
    "Support": "🔧", "Sales": "💼", "Billing": "💰",
    "Spam": "🚫", "HR": "👥", "Legal": "⚖️",
    "Technical": "💻", "Partnership": "🤝",
    "Complaint": "😡", "General": "📬"
}

st.title("📧 AI Email Classifier")
st.markdown("Classify emails instantly using Claude AI — category, urgency, sentiment and suggested response.")
st.divider()

# Load sample emails
try:
    samples_response = requests.get(f"{API_URL}/sample-emails")
    sample_emails = samples_response.json()["emails"] if samples_response.status_code == 200 else []
except Exception:
    sample_emails = []

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Email Input")

    if sample_emails:
        st.markdown("**Quick Test — Load a sample email:**")
        sample_labels = ["-- Select a sample --"] + [e["label"] for e in sample_emails]
        selected_sample = st.selectbox("", sample_labels)

        if selected_sample != "-- Select a sample --":
            sample = next(e for e in sample_emails if e["label"] == selected_sample)
            st.session_state["sender"] = sample["sender"]
            st.session_state["subject"] = sample["subject"]
            st.session_state["body"] = sample["body"]

    sender = st.text_input(
        "Sender Email",
        value=st.session_state.get("sender", ""),
        placeholder="sender@example.com"
    )
    subject = st.text_input(
        "Email Subject",
        value=st.session_state.get("subject", ""),
        placeholder="Enter email subject..."
    )
    body = st.text_area(
        "Email Body",
        value=st.session_state.get("body", ""),
        placeholder="Paste email body here...",
        height=250
    )

    classify_btn = st.button(
        "Classify Email",
        type="primary",
        disabled=not (subject.strip() or body.strip())
    )

with col2:
    st.subheader("Classification Results")

    if classify_btn and (subject.strip() or body.strip()):
        with st.spinner("Analyzing email with Claude AI..."):
            try:
                response = requests.post(
                    f"{API_URL}/classify",
                    json={"subject": subject, "body": body, "sender": sender}
                )

                if response.status_code == 200:
                    data = response.json()
                    c = data["classification"]

                    # Top metrics row
                    m1, m2, m3 = st.columns(3)
                    with m1:
                        cat_icon = CATEGORY_COLORS.get(c["category"], "📬")
                        st.metric("Category", f"{cat_icon} {c['category']}")
                    with m2:
                        urg_icon = URGENCY_COLORS.get(c["urgency"], "⚪")
                        st.metric("Urgency", f"{urg_icon} {c['urgency']}")
                    with m3:
                        sent_icon = SENTIMENT_COLORS.get(c["sentiment"], "😐")
                        st.metric("Sentiment", f"{sent_icon} {c['sentiment']}")

                    st.divider()

                    # Summary and confidence
                    st.markdown(f"**Summary:** {c.get('summary', '')}")
                    st.progress(
                        c.get("confidence", 0) / 100,
                        text=f"Confidence: {c.get('confidence', 0)}%"
                    )

                    # Human review warning
                    if c.get("requires_human_review"):
                        st.warning("⚠️ This email requires human review")

                    st.divider()

                    # Key points
                    st.markdown("**Key Points:**")
                    for point in c.get("key_points", []):
                        st.markdown(f"- {point}")

                    # Tags
                    if c.get("tags"):
                        st.markdown("**Tags:** " + " ".join([f"`{tag}`" for tag in c["tags"]]))

                    st.divider()

                    # Recommended action
                    st.markdown(f"**Recommended Action:** {c.get('action', '')}")

                    # Auto reply suggestion
                    st.markdown("**Suggested Reply:**")
                    st.info(c.get("auto_reply_suggestion", ""))

                    # Raw JSON
                    with st.expander("View Raw JSON Response"):
                        st.json(c)

                else:
                    error_msg = "Something went wrong"
                    try:
                        error_msg = response.json().get("detail", error_msg)
                    except Exception:
                        error_msg = response.text
                    st.error(f"Error: {error_msg}")

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to API. Make sure FastAPI is running on port 8000.")

    else:
        st.info("Enter an email on the left and click Classify to get started.")
        st.markdown("**What this tool detects:**")
        st.markdown("- Category (Support, Sales, Billing, Spam, HR, Legal...)")
        st.markdown("- Urgency level (High, Medium, Low)")
        st.markdown("- Sentiment (Positive, Neutral, Negative)")
        st.markdown("- Key points extracted from the email")
        st.markdown("- Suggested reply for the email")
        st.markdown("- Whether human review is required")