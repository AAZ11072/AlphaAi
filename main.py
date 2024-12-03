import telebot
import requests
import json

# Variables
BOT_TOKEN = "7645608540:AAEoUI24MUjXJvTG46SJ5hoOACB-HYSPXY4"
CHAT_API = "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"
BOT_MODE = "act as Alpha the Ai assistant, talk in formal tone"
CHAT_ENGINE = "meta-llama/llama-3-8b-instruct:free"
CHANNEL = "@NatureInsight"


bot = telebot.TeleBot(BOT_TOKEN)
# Initialize a dictionary to hold chat histories for each user
chat_histories = {}

# Define a function to call the OpenRouter API
def call_openrouter_api(user_id, user_message):
    if user_id not in chat_histories:
        chat_histories[user_id] = []

    # Append the new user message to the chat history
    chat_histories[user_id].append({"role": "user", "content": f'({BOT_MODE}), Question:{user_message}' })

    # Prepare the API request data with the chat history
    request_data = {
        "model": CHAT_ENGINE,  # Optional
        "messages": chat_histories[user_id]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {CHAT_API}"
        },
        data=json.dumps(request_data)
    )
    response_json = response.json()
    reply = response_json['choices'][0]['message']['content']

    # Append the bot's reply to the chat history
    chat_histories[user_id].append({"role": "assistant", "content": reply})

    # Limit the chat history to the last 20 messages to avoid large payloads
    chat_histories[user_id] = chat_histories[user_id][-20:]

    return reply

# Function to check if a user is a member of the channel
def is_member(user_id):
    try:
        member_status = bot.get_chat_member(CHANNEL, user_id).status
        return member_status in ['member', 'administrator', 'creator']
    except:
        return False


# Handle the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm Alpha, your Ai assistant. How can I help you today?")
  
# Handle the /about command
@bot.message_handler(commands=['about'])
def send_welcome(message):
    bot.reply_to(message, f"""
*Project Information:-*
Name: Alpha 
Version: 1.2
Model: Meta llama-3-8b-instruct
Updated: 4 December, 2024
Developer: @NatureInsight
   
""", parse_mode="Markdown")
    
    
# Handle text messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    if is_member(user_id):
        # Your bot's response logic here
        user_id = message.chat.id
        user_message = message.text
        # Simulate typing action
        bot_response = call_openrouter_api(user_id, user_message)
        bot.reply_to(message, bot_response, parse_mode="Markdown")
    else:
        bot.reply_to(message, f"Please join our channel {CHANNEL} to use this bot.")
 
        
 #report function       
@bot.message_handler(commands=["report"])
def send_message(message):
    chat_id = "5433178374"
    user = message.from_user.first_name
    bot.reply_to(message,"thanks for your feedback.")
    bot.send_message(chat_id, f"Report from {user} : {message.text}")
    

# Start polling for messages
bot.polling()
