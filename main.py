import pandas as pd
df = pd.read('main_df.csv', encoding='utf-8')
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
vectorizer.fit(df.iloc[:,1])
matrix_big = vectorizer.transform(df.iloc[:,1])
from sklearn.decomposition import TruncatedSVD
svd = TruncatedSVD(n_components = 125)
svd.fit(matrix_big)
matrix_small = svd.transform(matrix_big)
import numpy as np
from sklearn.neighbors import BallTree
from sklearn.base import BaseEstimator

def softmax(x):
    #создадим вероятностное распределение 
    proba = np.exp(-x)
    return proba/sum(proba)
class NeighborSampler(BaseEstimator):
    #класс для случайного выбора одного из ближайших соседей
    def __init__(self, k=12, temperature=1.0):
        self.k = k
        self.temperature = temperature
    def fit(self, X, y):
        self.tree_ = BallTree(X)
        self.y_ = np.array(y)
    def predict(self, X, random_state=None):
        distances, indices = self.tree_.query(X, return_distance=True, k=self.k)
        result = []
        for distance, index in zip(distances, indices):
            result.append(np.random.choice(index, p=softmax(distance*self.temperature)))
        return self.y_[result]
from sklearn.pipeline import make_pipeline
ns = NeighborSampler()
ns.fit(matrix_small, df.iloc[:,0])
pipe = make_pipeline(vectorizer, svd, ns)    

import telebot

TOKEN = '1031643376:AAEuEZ8UpoqpC1iLxYueOua_RcIxtMDbOj0'
bot = telebot.TeleBot(TOKEN)

from telebot import types
import datetime

markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
itembtn1 = types.KeyboardButton(u'\U0001F636')
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
def log(message):
    print("<!------!>")
    from datetime import datetime
    print(datetime.now())
    print("Сообщение от {0} {1} (id = {2}) \n {3} \n {4}"
          .format(message.from_user.first_name,               
          #найти тег Текста!пользователя, ответственный за текст
              message.from_user.last_name,
             str(message.from_user.id),
          message.forward_from, message.text))
    
