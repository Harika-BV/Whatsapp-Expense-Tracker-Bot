from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from src.bot import agent

routes = Blueprint("routes", __name__)

@routes.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    resp = MessagingResponse()

    try:
        result = agent.run(incoming_msg)  # AI processes user input
        resp.message(result)
    except Exception as e:
        print(e)
        resp.message("❌ Sorry, I couldn't process that request.")

    return str(resp)
