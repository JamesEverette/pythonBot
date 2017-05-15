import os, slackclient, time
import random
import subprocess
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging

# slackbot environment variables
botName = os.environ.get('botName')
botUserOAuthAccessToken = os.environ.get('botUserOAuthAccessToken')
botSlackId = os.environ.get('botSlackId')
botSlackClient = slackclient.SlackClient(botUserOAuthAccessToken)

logging.basicConfig(level=logging.INFO)

bot = ChatBot("Terminal",
    #storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    logic_adapters=[
        "chatterbot.logic.MathematicalEvaluation",
        #"chatterbot.logic.TimeLogicAdapter",
        "chatterbot.logic.BestMatch"
    ],
    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputAdapter",
    output_format="text",
    #database="database.db"
    database="chatterbot-database",
    database_uri='mongodb://localhost:27017/'
)


bot.set_trainer(ChatterBotCorpusTrainer)
bot.train('chatterbot.corpus.english')



def run():
    if botSlackClient.rtm_connect():
        print('Pybot is running...')
        while True:
            eventList = botSlackClient.rtm_read()
            if len(eventList) > 0:
                for event in eventList:
                    #print(event)
                    #Checks that the message did not come from the bot
                    if (event.get('type')) and (event.get('type') == 'message') and not (event.get('user') == botSlackId):
                        #Checks to see if it was a private message or a message directed '@' the bot
                        if event.get('text') and ( (event.get('channel').startswith('D')) or ('<@'+botSlackId+'>' in event.get('text').strip().split()) ):
                            interpret_message(message=event.get('text'), user=event.get('user'), channel=event.get('channel'))
            time.sleep(0.5)
    else:
        print('! Connection failed !')

def interpret_message(message, user, channel):
    if hi(message):
        deliver_message(random.choice(['hi', 'Hi', 'Hello', 'Hey', 'Yo', 'Hiya', 'Herro', 'Heyo', 'Hola', 'Howdy']), channel)
  
    elif bye(message):
        deliver_message(random.choice(['Bye','Later!','ttyl','Toodles!']), channel)
        
    elif command(message):
        execute_command(message, channel)
    else:
        if message.startswith('<'):
            message = message[13:]
        bot_input = bot.get_response(message)
        deliver_message(str(bot_input), channel)

def hi(message):
    print('is hi')
    wordList = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'yo', 'hiya', 'herro', 'heyo', 'hola', 'howdy']
    if any(word in message.lower().split() for word in wordList):
        return True

def bye(message):
    wordList = ['bye', 'later', 'ttyl', 'see ya', 'adios', 'toodles',
 'peace out']
    if any(word in message.lower().split() for word in wordList):
        return True

def command(message):
    if message.startswith('<'):
        message = message[13:]
    if message.lower().startswith('get claim'):
        return True

def deliver_message(message, channel):
    botSlackClient.api_call('chat.postMessage', channel=channel,
                          text=message, as_user=True)

def execute_command(message, channel):
    if message.startswith('<'):
        message = message[13:]
    if message.lower().startswith('get claim'):
        getClaim(message, channel)

def getClaim(message, channel):
    apiLink = open('apiLink.txt', 'r').read().strip()
    apiCredentials = open('apiCredentials.txt', 'r').read().strip()
    print(apiLink)
    claimNumber = message[10:]
    out = subprocess.check_output(['curl','-u', apiCredentials, apiLink + str(claimNumber)])
    deliver_message(out, channel)

if __name__=='__main__':
    run()
