from copy import deepcopy
import datetime
import json
import os
import time
import threading

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from chatbot import get_initial_msg, reply_to_msg, train_chatbot


STARTX = 'STARTX'

settings = json.loads(open('./settings.json').read())

client = Client(settings['SID'], settings['KEY'])

app = Flask(__name__)


def scan_for_intros(request_body, number):
    '''Send reasonable looking responses when given as a fake number'''
    is_likely_intro = False
    for kw in ('hey it', 'nice to', 'my number'):
        if kw in request_body.lower():
            is_likely_intro = True
    if (len(filter(lambda x: x['phone_number'] == number,
                   settings['SCHEDULES'])) == 0
        and (not STARTX in request_body)):
        is_likely_intro = True
    if is_likely_intro:
        reply = MessagingResponse()
        reply.message('nice to hear from you! I\'ll be in touch!')
        return str(reply)

@app.route('/', methods=['GET', 'POST'])
def handle_sms():
    '''Use chatbot to respond to messages'''
    reply = MessagingResponse()
    phone_num = request.values['From']
    body = request.values['Body']

    # check for intros
    intro = scan_for_intros(body, request.values['From'])
    if intro is not None:
        return intro

    # delete number from schedule
    for index, schedule in enumerate(settings['SCHEDULES']):
        print 'checking schedule', schedule
        print 'number is', request.values['From']
        if schedule['phone_number'] == request.values['From']:
            print 'deleting index', index
            del settings['SCHEDULES'][index]

    # add to schedule
    if body.startswith(STARTX):
        _, frequency, username = body.split(' ')
        frequency = float(frequency)
        found_schedule = False
        for schedule in enumerate(settings['SCHEDULES']):
            if schedule['phone_number'] == phone_num:
                schedule['frequency'] = frequency
                schedule['username'] = username
                found_schedule = True
        if not found_schedule:
            settings['SCHEDULES'].append({
                "username": username,
                "phone_number": phone_num,
                "frequency": frequency
            })
        reply.message('Started schedule for {} with frequency {}'.format(
            username, frequency))
        return str(reply)

    try:
        response = reply_to_msg(body)
        print 'response is', response
        response = str(response)
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
    while True:
        now = datetime.datetime.now()
        print 'schedules are', settings['SCHEDULES']
        for schedule in settings['SCHEDULES']:
            print 'schedule is', schedule
            if 'next_time' not in schedule:
                print 'updating next time'
                schedule['next_time'] = (
                    now + datetime.timedelta(minutes=schedule['frequency']))
                print 'schedule is', schedule
            if now > schedule['next_time']:
                send_message(schedule['phone_number'],
                             schedule['username'])
                schedule['next_time'] = (
                    now + datetime.timedelta(minutes=schedule['frequency']))
        time.sleep(3)


thread = threading.Thread(target=run_schedule)
thread.daemon = True

train_chatbot()

thread.start()

app.run(debug=True, port=80, use_reloader=False)
