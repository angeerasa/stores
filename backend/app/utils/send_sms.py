# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

twillio_from_mobile = os.environ["TWILLIO_FROM_MOBILE"]

def send_sms(to, message):
    print(f"sent sms {message}");
    # message = client.messages.create(
    #     body=f"OTP is {message}",
    #     from_=twillio_from_mobile,
    #     to=to,
    # )

    # print(message.body)
