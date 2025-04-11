import telebot
import json
import os
import time
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from functions import addBalance, isExists
from vars import admin_user_id

def register_plugin(bot):

# File to keep track of bonus claims
	BONUS_CLAIMS_FILE = 'bonus_claims.json'
	
	# Ensure the bonus claims file exists
	if not os.path.exists(BONUS_CLAIMS_FILE):
	    with open(BONUS_CLAIMS_FILE, 'w') as f:
	        json.dump({}, f)
	
	# Function to check if the user is eligible for a bonus
	def is_eligible_for_bonus(user_id):
	    with open(BONUS_CLAIMS_FILE, 'r') as f:
	        bonus_claims = json.load(f)
	
	    last_claim_time = bonus_claims.get(str(user_id))
	    current_time = time.time()
	    
	    # 72000 seconds = 5 minutes
	    if last_claim_time is None or (current_time - last_claim_time) > 72000:
	        return True
	    return False
	
	# Function to get remaining time for next bonus
	def get_remaining_time(user_id):
	    with open(BONUS_CLAIMS_FILE, 'r') as f:
	        bonus_claims = json.load(f)
	
	    last_claim_time = bonus_claims.get(str(user_id))
	    current_time = time.time()
	    
	    if last_claim_time is None:
	        return 0
	    
	    elapsed_time = current_time - last_claim_time
	    remaining_time = 72000 - elapsed_time  # 72000 seconds = 15 hours 
	    return max(0, remaining_time)
	
	# Function to update the bonus claim time
	def update_bonus_claim_time(user_id):
	    with open(BONUS_CLAIMS_FILE, 'r') as f:
	        bonus_claims = json.load(f)
	
	    bonus_claims[str(user_id)] = time.time()
	
	    with open(BONUS_CLAIMS_FILE, 'w') as f:
	        json.dump(bonus_claims, f)
	
	@bot.message_handler(func=lambda message: message.text.lower() == "🎁daily bonus")
	def daily_bonus(message):
	    user_id = message.from_user.id
	
	    if is_eligible_for_bonus(user_id):
	        # Add 100 coins to the user's balance
	        addBalance(user_id, 50)
	        # Update the last claim time
	        update_bonus_claim_time(user_id)
	        bot.send_message(user_id, "You have received 50 coins as your daily bonus! please join @thanos_pro ")
	    else:
	        remaining_time = get_remaining_time(user_id)
	        hours, remainder = divmod(remaining_time, 3600)
	        minutes, seconds = divmod(remainder, 60)
	        bot.send_message(user_id, f"You have already claimed your daily bonus. Please try again in {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds.")
	
	
	