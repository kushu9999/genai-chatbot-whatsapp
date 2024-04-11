from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_FROM = os.getenv('TWILIO_FROM')

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)


def send_reply(id, result):
    message = client.messages.create(
        from_=TWILIO_FROM,
        body=result,
        to=id
    )

    print(message.sid)
