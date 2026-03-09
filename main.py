from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from classifier import classify_email

app = FastAPI(
    title="Email Classifier API",
    description="AI-powered email classification using Anthropic Messages API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailRequest(BaseModel):
    subject: str
    body: str
    sender: str = ""

@app.get("/")
def root():
    return {"message": "Email Classifier API is running", "status": "healthy"}

@app.post("/classify")
def classify(request: EmailRequest):
    """Classify an email and return structured result"""
    if not request.subject.strip() and not request.body.strip():
        raise HTTPException(status_code=400, detail="Email subject or body is required")

    result = classify_email(request.subject, request.body, request.sender)

    return {
        "subject": request.subject,
        "sender": request.sender,
        "classification": result
    }

@app.get("/sample-emails")
def sample_emails():
    """Returns sample emails for testing"""
    return {
        "emails": [
            {
                "label": "Urgent Support",
                "sender": "angry.customer@email.com",
                "subject": "URGENT: System completely down, losing money every minute!",
                "body": "Our entire payment processing system has been down for 2 hours. We are losing thousands of dollars per minute. This is completely unacceptable. I need someone to call me immediately."
            },
            {
                "label": "Sales Inquiry",
                "sender": "john.smith@company.com",
                "subject": "Interested in your enterprise plan",
                "body": "Hi, I came across your product and I am very interested in the enterprise plan for our team of 50 people. Could you send me pricing information and schedule a demo?"
            },
            {
                "label": "Billing Issue",
                "sender": "finance@client.com",
                "subject": "Invoice discrepancy - Invoice #4521",
                "body": "Hello, I noticed that Invoice #4521 dated last month has an incorrect amount. We were charged $2,500 but our contract states $2,000. Please review and issue a corrected invoice."
            },
            {
                "label": "Spam",
                "sender": "noreply@promo.com",
                "subject": "YOU HAVE WON $1,000,000!!!",
                "body": "Congratulations! You have been selected as our lucky winner. Click here to claim your prize now! Limited time offer!"
            },
            {
                "label": "Partnership",
                "sender": "partnerships@techfirm.com",
                "subject": "Partnership opportunity between our companies",
                "body": "Dear team, I represent TechFirm and we believe there is a great synergy between our products. We would love to explore a potential partnership. Would you be available for a call next week?"
            }
        ]
    }