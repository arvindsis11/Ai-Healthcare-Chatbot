from chatterbot import ChatBot, utils
from chatterbot.trainers import ListTrainer
import os

try:
    os.remove("db.sqlite3")
    print("Old database removed. Training new database")
except FileNotFoundError:
    print('No database found. Creating new database.')

english_bot = ChatBot('Bot')
english_bot.set_trainer(ListTrainer)

for file in os.listdir('data'):
    print('Training using ' + file)
    convData = open('data/' + file, 'r').readlines()
    english_bot.train(convData)
    print("Training completed for " + file)
