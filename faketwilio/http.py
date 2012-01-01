import random
import urllib
import uuid

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

    def to_url_params(self, extra=None):
        args = {} if extra is None else extra
        for param in self.params:
            if getattr(self, param, None):
                args[param] = getattr(self, param)
        return urllib.urlencode(args)

    def send(self, method, url):
        if method == "GET":
            # TODO: doesn't combine GET args if some are already in URL
            # (could use requests or httplib2 for this)
            return urllib.urlopen("{0}?{1}".format(method, url)).read()
        elif method == "POST":
            return urllib.urlopen(url, self.to_url_params()).read()
        else:
            raise CwurlioUserException("Invalid method: {0}".format(method))

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
