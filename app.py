from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import requests
import os


load_dotenv()

app = FastAPI()


VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")


# Facebook Webhook Verification
@app.get("/webhook")
async def verify_token(request: Request):
    params = dict(request.query_params)
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == VERIFY_TOKEN:
        return PlainTextResponse(params.get("hub.challenge"))
    return PlainTextResponse("Error: Invalid verification token", status_code=403)

# Handle Incoming Messages
@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    print("Received Data:", data)

    for entry in data.get("entry", []):
        for messaging_event in entry.get("messaging", []):
            sender_id = messaging_event["sender"]["id"]
            if "message" in messaging_event and "text" in messaging_event["message"]:
                message_text = messaging_event["message"]["text"].lower()
                
                if message_text == "hi":
                    send_message(sender_id, "hi")
                else:
                    send_message(sender_id, "I only reply to 'hi' for now 😄")

    return {"status": "ok"}

def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    print("Sent Message:", response.json())
