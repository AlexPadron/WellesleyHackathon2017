from chatterbot import ChatBot

# Initializing ChatBot
chatbot = ChatBot(
    'Ron Obvious',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

# Train based on the english corpus
chatbot.train("chatterbot.corpus.english")

def reply_to_msg(msg):
	'''Bot that responds'''
    return chatbot.get_response(msg)

def get_initial_msg(number, username):
	'''
	Initiates conversation with user by going in sequence of predefined chats
	'''
	messages = []
	num = 0
	while num< len(messages):
		yield messages[num]
		num += 1
