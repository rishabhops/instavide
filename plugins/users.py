import telebot 
import os 
from functions import insertUser, track_exists, addBalance, cutBalance, getData, addRefCount, isExists, setWelcomeStaus, setReferredStatus 
import json 
from vars import admin_user_id 

# Function to register the bot commands 
def register_plugin(bot): 
    # [Previous /users and /check commands remain the same]
    @bot.message_handler(commands=['users']) 
    def count_users(message): 
        if message.from_user.id != admin_user_id: 
            bot.reply_to(message, "You are not authorized to use this command.") 
            return 
             
        try: 
            with open("user_ids.json", "r") as file: 
                user_ids = json.load(file) 
                total_users = len(user_ids) 
                bot.reply_to(message, f"Total users using the bot: {total_users}") 
        except FileNotFoundError: 
            bot.reply_to(message, "No users found.") 
     
    @bot.message_handler(commands=['check']) 
    def check_user_data(message): 
        if message.from_user.id != admin_user_id: 
            bot.reply_to(message, "You are not authorized to use this command.") 
            return 
        
        try: 
            user_id = message.text.split()[1] 
        except IndexError: 
            bot.reply_to(message, "Please provide a user ID to check.") 
            return 
            
        user_data = getData(user_id) 
        if user_data: 
            try:
                username = bot.get_chat(user_id).username if bot.get_chat(user_id).username else "N/A" 
                bot.reply_to(message, f"User ID: {user_id}\nUsername: @{username}\nBalance: {user_data.get('balance', 'N/A')} coins") 
            except telebot.apihelper.ApiException:
                bot.reply_to(message, f"User ID: {user_id}\nUsername: N/A\nBalance: {user_data.get('balance', 'N/A')} coins")
        else: 
            bot.reply_to(message, "User not found.") 

    @bot.message_handler(commands=['top10'])
    def show_top_users(message):
        # [Previous /top10 command implementation remains the same]
        if message.from_user.id != admin_user_id:
            bot.reply_to(message, "You are not authorized to use this command.")
            return
        
        try:
            account_dir = 'Account'
            if not os.path.exists(account_dir):
                bot.reply_to(message, "No users found in Account directory.")
                return

            users_data = []
            files = os.listdir(account_dir)
            
            if not files:
                bot.reply_to(message, "Account directory is empty.")
                return
                
            for filename in files:
                if filename.endswith('.json'):
                    try:
                        user_id = filename[:-5]
                        user_data = getData(user_id)
                        
                        if not user_data:
                            continue
                            
                        if 'balance' not in user_data:
                            continue
                            
                        balance = float(user_data['balance'])
                        if balance < 0:
                            continue
                            
                        users_data.append({
                            'user_id': user_id,
                            'balance': balance,
                            'total_refs': user_data.get('total_refs', 0),
                            'referred': user_data.get('referred', 0),
                            'welcome_bonus': user_data.get('welcome_bonus', 0)
                        })
                    except Exception as e:
                        continue

            if not users_data:
                bot.reply_to(message, "No valid user balances found.")
                return

            top_users = sorted(users_data, key=lambda x: x['balance'], reverse=True)[:10]
            response = "🏆 Top 10 Users by Balance 🏆\n\n"
            
            for index, user in enumerate(top_users, 1):
                try:
                    try:
                        chat = bot.get_chat(user['user_id'])
                        username = f"@{chat.username}" if chat.username else f"ID: {user['user_id']}"
                    except telebot.apihelper.ApiException:
                        username = f"ID: {user['user_id']}"
                    
                    formatted_balance = "{:,.2f}".format(user['balance'])
                    response += f"#{index} {username}\n"
                    response += f"├ Balance: {formatted_balance} coins\n"
                    response += f"├ Total Referrals: {user['total_refs']}\n"
                    response += f"├ Referred: {'Yes' if user['referred'] == 1 else 'No'}\n"
                    response += f"└ Welcome Bonus: {'Claimed' if user['welcome_bonus'] == 1 else 'Not Claimed'}\n\n"
                    
                except Exception as e:
                    continue

            if response == "🏆 Top 10 Users by Balance 🏆\n\n":
                bot.reply_to(message, "No valid users to display.")
                return
                
            bot.reply_to(message, response)

        except Exception as e:
            error_msg = f"An error occurred while fetching top users: {str(e)}"
            bot.reply_to(message, error_msg)

    @bot.message_handler(commands=['toprefs'])
    def show_top_referrers(message):
        # Check if user is admin
        if message.from_user.id != admin_user_id:
            bot.reply_to(message, "You are not authorized to use this command.")
            return
        
        try:
            # Get all files from Account directory
            account_dir = 'Account'
            if not os.path.exists(account_dir):
                bot.reply_to(message, "No users found in Account directory.")
                return

            # Collect all users and their referral data
            users_data = []
            files = os.listdir(account_dir)
            
            if not files:
                bot.reply_to(message, "Account directory is empty.")
                return
                
            for filename in files:
                if filename.endswith('.json'):
                    try:
                        user_id = filename[:-5]  # Remove .json extension
                        user_data = getData(user_id)
                        
                        if not user_data:
                            continue
                            
                        total_refs = user_data.get('total_refs', 0)
                        if total_refs > 0:  # Only include users with referrals
                            users_data.append({
                                'user_id': user_id,
                                'total_refs': total_refs,
                                'balance': float(user_data.get('balance', 0))
                            })
                    except Exception as e:
                        continue

            if not users_data:
                bot.reply_to(message, "No users with referrals found.")
                return

            # Sort users by referral count in descending order and get top 10
            top_referrers = sorted(users_data, key=lambda x: (x['total_refs'], x['balance']), reverse=True)[:10]

            # Create response message
            response = "👥 Top 10 Referrers 👥\n\n"
            
            for index, user in enumerate(top_referrers, 1):
                try:
                    # Get username
                    try:
                        chat = bot.get_chat(user['user_id'])
                        username = f"@{chat.username}" if chat.username else f"ID: {user['user_id']}"
                    except telebot.apihelper.ApiException:
                        username = f"ID: {user['user_id']}"
                    
                    # Format balance with comma separators
                    formatted_balance = "{:,.2f}".format(user['balance'])
                    
                    response += f"#{index} {username}\n"
                    response += f"├ Total Referrals: {user['total_refs']} users\n"
                    response += f"└ Balance: {formatted_balance} coins\n\n"
                    
                except Exception as e:
                    continue

            if response == "👥 Top 10 Referrers 👥\n\n":
                bot.reply_to(message, "No valid referrers to display.")
                return
                
            bot.reply_to(message, response)

        except Exception as e:
            error_msg = f"An error occurred while fetching top referrers: {str(e)}"
            bot.reply_to(message, error_msg)
