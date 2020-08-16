
import argparse
import os
from texts import *
import telebot
from telebot import types # кнопки
from string import Template
from datetime import datetime
from flask import Flask, request
from pymongo import MongoClient
import re

from pipe import *  

import telebot

bot = telebot.TeleBot(TOKEN)
API_TOKEN = os.environ['TOKEN']

server = Flask(__name__)
TELEBOT_URL = 'telebot_webhook/'
BASE_URL = 'https://saltybotessa.herokuapp.com/'

MONGODB_URI = os.environ['MONGODB_URI']

mongo_client = MongoClient(MONGODB_URI)
mongo_db = mongo_client.get_default_database()
mongo_users = mongo_db.get_collection('users')
mongo_logs = mongo_db.get_collection('logs')


def log(message):
    mongo_logs.insert_one({
        "text": message.text,
        "timestamp": datetime.utcnow()
    })

markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
itembtn1 = types.InlineKeyboardMarkup(u'\U0001F636')
itembtn2= types.KeyboardButton(u'\U0001F603')
itembtn22= types.KeyboardButton(u'\U0001F620')
itembtn3 = types.KeyboardButton(text = 'Поделитесь контактом?',request_contact=True)
markup.add(itembtn1, itembtn2,itembtn22, itembtn3)
k = [u'\U0001F601',u'\U0001F603', u'\U0001F636']

# @bot.message_handler(commands=['start','help'])
# def send_welcome(message):
#     bot.reply_to(message,'Howdy, how are you doing?')
    
@bot.message_handler(commands=['start'])
def cmd_start(message):
    
    bot.send_message(message.from_user.id, 'Привет')
    log(message)
    
#     bot.send_message(message.from_user.id, '')
#     log(message)

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Hi there, I am EchoBot. Just say anything nice and I'll say the exact same thing to you!")
    log(message)

#инструкция дл help


@bot.message_handler(func=lambda message: True)
def echo_hello(message):
    l = []
    a = pipe.predict([message.text.lower()])[0]
    if message.text not in k:
        bot.reply_to(message, a)
        l.append(a)
        bot.send_message(message.from_user.id,'жмакните', reply_markup=markup)  
    
    #прописать команду not to use a какое-то количество команд от одного пользователя.
    
    #какие еще методы, помимо message_handlera, есть у питона?

    
    
@server.route('/' + TELEBOT_URL + API_TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=BASE_URL + TELEBOT_URL + API_TOKEN)
    return "!", 200 


parser = argparse.ArgumentParser(description='Run the bot')
parser.add_argument('--poll', action='store_true')
args = parser.parse_args()

if args.poll:
    bot.remove_webhook()
    bot.polling()
else:
    # webhook should be set first
    webhook()
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
