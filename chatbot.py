import json

from chatterbot import ChatBot

chatbot = None

def train_chatbot():
    # Initializing ChatBot
    global chatbot
    chatbot = ChatBot(
            'Ron Obvious',
            trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
    )

    # Train based on the english corpus
    chatbot.train("chatterbot.corpus.english")

def reply_to_msg(msg):
    '''Bot that responds'''
    global chatbot
    return chatbot.get_response(msg)

def gen():
    messages = json.loads(open('./settings.json').read())['MESSAGES']
    num = 0
    while num < len(messages):
        yield messages[num]
        num += 1
    while True:
        yield 'foo'

g = gen()

def get_initial_msg(number, username):
	'''
	Initiates conversation with user by going in sequence of predefined chats
	'''
        return next(g)
