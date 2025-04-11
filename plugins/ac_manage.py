import telebot 
import re 
import json 
from telebot import types 
import requests 
import time 
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup 
from functions import insertUser, track_exists, addBalance, cutBalance, getData, addRefCount, isExists, setWelcomeStaus, setReferredStatus 
import telebot 
import os 
import importlib.util 
from vars import admin_user_id 

def register_plugin(bot): 
    @bot.message_handler(commands=['cut']) 
    def cut_coins(message): 
        if message.from_user.id != admin_user_id: 
            bot.reply_to(message, "You are not authorized to use this command.") 
            return 
            
        try: 
            command_parts = message.text.split() 
            
            # Handle reply to user
            if message.reply_to_message:
                if len(command_parts) != 2:
                    raise ValueError("When replying to a user, use format: /cut amount")
                user_id = str(message.reply_to_message.from_user.id)
                amount = float(command_parts[1])
            # Handle direct command
            else:
                if len(command_parts) != 3:
                    raise ValueError("When not replying, use format: /cut userid amount")
                user_id = command_parts[1]
                amount = float(command_parts[2])
                
            # Check if the user exists 
            if not isExists(user_id): 
                bot.reply_to(message, "User does not exist.") 
                return 
                 
            # Cut balance 
            if amount > 0: 
                if cutBalance(user_id, amount): 
                    # Get username for notification
                    try:
                        username = bot.get_chat(user_id).username
                        user_mention = f"@{username}" if username else f"User {user_id}"
                    except:
                        user_mention = f"User {user_id}"
                        
                    bot.reply_to(message, f"{amount} coins deducted from {user_mention}'s balance.") 
                    bot.send_message(user_id, f"{amount} coins have been deducted from your balance.") 
                else:
                    bot.reply_to(message, "User doesn't have enough balance for this deduction.")
            else: 
                bot.reply_to(message, "Amount should be a positive value.") 
                
        except ValueError as ve: 
            bot.reply_to(message, str(ve)) 
        except Exception as e:
            bot.reply_to(message, "An error occurred. Please check the format and try again.")
     
    @bot.message_handler(commands=['add']) 
    def add_coins(message): 
        if message.from_user.id != admin_user_id: 
            bot.reply_to(message, "You are not authorized to use this command.") 
            return 
            
        try: 
            command_parts = message.text.split() 
            
            # Handle reply to user
            if message.reply_to_message:
                if len(command_parts) != 2:
                    raise ValueError("When replying to a user, use format: /add amount")
                user_id = str(message.reply_to_message.from_user.id)
                amount = float(command_parts[1])
            # Handle direct command
            else:
                if len(command_parts) != 3:
                    raise ValueError("When not replying, use format: /add userid amount")
                user_id = command_parts[1]
                amount = float(command_parts[2])
     
            # Check if the user exists 
            if not isExists(user_id): 
                bot.reply_to(message, "User does not exist.") 
                return 
                
            # Add balance 
            if amount > 0: 
                if addBalance(user_id, amount):
                    # Get username for notification
                    try:
                        username = bot.get_chat(user_id).username
                        user_mention = f"@{username}" if username else f"User {user_id}"
                    except:
                        user_mention = f"User {user_id}"
                        
                    bot.reply_to(message, f"{amount} coins added to {user_mention}'s balance.") 
                    bot.send_message(user_id, f"{amount} coins have been added to your balance.") 
            elif amount < 0: 
                current_balance = float(getData(user_id)['balance'])
                if current_balance + amount < 0: 
                    bot.reply_to(message, f"The user's balance cannot go negative.") 
                    return 
                if cutBalance(user_id, abs(amount)): 
                    bot.reply_to(message, f"{abs(amount)} coins deducted from user {user_id}'s balance.") 
                    bot.send_message(user_id, f"{abs(amount)} coins have been deducted from your balance.") 
            else: 
                bot.reply_to(message, "Amount should be a non-zero value.") 
                
        except ValueError as ve: 
            bot.reply_to(message, str(ve)) 
        except Exception as e:
            bot.reply_to(message, "An error occurred. Please check the format and try again.")
