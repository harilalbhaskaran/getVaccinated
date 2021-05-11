from telegram.ext import *
from datetime import date       
import requests, json, sys

print("Bot Started...")
def start_command(update, context):
    update.message.reply_text('Enter your PIN code')
def help_command(update, context):
    info = """This bot helps for checking slots availability in your nearest vaccination center.\n
Slots availability data is grabbed from Co-WIN Public APIs (https://apisetu.gov.in/public/api/cowin)

The appointment availability data is cached and may be upto 30 minutes old. Further, these APIs are subject to a rate limit of 100 API calls per 5 minutes per IP. Please consider these points while using the bot."""
    update.message.reply_text(info)
def dev_command(update, context):
    update.message.reply_text('''Maintained by \n-Your Message-''')
def handle_message(update, context):
    user_input = str(update.message.text).lower()
    if user_input in ("hello", "hi"):
        bot_response = "Hello how are you, Please enter your PIN code"
    elif (len(user_input) == 6):
        bot_response = slot_check(user_input)
    else:
        bot_response = "I dont understand, Please enter a valid 6 digit PIN number."
    update.message.reply_text(bot_response)

def error(update, context):
    print(f"Update : {update} caused error -{context.error}")


def main():
    updater = Updater('API-KEY', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start_command))
    dp.add_handler(CommandHandler('help',help_command))
    dp.add_handler(CommandHandler('dev',dev_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

def slot_check(pin):
    dt = date.today()
    today =  dt.strftime("%d-%m-%Y")
#API reference
#https://apisetu.gov.in/public/api/cowin
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
    payload={'pincode':pin,'date': today}
    headers = {'accept-language': 'hi_IN','accept': 'application/json','hostname': 'cdn-api.co-vin.in','user-agent': 'PostmanRuntime/7.26.8'}
    response = requests.request("GET", url, headers=headers, params=payload)
    data =response.json()
    if len(data["centers"]) == 0:
        return "No Vaccination center is available for booking."
    else:
        return response.text

main()