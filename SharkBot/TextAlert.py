#!/usr/bin/env python3
from twilio.rest import Client
import argparse
import os

# the following line needs your Twilio Account SID and Auth Token

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number
def send_message(message='Oh no!'):
    client = Client(os.getenv('TWILIO_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    client.messages.create(to=os.getenv('MY_PHONE_NUMBER'),
                           from_=os.getenv('TWILIO_NUMBER'),
                           body=message)


def main():
    parser = argparse.ArgumentParser(description='Notify me when a service is down')
    parser.add_argument('message', help='The message to be sent to my phone')
    args = parser.parse_args()

    send_message(args.message)

if __name__ == '__main__':
    main()
