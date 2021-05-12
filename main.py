#!/usr/bin/env python
# This program is dedicated to the public domain under the CC0 license.

from telegram.ext import*
from datetime import date      
import requests, json, logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

print("Bot Started...")
slog ='''Wash Hands, Stay Home, and Flatten the Curve\nBe ready to fight #COVID19'''
info = """You can check the slots availability in your nearest vaccination center with this Bot.\n
Slot database is grabbed from Co-WIN Public APIs (https://apisetu.gov.in/public/api/cowin)\n
The appointment availability data is cached and may be upto 30 minutes old. Please consider this point while using the bot."""

def start_command(update, context):
    update.message.reply_text(info)
    update.message.reply_text(slog)
    update.message.reply_text('Enter your PIN code')
def help_command(update, context):
    update.message.reply_text(info)
def dev_command(update, context):
    update.message.reply_text('''Maintained by \n-Your Message-''')
    update.message.reply_text(slog)
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
    output2 = ""
    output3 = ""

    dt = date.today()
    today =  dt.strftime("%d-%m-%Y")
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
    payload={'pincode':pin,'date': today}
    headers = {'accept-language': 'hi_IN','accept': 'application/json','hostname': 'cdn-api.co-vin.in','user-agent': 'PostmanRuntime/7.26.8'}
    response = requests.request("GET", url, headers=headers, params=payload)
    data =response.json()
    #out = json2html.convert(data)
    if len(data["centers"]) == 0:
        return "No Vaccination center is available for booking."
    else:
        for dt in data['centers']:
            output1 =('Vaccine Center :' + str(dt['center_id']) + " - " + str(dt['name']) + "\n"
            "Block : "+ str(dt['block_name']) + ", District :" + str(dt['district_name']) + ", " + str(dt['state_name']) + ", PIN-" + str(dt['pincode'])
            )
            for dx in dt['sessions']:
                output2 += ('\nDate : ' + str(dx['date']) + ", Min Age Limit :" + str(dx['min_age_limit']) +
                ", Vaccine :" + str(dx['vaccine']) + "\nAvailable slotes : "
                )
                for dz in dx['slots']:
                    output2 += str(dz) + ", "
        return(output1 + "\n" + output2 + "\n\nBook Appointment through CoWin portal\nVisit https://selfregistration.cowin.gov.in")
        #return response.text
main()
