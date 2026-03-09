# 📧 AI Email Classifier

An intelligent email classification system powered by Claude AI. Instantly categorizes emails by type, urgency, sentiment, and generates suggested replies — all via a clean Streamlit UI backed by a FastAPI service.

---

## 🚀 Features

- **10 Categories**: Support, Sales, Billing, Spam, HR, Legal, Technical, Partnership, Complaint, General
- **Urgency Detection**: High / Medium / Low
- **Sentiment Analysis**: Positive / Neutral / Negative
- **Confidence Score**: How certain Claude is about the classification
- **Key Points Extraction**: Bullet summary of the email's main points
- **Auto-Reply Suggestion**: AI-generated reply draft
- **Human Review Flag**: Alerts when manual review is recommended
- **Sample Emails**: Built-in test emails to demo the system
- **Raw JSON View**: Full classification output for developers

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Model | Claude API (`claude-opus-4-6`) via Anthropic Messages API |
| Backend | Python, FastAPI, Uvicorn |
| Frontend | Streamlit |
| HTTP Client | Requests |

---

## 📁 Project Structure

```
email-classifier/
├── main.py          # FastAPI app — POST /classify, GET /sample-emails
├── classifier.py    # Claude API integration and prompt logic
├── app.py           # Streamlit frontend
├── .env             # API key (not committed)
├── .env.example     # Example env file
├── requirements.txt # Python dependencies
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/abdullahaghaMAF/claude-api-email-classifier.git
cd claude-api-email-classifier
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
copy .env.example .env    # Windows
cp .env.example .env      # Mac/Linux
```
Edit `.env` and add your Anthropic API key.

### 5. Run FastAPI backend
```bash
uvicorn main:app --reload --port 8000
```

### 6. Run Streamlit frontend (new terminal)
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/classify` | Classify an email |
| `GET` | `/sample-emails` | Return sample test emails |

### POST /classify — Request Body
```json
{
  "subject": "Invoice overdue",
  "body": "Hi, I noticed my invoice #1234 is now 30 days overdue...",
  "sender": "client@example.com"
}
```

### POST /classify — Response
```json
{
  "classification": {
    "category": "Billing",
    "urgency": "High",
    "sentiment": "Negative",
    "confidence": 94,
    "summary": "Client reporting overdue invoice requiring immediate attention",
    "key_points": ["Invoice #1234 is 30 days overdue", "Client requesting resolution"],
    "action": "Escalate to billing team immediately",
    "auto_reply_suggestion": "Thank you for reaching out. We are reviewing invoice #1234 and will respond within 24 hours.",
    "tags": ["billing", "overdue", "urgent"],
    "requires_human_review": true
  }
}
```

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key from console.anthropic.com |

---

## 📬 Sample Use Cases

- **Customer support teams** — Auto-route incoming emails to the right department
- **Sales teams** — Prioritize high-urgency leads instantly
- **Operations** — Flag emails requiring human review before they pile up
- **Developers** — Use the `/classify` API endpoint in any email pipeline

---

## 📄 License

MIT License — free to use, modify, and distribute.