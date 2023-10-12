import telebot
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

import os

import barcode

from barcode import EAN13
from barcode.codex import Code128
from barcode.writer import ImageWriter

import pandas as pd

#Функция проверки подключенных пользователя
def authorization(ID):
    id_clients = 'resource/id_clients.xlsx'
    excel_data_df = pd.read_excel(id_clients)
    for df in excel_data_df['telegram id'].tolist():
        try:
            if df == ID:
                return True
        except:
            return False

#Проверка типа баркода
def control_barcode(msg, chat_id):
    if msg.isdigit() == True and len(msg) == 13:
        Type_EAN13(msg, chat_id)
    else:
        Type_Code128(msg, chat_id)


def Type_Code128(df, chat_id):
    try:
        with open('filestorage' + '/' + df + ".jpeg", "wb") as f:
            Code128(df, writer=ImageWriter()).write(f)
            photo = open('filestorage' + '/' + df + '.jpeg', 'rb')
            bot.send_document(chat_id, photo)
            photo.close()
        os.remove('filestorage' + '/' + df + '.jpeg')
    except barcode.errors.IllegalCharacterError:
        bot.send_message(chat_id, 'Только латинские буквы\n'
                                  'Попробуй ещё раз')
        pass



def Type_EAN13(df, chat_id):
    with open('filestorage' + '/' + df + ".jpeg", "wb") as f:
        EAN13(df, writer=ImageWriter()).write(f)
        photo = open('filestorage' + '/' + df + '.jpeg', 'rb')
        bot.send_document(chat_id, photo)
        photo.close()
    os.remove('filestorage' + '/' + df + '.jpeg')


@bot.message_handler(commands=['start'])
@bot.message_handler(content_types=['text'])
def msg(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, 'Добро пожаловать в\n'
                                          'автоматизированный бот генератор штрихкодов для печати\n\n'
                                          'Вы можете мне отправить в сообщении штрихкод по одному или списком ввиде столба\n\n'
                                          'Например:\n\n'
                                          'WB_12345678 и нажимаете отправить\n\n'
                                          'WB_12345678\n'
                                          'WB_1234648\n'
                                          '1234567890426\n'
                                          '3654896148735 и нажимаете отправить\n'
                                          '\n'
                                          'Данный бот отправит вам фотографии штрихкодов для печати на этикет-принтере\n'
                                          'стикерной машинке')

        if authorization(message.chat.id):
            print(message.chat.id)
            bot.send_message(message.chat.id, 'Прошёл проверку!\n'
                                              'Можешь пользоваться данным ботом!')


        else:
            bot.send_message(message.chat.id, 'Не прошёл проверку')
            bot.send_message(message.chat.id, 'Тебе сюда нельзя. Твой ID: ' + str(message.chat.id))
    else:
        if authorization(message.chat.id):
            lst_message = message.text.split()
            for text in lst_message:
                control_barcode(text, message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Не прошёл проверку')
            bot.send_message(message.chat.id, 'Тебе сюда нельзя. Твой ID: ' + str(message.chat.id))


bot.polling(none_stop=True, interval=0)
