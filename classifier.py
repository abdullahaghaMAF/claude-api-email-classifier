import anthropic
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def classify_email(subject: str, body: str, sender: str = "") -> dict:
    """Classify an email using Claude API and return structured result"""

    prompt = f"""You are an expert email classification system for a business.
Analyze the following email and return a structured classification.

Email Details:
- Sender: {sender if sender else "Unknown"}
- Subject: {subject}
- Body: {body}

Classify this email and respond in this exact JSON format:
{{
    "category": "one of: Support, Sales, Billing, Spam, HR, Legal, Technical, Partnership, Complaint, General",
    "urgency": "one of: High, Medium, Low",
    "sentiment": "one of: Positive, Neutral, Negative",
    "confidence": <number between 0 and 100 indicating classification confidence>,
    "action": "Brief recommended action for the recipient",
    "key_points": ["key point 1", "key point 2", "key point 3"],
    "auto_reply_suggestion": "A professional suggested reply to this email in 2-3 sentences",
    "tags": ["tag1", "tag2", "tag3"],
    "requires_human_review": true or false,
    "summary": "One sentence summary of what this email is about"
}}

Classification rules:
- High urgency: requires response within hours (complaints, outages, legal, urgent billing)
- Medium urgency: requires response within 24 hours (general support, sales inquiries)
- Low urgency: can wait 2-3 days (newsletters, partnerships, general info)
- Mark requires_human_review as true for legal, complaints, or sensitive topics

Return only the JSON, no explanation."""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    result_text = response.content[0].text.strip()
    result_text = result_text.replace("```json", "").replace("```", "").strip()
    return json.loads(result_text)