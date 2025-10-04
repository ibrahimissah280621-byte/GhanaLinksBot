import telebot
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("8377765201:AAHv6_h1mqfZlSDEpEe8QgL1EsZP8TVPtSg")
PAYSTACK_SECRET_KEY = os.getenv("Psk_live_3ac39da1898e2f4e58fcaf7a3f692109001fde2a")

bot = telebot.TeleBot(8377765201:AAHv6_h1mqfZlSDEpEe8QgL1EsZP8TVPtSg)

user_data = {}

# ====== START COMMAND ======
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Welcome to GhanaLinksBot 🇬🇭\n\n"
        "We connect people who need services with verified skilled workers, "
        "and also link house owners with tenants.\n\n"
        "💰 Each successful connection costs GHC 10.\n\n"
        "Please choose:\n"
        "1️⃣ /works – For skilled workers\n"
        "2️⃣ /rent – For house owners or tenants\n\n"
        "⚠ Do not send money to anyone before meeting in person!",
        parse_mode="Markdown"
    )


# ====== WORKS FORM ======
@bot.message_handler(commands=['works'])
def works(message):
    bot.send_message(
        message.chat.id,
        "🛠 Please provide your full name:",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, get_fullname)


def get_fullname(message):
    user_data[message.chat.id] = {"full_name": message.text}
    bot.send_message(message.chat.id, "What is your skill or trade?")
    bot.register_next_step_handler(message, get_skill)


def get_skill(message):
    user_data[message.chat.id]["skill"] = message.text
    bot.send_message(message.chat.id, "Enter your location:")
    bot.register_next_step_handler(message, get_location)


def get_location(message):
    user_data[message.chat.id]["location"] = message.text
    bot.send_message(
        message.chat.id,
        "✅ Great! Before your details go live, please pay GHC 10 using Paystack.\n\n"
        "Use this link:\n"
        "👉 https://paystack.com/pay/ghanalinks\n\n"
        "After payment, enter your Paystack Transaction Reference ID below to confirm.",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, verify_payment)


def verify_payment(message):
    reference = message.text.strip()
    headers = {
        "Authorization": f"Bearer {sk_live_3ac39da1898e2f4e58fcaf7a3f692109001fde2a}"
    }
    response = requests.get(
        f"https://api.paystack.co/transaction/verify/{reference}",
        headers=headers
    )

    data = response.json()
    if data.get("status") and data["data"]["status"] == "success":
        bot.send_message(
            message.chat.id,
            "✅ Payment confirmed! Your details have been verified.\n\n"
            "📞 Contact sharing unlocked.\n"
            "You’ll now be matched with clients.",
            parse_mode="Markdown"
        )
        # Here, you can save to a database or notify admin
    else:
        bot.send_message(
            message.chat.id,
            "❌ Payment not verified. Please check your transaction ID and try again."
        )

# ====== RUN BOT ======
print("🤖 GhanaLinksBot with Paystack is running...")
bot.infinity_polling()