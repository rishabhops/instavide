import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from functions import getData, cutBalance

# Define the minimum and maximum values for views

# Function to register the bot commands and buttons
def register_plugin(bot):
    @bot.message_handler(func=lambda message: message.text == "🛒order")
    def order_views(message):
        user_id = message.from_user.id
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton("👁‍🗨 Reels View")
       # button2 = KeyboardButton("👁‍🗨 fast views")
       # button3 = KeyboardButton("🙂 reaction+views")
     #   button4 = KeyboardButton("😊 auto views")
        markup.add(button1)
      #  markup.add(button4)
        bot.send_message(user_id, "Please select order type 👇.", reply_markup=markup)
        

    @bot.message_handler(func=lambda message: message.text == "😊 auto views")
    def order_views(message):
        user_id = message.from_user.id
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton("👁‍🗨 set autoview")
        button2 = KeyboardButton("💔 cancel autoview")
        markup.add(button1, button2)
        bot.send_message(user_id, "Please select order type 👇.", reply_markup=markup)
        
        
