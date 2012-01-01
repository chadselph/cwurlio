Cwurlio
#######
aka Fake TwilioProxy

Cwurlio is used to debug your Twilio Apps so that you don't have to use curl.

Cwurlio is not for outbound SMS or Call REST calls, but rather to test your webapp against 

Instead of

    curl http://myserver/service -X POST -d 'From=15551214312' -d 'Body=asdfa' ...

You can just do:

    cwurlio dial 5551234567
    cwurlio sms 5551234567 --message "hey... man"

Hey buddy, curl works just fine for me, what's the point?
=========================================================

Using curl instead of cwurlio has the following drawbacks:

    * You're not testing the [X-Twilio-Signature](http://www.twilio.com/docs/security#validating-requests) header, this can do that
    * You're only including a subset of the parameters Twilio is going to hit your endpoint witih; this will test them all.
    * curl sucks for this. Like, really.
