from twilio.rest import Client

def texting():
    account_sid = "AC4c12692fe7d2052d6f9e2438483f5de0"
    auth_token  = "1b8883cda788b896061c839a6df84b3f"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+16096138831",
        from_= "+17039911570",
        body="This is the Hackathon Project AI. A medical emergency has been detected, please send help immediately")
    
    print(message.sid)