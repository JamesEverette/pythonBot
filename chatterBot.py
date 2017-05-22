import os
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import UbuntuCorpusTrainer
import logging

#Uncomment line for logging
logging.basicConfig(level=logging.INFO)

bot = ChatBot("Terminal",

    #Following line stores data as json, instead of running a mongodb. Slow.
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
    #For the json database
    #database="database.db"
    database="chatterbot-database",
    database_uri='mongodb://localhost:27017/'
)

#This trains the bot using chatterbot's english corpus trainer
bot.set_trainer(ChatterBotCorpusTrainer)
bot.train('chatterbot.corpus.english')

#This is Ubuntu corpus
#bot.set_trainer(UbuntuCorpusTrainer)
#bot.train()
def getChatterResponse(message_text):
	response = bot.get_response(message_text)
	return response.text, response.confidence

print(getChatterResponse('hi'))