import random
import urllib, urllib2
import uuid
from twilio.util import RequestValidator
from faketwilio import CwurlioUserException

class TwilioProxyRequest(object):

    def random_geodata(self):
        data = [
            ("San Francisco", "CA", "94115", "US"),
            ("New York", "NY", "10458", "US"),
            ("Pullman", "WA", "99163", "US"),
            # not sure if this is accurate
            ("Montreal", "Quebec", "H2B2V9", "Canada"),
        ]
        return random.choice(data)

    def fake_sid(self, prefix):
        return "{0}{1}".format(prefix, str(uuid.uuid4()).replace('-',''))

    @property
    def url_params(self):
        args = {}
        for param in self.params:
            if getattr(self, param, None):
                args[param] = getattr(self, param)
        return args

    def send(self, method, url, authtoken):
        validator = RequestValidator(authtoken)
        params = urllib.urlencode(self.url_params)
        if method == "GET":
            url = "{0}?{1}".format(url, params)
            sig = validator.compute_signature(url, {})
            req = urllib2.Request(url)
        elif method == "POST":
            sig = validator.compute_signature(url, self.url_params)
            req = urllib2.Request(url, params)
        else:
            raise CwurlioUserException("Invalid method: %s" % method)

        req.add_header("X-Twilio-Signature", sig)
        return urllib2.urlopen(req).read()

class TwilioIncomingSmsRequest(TwilioProxyRequest):
    params = ['SmsSid', 'AccountSid', 'From', 'To', 'Body', 'FromCity',
            'FromState', 'FromZip', 'FromCountry', 'ToCity', 'ToState',
            'ToZip', 'ToCountry']

    def __init__(self, AccountSid, From, To, Body):
        self.SmsSid = self.fake_sid("SM")
        self.AccountSid = AccountSid
        self.From = From
        self.To = To
        self.Body = Body

        self.FromCity, self.FromState, self.FromZip, self.FromCountry = self.random_geodata()
        self.ToCity, self.ToState, self.ToZip, self.ToCountry = self.random_geodata()

class TwilioIncomingCallRequest(TwilioProxyRequest):
    params = ['CallSid', 'AccountSid', 'From', 'To', 'CallStatus',
            'ApiVersion', 'Direction', 'FromCity', 'FromState',
            'FromZip', 'FromCountry', 'ToCity', 'ToState', 'ToZip',
            'ToCountry']

    def __init__(self, AccountSid, From, To):
        self.CallSid = self.fake_sid("CA")
        self.AccountSid = AccountSid
        self.From = From
        self.To = To
        self.CallStatus = 'in-progress'
        # XXX: do we care about 2008 version?
        self.ApiVersion = '2010-04-01'
        self.Direction = 'incoming'
        # geodata
        self.FromCity, self.FromState, self.FromZip, self.FromCountry = self.random_geodata()
        self.ToCity, self.ToState, self.ToZip, self.ToCountry = self.random_geodata()
