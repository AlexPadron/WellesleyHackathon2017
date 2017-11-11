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
    chatbot.train("chatterbot.corpus.english.drugs")

def reply_to_msg(msg):
    '''Bot that responds'''
    global chatbot
    return chatbot.get_response(msg)


def gen():
    messages = json.loads(open('./settings.json').read())['MESSAGES']
    num = 0
    while True:
        yield messages[num % len(messages)]
        num += 1

g = gen()

def get_initial_msg(number, username):
    '''Initiates conversation with user by going in sequence of predefined chats'''
    global g
    return next(g)
