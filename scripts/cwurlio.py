import argparse
from faketwilio.http import TwilioIncomingCallRequest, TwilioIncomingSmsRequest
from faketwilio.parse import parse_twiml as parser
from faketwilio.util import fetch_app, callback_str
#TODO: import logging


def parse_sms(account, authtoken, number, message, **kwargs):
    from_ = kwargs.pop('from', '+12345678900')
    req = TwilioIncomingSmsRequest(account, from_, number, message)
    return run(account, authtoken, 'sms', req, number, **kwargs)

def parse_dial(account, authtoken, number, **kwargs):
    from_ = kwargs.pop('from', '+12345678900')
    req = TwilioIncomingCallRequest(account, from_, number)
    return run(account, authtoken, 'dial', req, number, **kwargs)

def run(account, authtoken, action, req, number, parse_twiml, **kwargs):
    (method, url) = fetch_app(account, authtoken, number, action)
    print("Sending a {method} request to {url} ...".format(method=method, url=url))
    resp = req.send(method, url, authtoken)
    if parse_twiml:
        parser(resp,
            kwargs['say_callback'],
            kwargs['play_callback'],
            kwargs['gather_callback'],
            kwargs['record_callback'],
            kwargs['sms_callback'],
            kwargs['dial_callback'],
            kwargs['hangup_callback'],
            kwargs['redirect_callback'],
            kwargs['reject_callback'],
            kwargs['pause_callback'])
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
    for verb in ["play", "say", "gather", "record", "sms", "dial", "hangup", "redirect", "reject", "pause"]:
        parser.add_argument("--{0}-callback".format(verb), metavar="module.func",
                help="Python function to do <{0}>".format(verb.capitalize()),
                default="faketwilio.twiml.{0}".format(verb), type=callback_str)

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
