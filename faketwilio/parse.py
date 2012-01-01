from xml.etree.ElementTree import XMLParser

class TwimlParseError(Exception): pass

class TwimlQueue(object):
    def __init__(self, say, play, gather, record, sms, dial, hangup, redirect,
            reject, pause):
        self.handlers = {
            'Say': say,
            'Play': play,
            'Gather': gather,
            'Record': record,
            'Sms': sms,
            'Dial': dial,
            'Hangup': hangup,
            'Redirect': redirect,
            'Reject': reject,
            'Pause': pause,
            'Response': (lambda **args: 0)
        }
        dial_subhandlers = {
            'Client': self.dial_noun,
            'Number': self.dial_noun,
            'Conference': self.dial_noun,
        }
        self.handlers.update(dial_subhandlers)
        self.queue = []
        self.in_response = False

    def dial_noun(self, **kwargs):
        # the top of the stack should be a <Dial> right now
        dial = self.queue.pop()
        if dial['tag'] != 'Dial':
            raise TwimlParseError("<%s> should be in a <Dial>" % dial['tag'])
        if 'children' not in dial:
            dial['children'] = []
        dial['children'].append(kwargs)
        self.queue.append(dial)

    def start(self, tag, attributes):
        if not self.in_response:
            if tag != "Response":
                raise TwimlParseError("<Response> needed.")
            else:
                self.in_response = True
        #print "  " * len(self.queue), "entering", tag
        self.queue.append({'tag': tag, 'attributes': attributes})

    def end(self, tag):
        args = self.queue.pop()
        self.handlers[tag](**args)
        #print "  " * len(self.queue), 'ending tag', tag, args

    def data(self, data):
        top = self.queue.pop()
        top['data'] = top.get('data', '') + data
        # put er back
        self.queue.append(top)

    def close(self):
        pass

def parse_twiml(data, *args, **kwargs):
    parser = XMLParser(target=TwimlQueue(*args, **kwargs))
    parser.feed(data)
    parser.close()

if __name__ == "__main__":
    # run tests
    def a(**kwargs):
        print 'callback:', kwargs
    callbacks = [a,a,a,a,a,a,a,a,a,a]
    parser = XMLParser(target=TwimlQueue(*callbacks))
    test = """<?xml version="1.0" encoding="UTF-8" ?>
    <Response>
         <Say voice="woman" language="en-gb" loop="2">Hello</Say>
         <Dial>
            <Client>Chad</Client>
  

            <Number>1234</Number>
         </Dial>
     </Response>"""
    parser.feed(test)
    parser.close()
