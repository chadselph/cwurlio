"""
Default handlers for parsing TwiML; just print messages.
"""
from __future__ import print_function

def say(name, attributes, text):
    print("Robot voice says: ", text)

def play(name, attributes, text):
    print("Playing: ", text)

def gather(name, attributes, text):
    raw_input("Gather: (blank for timeout)")

def record(name, attributes, text):
    print("record")

def sms(name, attributes, text):
    print("sending a text to ", text)

def dial(name, attributes, text, children):
    print("dialing...")

def hangup(name, attributes, text):
    print("ending call")

def redirect(name, attributes, text):
    pass

def reject(name, attributes, text):
    pass

def pause(name, attributes, text):
    print("pausing for ",text,"seconds")
