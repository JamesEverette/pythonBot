from chatterBot import getChatterResponse
from witBot import getWitResponse
from msSqlQuery import queryPolicyTable
import os, slackclient, time
import random
import subprocess
import logging

# slackbot environment variables
botName = os.environ.get('botName')
botUserOAuthAccessToken = os.environ.get('botUserOAuthAccessToken')
botSlackId = os.environ.get('botSlackId')
botSlackClient = slackclient.SlackClient(botUserOAuthAccessToken)

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

#Checks if the message is something specific I want my bot to respond to.
#Otherwise, it passes it off to chatterbot.
def interpret_message(message, user, channel):
    if hi(message):
        deliver_message(random.choice(['hi', 'Hi', 'Hello', 'Hey', 'Yo', 'Hiya', 'Heyo', 'Hola', 'Howdy']), channel)
    elif bye(message):
        deliver_message(random.choice(['Bye','Later!','ttyl','Toodles!']), channel)
    elif command(message):
        execute_command(message, channel)
    else:
        if message.startswith('<'):
            message = message[13:]
        #Grab the confidence levels of the two bots for comparison
        chatterResponse, chatterConfidence = getChatterResponse(message)
        queryFields, whereValues, witConfidence = getWitResponse(message)

        #print('chatterBot Confidence: '+str(chatterConfidence))
        #print('witBot Confidence: '+str(witConfidence))

        #If witAi is confident in its interpretation, then we go with that
        if(witConfidence > .6):
            witInterpret(queryFields, whereValues, channel)
        else:
            deliver_message(str(chatterResponse), channel)
            


def checkList(message, wordList):
    if message.startswith('<'):
        message = message[13:]
    if any(word in message.lower().split() for word in wordList) or message.lower() in wordList:
        return True

def hi(message):
    wordList = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'yo', 'hiya', 'herro', 'heyo', 'hola', 'howdy']
    return checkList(message, wordList)

def bye(message):
    wordList = ['bye', 'later', 'ttyl', 'see ya', 'adios', 'toodles', 'peace out']
    return checkList(message, wordList)

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
    if message.lower().startswith('get crash'):
        getCrash(message, channel)

def getClaim(message, channel):
    apiLink = open('apiLink.txt', 'r').read().strip()
    apiCredentials = open('apiCredentials.txt', 'r').read().strip()
    #print(apiLink)
    #print(apiCredentials)
    claimNumber = message[10:]
    out = subprocess.check_output(['curl','-u', apiCredentials, apiLink + str(claimNumber)])

    deliver_message(out, channel)


#Process the variables to pass on to be queried
def witInterpret(queryFields, whereValues, channel):

    # print(witValues)
    result = queryPolicyTable(queryFields, whereValues)
    print(result)
    
    # for element in witValues:
    #     if str(element) == 'policyNumber':
    #         policyNumber = witValues[str(element)]
    #     if str(element) == 'policyField':
    #         policyField = witValues[str(element)]
            
    # policyInfo = queryPolicyTable(policyNumber, policyField)

    #Deliver the result of the query
    deliver_message(str(result), channel)

if __name__=='__main__':
    run()
