"""
Default handlers for parsing TwiML; just print messages.
"""
from __future__ import print_function

def say(tag, attributes, data):
    print("Robot voice says: ", data)

def play(tag, attributes, data):
    print("Playing: ", data)

def gather(tag, attributes, data):
    raw_input("Gather: (blank for timeout)")

def record(tag, attributes, data):
    print("record")

def sms(tag, attributes, data):
    print("sending", attributes.get('to','you') ,"an sms:", data)

def dial(tag, attributes, data, children):
    print("dialing...")

def hangup(tag, attributes, data):
    print("ending call")

def redirect(tag, attributes, data):
    pass

def reject(tag, attributes, data):
    pass

def pause(tag, attributes, data):
    print("pausing for ",data,"seconds")
