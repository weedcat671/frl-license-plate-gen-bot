import telebot
import logging
from japgenerator.generator import plate_generator
from generation_stages import generation_stages
from config import token


# Set your Telegram bot API token in config.py
bot = telebot.TeleBot(token)
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")

# Basic bot answers
answers = {
    "greeting": "Hello, ",
    "cancel": "The request has been canceled",
    "error": "Request error. Make sure you have followed the instructions.",
}

users_sessions = dict()

def say_hello(message, senduser_id):
    gr = answers["greeting"]
    bot.send_message(senduser_id, gr + f"*{message.from_user.first_name}*", parse_mode='Markdown')

def get_keyboard(buttons):
    if buttons is None:
        return telebot.types.ReplyKeyboardRemove()
    kb = telebot.types.ReplyKeyboardMarkup(selective=True)
    for button in buttons:
        kb.row(telebot.types.KeyboardButton(button))
    return kb


# Bot message handlers

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.chat.id)
    say_hello(message, user_id)
    logging.info(f"NEW USER - {user_id}")

@bot.message_handler(commands=['stoprequest'])
def stop_request(message):
    user_id = str(message.chat.id)
    users_sessions.pop(user_id, None)
    bot.send_message(user_id, answers["cancel"], reply_markup=telebot.types.ReplyKeyboardRemove())
    logging.info(f"REQUEST STOP - {user_id}")

@bot.message_handler(commands=['japnumberplate'])
def start_user_session(message):
    user_id = str(message.chat.id)
    users_sessions[user_id] = {'stage': 0}
    bot.send_message(user_id, generation_stages[users_sessions[user_id]['stage']]["reply_text"],
                      reply_markup=get_keyboard(generation_stages[users_sessions[user_id]['stage']]["kb-array"]))
    logging.info(f"SESSION STARTED - {user_id}")

@bot.message_handler(content_types=['text'])
def generation_process(message):
    try:
        user_id = str(message.chat.id)
        users_sessions[user_id][generation_stages[users_sessions[user_id]["stage"]]["datatype"]] = message.text
        logging.info(f"SESSION - {users_sessions[user_id]}")
        if users_sessions[user_id]["stage"] == len(generation_stages) - 1:
            numberplate = plate_generator(
                users_sessions[user_id]["prefecture"],
                users_sessions[user_id]["hiragana"],
                users_sessions[user_id]["veh_type"],
                users_sessions[user_id]["digits"],
            )
            with open("code.txt", "w") as txt_file:
                txt_file.write(numberplate)
            with open("code.txt") as txt_file:
                bot.send_document(user_id, txt_file, reply_markup=telebot.types.ReplyKeyboardRemove())
            logging.info(f"SESSION END - {users_sessions[user_id]}")
            users_sessions.pop(user_id, None)
        else:
            users_sessions[user_id]["stage"] += 1
            bot.send_message(user_id, generation_stages[users_sessions[user_id]['stage']]["reply_text"],
                  reply_markup=get_keyboard(generation_stages[users_sessions[user_id]['stage']]["kb-array"]))
    except:
        bot.send_message(user_id, answers["error"])
        if user_id in users_sessions:
            logging.warning(f"ERROR - {users_sessions[user_id]}")


if __name__ == "__main__":
    logging.info("Bot started")
    bot.infinity_polling()
