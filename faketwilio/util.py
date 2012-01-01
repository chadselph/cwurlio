import sys
from twilio.rest import TwilioRestClient
from faketwilio import CwurlioUserException

def fetch_app(account, auth, number, action="dial"):
    client = TwilioRestClient(account, auth)
    numbers = client.phone_numbers.list()
    matches = [num for num in numbers if number in num.phone_number]
    if len(matches) == 1:
        if action == "dial":
            return fetch_dial_app(matches[0], client)
        elif action == "sms":
            return fetch_sms_app(matches[0], client)
    elif len(matches) == 0:
        phone_numbers = ",".join([num.phone_number for num in numbers])
        raise CwurlioUserException("{number} not found; try one of {phone_numbers}".format(**locals()))
    else:
        phone_numbers = ",".join([num.phone_number for num in matches])
        raise CwurlioUserException("Which do you mean? {0}".format(phone_numbers))

def fetch_dial_app(match, client):
    if match.voice_application_sid:
        #lookup app
        match = client.applications.get(match.voice_application_sid)
    return match.voice_method, match.voice_url

def fetch_sms_app(match, client):
    if match.sms_application_sid:
        #lookup app
        match = client.applications.get(match.sms_application_sid)
    return match.sms_method, match.sms_url

def get_callback(string):
    mod, func = string.rsplit(".", 1)
    __import__(mod)
    return getattr(sys.modules[mod], func)
