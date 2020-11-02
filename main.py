# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import speech_recognition as sr
import os
import sys
import webbrowser
from os import path
import requests
from pydub import AudioSegment
import config
import telebot
import json

bot = telebot.TeleBot(config.token)
url = '/rest/api/2/issue'
headers = {'Accept': 'application/json', 'Content-Type': 'application/json',
           'Authorization': 'Basic'}


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('priv.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)

    dst = "priv.wav"
    sound = AudioSegment.from_ogg('priv.ogg')
    sound.export(dst, format="wav")

    r = sr.Recognizer()
    with sr.AudioFile(dst) as source:
        audio = r.listen(source)

    try:
        task = r.recognize_google(audio, language="ru-RU").lower()
        print("Вы сказали: " + task)
    except sr.UnknownValueError:
        print("Хуйня какая-то")
        task = command()

    query = {
        "fields": {
            "project":
                {
                    "id": "10603"
                },
            "summary": task,
            "description": "",
            "issuetype": {
                "name": "Task"
            }
        }
    }
    res = requests.post(url, headers=headers, data=json.dumps(query))
    print(res.text)


bot.polling()
