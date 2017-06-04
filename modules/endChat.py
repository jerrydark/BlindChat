from templates import TextTemplate
from templates import add_quick_reply
from utilities import send_gender_menu, send_message
import requests
import config
import os
import json

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', config.ACCESS_TOKEN)

def endChat(sender, activeChatsDB, payload, sharePromptDone=False):

    try:
        partner = activeChatsDB.get_partner(sender)
        alias1 = activeChatsDB.get_alias(sender)
        alias2 = activeChatsDB.get_alias(partner)
    except:
        message = TextTemplate(text="No open chat was found which can be closed")
        send_message(message.get_message(), id=sender)
        send_gender_menu(sender=sender)
        return

    if sharePromptDone == False:

        # SENDER
        message = TextTemplate(text = "You have ended the chat with. Would you like to share your profile with "+alias2+"?")
        message = message.get_message()
        message = add_quick_reply(message=message, title="Share", payload=json.dumps({"keyword":"profile_share","ans":"y"}))
        message = add_quick_reply(message=message, title="Don't share", payload=json.dumps({"keyword":"profile_share","ans":"n"}))

        send_message(message=message, id=sender)

        # PARTNER
        message = TextTemplate(text=alias1+" has quit the chat. Would you like to share your profile with " + alias1 + "?")
        message = message.get_message()
        message = add_quick_reply(message=message, title="Share", payload=json.dumps({"keyword":"profile_share","ans":"y"}))
        message = add_quick_reply(message=message, title="Don't share", payload=json.dumps({"keyword":"profile_share","ans":"n"}))

        send_message(message=message, id=partner)


    else:
        if isinstance(payload, str):
            payload = json.loads(payload)
        if payload["ans"] == "y":
            message = TextTemplate(text="www.facebook.com/"+partner)
            send_message(message=message.get_message(), id=partner)

        send_gender_menu(sender=sender)
