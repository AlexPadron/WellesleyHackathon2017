#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')
import json
import requests
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

sid = 'AC4ce0adbe23b6d20149484a1aba48b227'
key = '3ab2d186deb934743eec888b02b551c4'

google_api_key = 'AIzaSyBBYXg7UcW42aJsb1Wtu8gk9UMmqXqYLNY'

client = Client(sid, key)

client.messages.create(
    to='8604881641',
    from_='8602002058',
    body='hello world'
)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def sms_reply():
    reply = MessagingResponse()
    body = request.values['Body']
    try:
        method, body = body.split(' ', 1)
        # if schema isn't supplied, default to http
        if method == 'GOOGLE':
            content = requests.get(
                'https://www.googleapis.com/customsearch/v1?key='
                + google_api_key +
                '&cx=017576662512468239146:omuauf_lfve&q='
                + body).content
            data = json.loads(content)
            print 'data is', data['items']
            resp = ''
            for item in data['items']:
                resp += item['formattedUrl'] + '\n'
        else:
            resp = 'invalid method {}'.format(method)

        resp = str(resp).replace('\n', '')
        reply.message(resp)
    except Exception as e:
        print type(e)
        print e
        reply.message('an error!')
    finally:
        print 'returning', reply
        return str(reply)

app.run(debug=True, port=80)
