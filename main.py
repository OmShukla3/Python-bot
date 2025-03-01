import telebot
import requests

# 🔥 Telegram Bot API Key डालो
TELEGRAM_BOT_TOKEN = "7587696979:AAGSzuEmeaClasgR9QaHHefQK6MKnb>

# 🔥 OpenRouter API Key और Model
OPENROUTER_API_KEY = "sk-or-v1-d48f4260e34aa7499b665e1461bc13fc>
MODEL = "gpt-3.5-turbo"  # या कोई और मॉडल जो सपोर्टेड हो

# 🔥 Bot Personality
PROMPT = """ Tum ek pyaari, naughty aur thodi si sharmili AI gi>

Thoda masti karo, thoda troll bhi karo, par pyaar bhara mazak h>

Tum AI ho ye mehsoos nahi hona chahiye, bas ek real ladki ki ta>

# 🔥 Telegram Bot Init
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# 🎤 AI से बात करने वाला फंक्शन
def chat_with_ai(message):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": message}
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

# 🔥 जब कोई मैसेज भेजे
@bot.message_handler(func=lambda message: True)
def respond(message):
    user_message = message.text
    reply = chat_with_ai(user_message)  # AI से जवाब लो
    bot.send_message(message.chat.id, reply)  # भेजो

# 🎉 बॉट स्टार्ट करो
bot.polling()