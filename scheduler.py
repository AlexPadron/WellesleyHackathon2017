import datetime
import json
import os
import time
import threading

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from chatbot import get_initial_msg, reply_to_msg


settings = json.loads(open('./settings.json').read())

client = Client(settings['SID'], settings['KEY'])

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def handle_sms():
    '''Use chatbot to respond to messages'''
    reply = MessagingResponse()
    phone_num = request.values['From']
    body = request.values['Body']
    text = body.split(' ')
    results = filter(lambda x: x['phone_number']= phone_num, settings['SCHEDULES'])

    if len(results)>0:
        settings['SCHEDULES']["frequency"] = text[-1]
        settings['SCHEDULES']["username"] = text[-2]
    else:
        settings['SCHEDULES'].append({"username": text[-2], "phone_number": phone_num,
            "frequency": text[-1]})

    try:
        response = reply_to_msg(body)
    except Exception as e:
        response = str(e)
    reply.message(response)
    return str(reply)


def send_message(number, name):
    '''Send an sms message'''
    client.messages.create(
        to=number,
        from_='8602002058',
        body=get_initial_msg(number, name)
    )

def run_schedule():
    '''Send automated messages'''
    start = datetime.datetime.now()
    for schedule in settings['SCHEDULES']:
        schedule['next_time'] = (
            start + datetime.timedelta(minutes=schedule['frequency']))
    while True:
        now = datetime.datetime.now()
        for schedule in settings['SCHEDULES']:
            print 'checking schedule with next {} and now {}'.format(
                schedule['next_time'], now)
            if now > schedule['next_time']:
                send_message(schedule['phone_number'],
                             schedule['username'])
                schedule['next_time'] = (
                    now + datetime.timedelta(minutes=schedule['frequency']))
        time.sleep(1)


thread = threading.Thread(target=run_schedule)
thread.daemon = True
thread.start()

app.run(debug=True, port=80)
