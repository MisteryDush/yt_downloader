import pytube.exceptions
from pytube import YouTube
from telebot import TeleBot
import os

TOKEN = "" # <<<<<------ your token here
bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def welcome_message(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Hello, just send me a link to YouTube video and then I'll download this video "
                                    "for you!")
    bot.register_next_step_handler(msg, check_link)


def check_link(link):
    chat_id = link.chat.id
    first_part = link.text.split(':')[0]
    if first_part != "https":
        bot.send_message(chat_id, "Oops, that's not a link!")
        msg = bot.send_message(chat_id, "Please send me the link.")
        bot.register_next_step_handler(msg, check_link)
    try:
        yt = YouTube(link.text)
        video = yt.streams.filter(file_extension='mp4').get_highest_resolution()
        bot.send_message(chat_id, "This might take a while, please wait.")
        path = video.download().split('\\')[-1]
        bot.send_video(chat_id, video=open(f'{path}', 'rb'), caption=video.title)
        os.remove(f'{path}')
        msg = bot.send_message(chat_id, "Please send me the link.")
        bot.register_next_step_handler(msg, check_link)
    except pytube.exceptions.RegexMatchError:
        msg = bot.send_message(chat_id, "Invalid link, please send me the working one!")
        bot.register_next_step_handler(msg, check_link)


bot.polling(none_stop=True)
