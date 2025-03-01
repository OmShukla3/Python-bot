import telebot
import requests
import os
from flask import Flask, request

# Load Environment Variables (Set these in Render)
BOT_TOKEN = os.getenv("7587696979:AAGSzuEmeaClasgR9QaHHefQK6MKnbAMC00")
OPENROUTER_API_KEY = os.getenv("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")
BOT_PERSONALITY = os.getenv("BOT_PERSONALITY", "You are a helpful AI assistant.")  # Default Prompt

bot = telebot.TeleBot(BOT_TOKEN)

# OpenRouter API Function
def chat_with_ai(user_message):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",  # Model Select कर सकते हो
        "messages": [
            {"role": "system", "content": BOT_PERSONALITY},  # Custom Prompt
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    
    # Debugging Logs (Check in Render)
    print("Status Code:", response.status_code)
    print("Response:", response.json())

    # Handle API Errors
    try:
        result = response.json()
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return f"API Error: {result}"  
    except Exception as e:
        return f"Error: {str(e)}"

# Telegram Message Handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    bot_reply = chat_with_ai(user_text)
    bot.send_message(message.chat.id, bot_reply)

# Flask Server (For Render)
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is Running!"

@app.route("/" + BOT_TOKEN, methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://your-render-url.onrender.com/" + BOT_TOKEN)  # Change URL
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
