import telebot
from pytube import YouTube
import os

TOKEN = "6507104621:AAFx_1NBY-tfYnQ-E4DJHLV5C1ZlGjyivl8"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "YouTube linkini yuboring.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        msg = bot.reply_to(message, "Yuklanmoqda...")
        try:
            yt = YouTube(url)
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            out_file = video.download()
            with open(out_file, 'rb') as f:
                bot.send_video(message.chat.id, f)
            os.remove(out_file)
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"Xato: {str(e)}", message.chat.id, msg.message_id)
    else:
        bot.reply_to(message, "Faqat YouTube linki bo'lsin.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
