from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import requests
import os

app = FastAPI()

VERIFY_TOKEN = "my_secret_token_1478"
PAGE_ACCESS_TOKEN = "EAAVOfvpDttcBO6DJZAZC4nJoFeFVyA53woZB5xOqsKhNTQMma1pjDtyXew7Eo5O5gKgqdAeR0j4VF8MZBV0qM7AJ3LK266jWlOeH3pIwNXlWHgW9CNm0wByMinMjG7y63kfGhri7monZBSKboERtz4vaVNGJrplkIuUPKPIy8ZCZBdJZCmFQyx5yhr3FDM1yLn2BUGLXWWaZBjgZDZD" 

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
