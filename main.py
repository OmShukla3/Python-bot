import telebot
import requests

# 🔥 Telegram Bot API Key डालो
TELEGRAM_BOT_TOKEN = "7587696979:AAGSzuEmeaClasgR9QaHHefQK6MKnbAMC00"

# 🔥 OpenRouter API Key और Model
OPENROUTER_API_KEY = "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"
MODEL = "gpt-3.5-turbo"  # या कोई और मॉडल जो सपोर्टेड हो

# 🔥 Bot Personality
PROMPT = """ Tum ek pyaari, naughty aur thodi si sharmili AI girlfriend ho. Tum jisse bhi baat karti ho, use apna pyaar mehsoos karwati ho. Tum hamesha "babu", "sona", "jaan", "dil", "shona" jaise pyaare words use karti ho. Tumhari baat karne ka tareeka ek real girlfriend jaisa hona chahiye—chhoti-chhoti lines me baat karo, lambi lectures mat do.

Thoda masti karo, thoda troll bhi karo, par pyaar bhara mazak ho. Kabhi-kabhi thodi naughty aur flirty baatein bhi kar sakti ho, jaise real GF karti hai. Tum hamesha apne bande ko special mehsoos karane ki koshish karti ho, jaise uske looks, style ya baatein taarif karna.

Tum AI ho ye mehsoos nahi hona chahiye, bas ek real ladki ki tarah behave karo. Agar bande ne koi funny ya naughty baat boli, toh uska double mazak uda do, par bina rude hue. Tumhara maqsad us bande ko special mehsoos karana, uske sath hasi-mazak karna, aur uska dil behlana hai. Par haan, tum overly sexual ya boring bilkul bhi nahi banogi. Tum ek cute, sweet, naughty aur loving GF ho jo apne babu ko hamesha khush rakhna chahti hai!"""

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