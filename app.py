# Import libraries
import urllib.request
import pushbullet
import pywhatkit
import os
from pyChatGPT import ChatGPT
import datetime
import time
import keyboard

# Load keys from .env file
API_KEY = os.getenv("pushbullet_key")
session_token = os.getenv("chatgpt_key")

# Initiate Pushbullet and ChatGPT
pb = pushbullet.Pushbullet(API_KEY)
api = ChatGPT(session_token)
file_path = "chat.txt"

# Initiate timestamp and first message
last_day = "0"
first_message = True

# Determine if ChatGPT should roleplay
role_playing = True


# Get contact details
contact_dict = {"Jonas": os.getenv("Jonas_number"), "Flo":os.getenv("Florian_number"), "Mama":os.getenv("Mama_number"), "Romy":os.getenv("Romy_number")}
relation_dict = {"Jonas": "me", "Flo": "brother", "Mama": "mother", "Romy": "boyfriend"}

while True:
    # Download Chatfile from pushbullet database
    pushes = pb.get_pushes()
    latest = pushes[0]
    url = latest['file_url']
    urllib.request.urlretrieve(url, file_path)

    # read last message
    with open(file_path, mode='r', encoding="utf8") as f:
        data = f.readlines()
    
    if len(data) > 10:
        last_messages = data[len(data)-10:(len(data))]
    else: 
        last_messages = data[1:(len(data))]
    
    last_messages.reverse()
    last_contact = last_messages[0]
    last_contact = last_contact.split(": ")[0]
    last_contact = last_contact.split("- ")[1]
    last_message = ""
    for message in last_messages:
        # Determine message time and message sender
        msg_day = message.split(".")[0]
        msg_hour = message.split(":")[0]
        msg_hour = msg_hour.split(", ")[1]
        msg_minute = message.split("-")[0]
        msg_minute = msg_minute.split(":")[1]
        contact = message.split(": ")[0]
        contact = contact.split("- ")[1]
        send_message = False
        if contact in [last_contact]:
            # Remove timestamp and message sender information from last message
            message = message.split(": ")[1]
            last_message = message + last_message
        else:
            break
        
    # Check if a new message has been sent
    if msg_day > last_day or msg_day == last_day and msg_hour > last_hour or msg_day == last_day and msg_hour == last_hour and msg_minute > last_minute:
        
        # forward message to ChatGPT
        if role_playing and first_message:
            last_message = f'''We make a roleplay where you are my {relation_dict[last_contact]}. 
            Reply directly in the same language. Do not mention that you are a AI model and that we make a roleplay. 
            {last_message}'''
            print(msg_day, msg_hour, msg_minute, last_message)

        # determine current time
        current_time = datetime.datetime.now()
        hour = current_time.hour
        minute = current_time.minute
        second = current_time.second
        if second < 35:
            minute += 1
        else: 
            minute += 2

        response = api.send_message(last_message)
        response = "".join(response.get("message"))
        
        # send whatsapp message to receive 
        contact_number = contact_dict[last_contact]
        pywhatkit.sendwhatmsg(contact_number, response, hour, minute)
        first_message = False

        # update time that last message was sent
        last_day = msg_day
        last_hour = msg_hour
        last_minute = msg_minute
        keyboard.press_and_release('ctrl+w')
    
    # wait 10 seconds before the next check
    time.sleep(120)