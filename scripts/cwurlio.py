import argparse
from faketwilio.http import TwilioIncomingCallRequest, TwilioIncomingSmsRequest
from faketwilio.util import fetch_app
#TODO: import logging


def parse_sms(account, authtoken, number, message, parse_twiml, **kwargs):
    from_ = kwargs.pop('from', '+12345678900')
    req = TwilioIncomingSmsRequest(account, from_, number, message)
    (method, url) = fetch_app(account, authtoken, number, "sms")
    print("Sending a {method} request to {url} ...".format(method=method, url=url))
    resp = req.send(method, url, authtoken)
    if parse_twiml:
        pass
    else:
        print("Got TwiML response...")
        print(resp)

def parse_dial(account, authtoken, number, parse_twiml, **kwargs):
    from_ = kwargs.pop('from', '+12345678900')
    req = TwilioIncomingCallRequest(account, from_, number)
    (method, url) = fetch_app(account, authtoken, number, "dial")
    print("Sending a {method} request to {url} ...".format(method=method, url=url))
    resp = req.send(method, url, authtoken)
    if parse_twiml:
        pass
    else:
        print("Got TwiML response...")
        print(resp)

def main():

    parser = argparse.ArgumentParser(description="Fake Twilio incoming call/sms tester")
    parser.add_argument("--account", help="Twilio Account Sid")
    parser.add_argument("--authtoken", help="Twilio Auth Token")

    # XXX: is this fesible?
    parser.add_argument("--parse-twiml", help="Fake execute the TwiML",
            action="store_true")
    for verb in ["play", "say", "gather", "record", "sms", "dial"]:
        parser.add_argument("--{0}-callback".format(verb),
                help="Python function to do <{0}>".format(verb.capitalize()),
                metavar="module.func", default="faketwilio.twiml.{0}".format(verb))

    subparsers = parser.add_subparsers(help="Phone Action")

    sms_parser = subparsers.add_parser('sms')
    sms_parser.add_argument("number", help="Phone Number to text")
    sms_parser.add_argument('message')
    sms_parser.add_argument('--from')
    sms_parser.set_defaults(func=parse_sms)

    dial_parser = subparsers.add_parser('dial')
    dial_parser.add_argument("number", help="Phone Number to Dial")
    dial_parser.add_argument('--from')
    dial_parser.set_defaults(func=parse_dial)

    args = parser.parse_args()
    args.func(**vars(args))


if __name__ == "__main__":
    main()
