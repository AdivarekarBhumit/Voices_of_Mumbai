from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import copy
import logging

content = {}
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def get_info(update):
    upd = copy.deepcopy(update.to_dict())
    #print(update)
    user_id = update.message.from_user.id
    content['user_id'] = user_id
    print(user_id)
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    content['first_name'] = first_name
    content['last_name'] = last_name
    msg = update.message.text
    print(msg)
    if upd.get('message').get('location') != None:
        lat = upd.get('message').get('location').get('latitude')
        lng = upd.get('message').get('location').get('longitude')
        print(str(lat) + ',' + str(lng))
        content['latlng'] = str(lat) + ',' + str(lng)
    
    if update.message.photo != []:
        print(update.message.photo[-1].get_file()['file_path'])
        content['file_info'] = update.message.photo[-1].get_file()['file_path']

def echo(bot, update):
    if update.message.photo != []:
        get_info(update)
        location_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
        contact_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
        custom_keyboard = [[ location_keyboard, contact_keyboard ]]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=update.message.chat_id, 
                        text="Would you mind sharing your location and contact with me?", 
                        reply_markup=reply_markup)

def location(bot, update):
    get_info(update)

def contact(bot, update):
    upd = update.to_dict()
    phone_no = str('+') + upd.get('message').get('contact').get('phone_number')
    content['contact'] = phone_no
    print(phone_no)
    

def description(bot, update):
    desc = update.to_dict().get('message').get('text')
    content['description'] = desc
    print(content)
    
def main():
    TOKEN = open('./api_key/api.txt').read()

    updater = Updater(TOKEN)

    dp = updater.dispatcher

    #dp.add_handler(MessageHandler(Filters.text | Filters.photo | Filters.location, echo))
    dp.add_handler(MessageHandler(Filters.photo, echo))    
    dp.add_handler(MessageHandler(Filters.location, location))
    dp.add_handler(MessageHandler(Filters.reply, contact))
    dp.add_handler(MessageHandler(Filters.text, description))
    # log all errors
    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
    content = {}