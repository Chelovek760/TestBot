import telebot
from telebot import types
import json
import subprocess
import os
import datetime
#subprocess.Popen('TimeDirect.py',shell=True)
Mes = {'Январь': 1, 'Февраль': 2, 'Март': 3,
       'Апрель': 4, 'Май': 5, 'Июнь': 6,
       'Июль': 7, 'Август': 8, 'Сентябрь': 9,
       'Октябрь': 10, 'Ноябрь': 11,
       'Декабрь': 12}
# os.system('TimeDirect.py')

command = ['Выбрать след. дату', 'Показать все дела']
markup = types.ReplyKeyboardMarkup()
markup1 = types.ReplyKeyboardMarkup(row_width=5)
markup2 = types.ReplyKeyboardMarkup()
Next_Dat = types.KeyboardButton(command[0])
Pokazat_Vse_dela = types.KeyboardButton(command[1])
Yanvar = types.KeyboardButton('Январь')
Fev = types.KeyboardButton('Февраль')
Mart = types.KeyboardButton('Март')
Apr = types.KeyboardButton('Апрель')
May = types.KeyboardButton('Май')
June = types.KeyboardButton('Июнь')
July = types.KeyboardButton('Июль')
Augu = types.KeyboardButton('Август')
Sept = types.KeyboardButton('Сентябрь')
Oct = types.KeyboardButton('Октябрь')
Nov = types.KeyboardButton('Ноябрь')
Dec = types.KeyboardButton('Декабрь')
markup.row(Yanvar, Fev, Mart, Apr)
markup.row(May, June, July, Augu)
markup.row(Sept, Oct, Nov, Dec)
markup2.add(Next_Dat, Pokazat_Vse_dela)
# TODO Проверка на весокосный
Kalend = {'Январь': [i for i in range(1, 32)], 'Февраль': [i for i in range(1, 30)], 'Март': [i for i in range(1, 32)],
          'Апрель': [i for i in range(1, 31)], 'Май': [i for i in range(1, 32)], 'Июнь': [i for i in range(1, 31)],
          'Июль': [i for i in range(1, 32)], 'Август': [i for i in range(1, 32)], 'Сентябрь': [i for i in range(1, 31)],
          'Октябрь': [i for i in range(1, 32)], 'Ноябрь': [i for i in range(1, 31)],
          'Декабрь': [i for i in range(1, 32)]}
token = '495867379:AAGXNK7fwLCtK1IITDbQzItEcnC5hqt3CXA'
bot = telebot.TeleBot(token)
commad_tree = dict()
id_time_work = dict()
id_time = dict()
time_work = dict()
obsh = dict()
works = []
times = []
with open('command_tree.json', 'r', encoding='utf-8') as outfile_c:
    try:
        commad_tree = json.load(outfile_c)
    except json.JSONDecodeError:
        id_time_work = {}
with open('id_bd.json', 'r', encoding='utf-8') as outfile_bd:
    try:
        id_time_work = json.load(outfile_bd)
    except json.JSONDecodeError:
        commad_tree = {}

print(id_time_work)
print(commad_tree)


@bot.message_handler(commands=['settings'])
def Setings(message):
    bot.send_message(message.chat.id,
                     'Введите время и периодичность напоминаний (часы и минуты в минутах через пробел')
    commad_tree.update({str(message.chat.id): 'set'})
    with open('command_tree.json', 'w', encoding='utf-8') as outfile_c:
        json.dump(commad_tree, outfile_c, indent=4,
                  ensure_ascii=False)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Выбери дату, а потом дела, которые надо сделать")
    commad_tree.update({str(message.chat.id): 'start'})
    with open('command_tree.json', 'w', encoding='utf-8') as outfile_c:
        json.dump(commad_tree, outfile_c, indent=4,
                  ensure_ascii=False)
    print(commad_tree)


@bot.message_handler(func=lambda message: str(message.chat.id) not in commad_tree)
def Luboe_Soobshenie(message):
    commad_tree.update({str(message.chat.id): 'error'})
    with open('command_tree.json', 'w', encoding='utf-8') as outfile_c:
        json.dump(commad_tree, outfile_c, indent=4,
                  ensure_ascii=False)
    id_time_work.update({str(message.chat.id): {'time': [], 'set': []}})
    print(commad_tree)
    print(id_time_work)
    Month(message)


with open('command_tree.json', 'r', encoding='utf-8') as outfile_c:
    try:
        commad_tree = json.load(outfile_c)
    except json.JSONDecodeError:
        commad_tree = {}


@bot.message_handler(commands=['stop'])
def OjidanieProchtenia(message):
    with open('id_bd.json', 'r', encoding='utf-8') as outfile_bd:
        try:
            id_time_work = json.load(outfile_bd)
        except json.JSONDecodeError:
            pass
    now = datetime.datetime.now()
    t = id_time_work[str(message.chat.id)]['time']
    print('wait', id_time_work)
    izmenmas = []
    for time in t:
        if now.month > Mes[time['month']]:
            time['do'] = True
            izmenmas.append(time)
        elif now.month == Mes[time['month']]:
            if now.day > int(time['day']):
                time['do'] = True
                izmenmas.append(time)
            elif now.day == int(time['day']):
                if now.hour > int(id_time_work[str(message.chat.id)]['set'][0]):
                    time['do'] = True
                    izmenmas.append(time)
                elif now.hour == int(time['day']):
                    if now.minute >= int(id_time_work[str(message.chat.id)]['set'][1]):
                        time['do'] = True
                        izmenmas.append(time)
                    else:
                        izmenmas.append(time)
                else:
                    izmenmas.append(time)
            else:
                izmenmas.append(time)
        else:
            izmenmas.append(time)

    sett = id_time_work[str(message.chat.id)]['set']
    id_time_work.update({str(message.chat.id): {'time': izmenmas, 'set': sett}})

    with open('id_bd.json', 'w', encoding='utf-8') as outfile_bd:
        json.dump(id_time_work, outfile_bd, indent=4,
                  ensure_ascii=False)
    Month(message)


@bot.message_handler(func=lambda message: commad_tree[str(message.chat.id)] == 'set')
def ApSetings(message):
    try:
        time = message.text.split(' ')
        print(time)
        if int(time[0]) >= 24 or int(time[1]) >= 60:
            bot.send_message(message.chat.id, 'Ошибка в в указании времени')
            Setings(message)
        else:
            obsh = id_time_work[str(message.chat.id)]
            obsh.update({'set': [time[0], time[1]]})
            id_time_work.update({str(message.chat.id): obsh})
            with open('id_bd.json', 'w', encoding='utf-8') as outfile_bd:
                json.dump(id_time_work, outfile_bd, indent=4,
                          ensure_ascii=False)
            commad_tree.update({str(message.chat.id): 'error'})
            with open('command_tree.json', 'w', encoding='utf-8') as outfile_c:
                json.dump(commad_tree, outfile_c, indent=4,
                          ensure_ascii=False)
        Month(message)
        print(id_time_work)
    except BaseException:
        bot.send_message(message.chat.id, 'Ошибка формата ввода')
        Setings(message)


@bot.message_handler(func=lambda message: message.text == command[0])
def Nextdate(message):
    Month(message)


@bot.message_handler(func=lambda message: message.text == command[1])
def VseDelaId(message):
    id_time_work = dict()
    with open('id_bd.json', 'r', encoding='utf-8') as outfile_bd:
        try:
            id_time_work = json.load(outfile_bd)
        except json.JSONDecodeError:
            pass
    if len(id_time_work[str(message.chat.id)]['time']) != 0:
        mes_works = ''
        mes = ''
        count = 0
        for time in id_time_work[str(message.chat.id)]['time']:
            try:
                mes = mes + 'Дата: %s.%s\n' % (time['day'], time['month'])
            except BaseException:
                continue
            for works in time['works']:
                count += 1
                mes_works = mes_works + '[%d]    %s\n' % (count, works)
            mes = mes + mes_works
    else:
        mes = "Счастиливый человек! Нет дел"
    bot.send_message(message.chat.id, mes)


@bot.message_handler(func=lambda message: commad_tree[str(message.chat.id)] == 'month')
def Day(message):
    # for i in range(0,len(Kalend[message.text])//5*5,5):
    #    a1,a2,a3,a4,a5 =types.KeyboardButton(Kalend[message.text][i]),types.KeyboardButton(Kalend[message.text][i+1]),types.KeyboardButton(Kalend[message.text][i+2]),types.KeyboardButton(Kalend[message.text][i+3]),types.KeyboardButton(Kalend[message.text][i+4])
    #   markup1.add(a1,a2,a3,a4,a5)
    try:
        for day in Kalend[message.text]:
            markup1.add(types.KeyboardButton(day))
        bot.send_message(message.chat.id, 'Введи день', reply_markup=markup1)
        commad_tree.update({str(message.chat.id): 'day'})
        with open('command_tree.json', 'w', encoding='utf-8') as outfile_c:
            json.dump(commad_tree, outfile_c, indent=4,
                      ensure_ascii=False)
        times = id_time_work[str(message.chat.id)]['time']
        times.append({'month': message.text})
        sett = id_time_work[str(message.chat.id)]['set']
        id_time_work.update({str(message.chat.id): {'time': times, 'set': sett}})
    except KeyError:
        bot.send_message(message.chat.id, 'Введи месяц', reply_markup=markup)
    print(commad_tree)
    print(id_time_work)


@bot.message_handler(
    func=lambda message: commad_tree[str(message.chat.id)] == 'start' or commad_tree[str(message.chat.id)] == 'error',
    content_types=["text"])
def Month(message):
    bot.send_message(message.chat.id, "Введи месяц", reply_markup=markup)
    commad_tree.update({str(message.chat.id): 'month'})
    with open('command_tree.json', 'w', encoding='utf-8') as outfile_c:
        json.dump(commad_tree, outfile_c, indent=4,
                  ensure_ascii=False)
    print(commad_tree)


@bot.message_handler(func=lambda message: commad_tree[str(message.chat.id)] == 'day')
def Works(message):
    bot.send_message(message.chat.id, 'Введи дела', reply_markup=markup2)
    commad_tree.update({str(message.chat.id): 'works'})
    with open('command_tree.json', 'w', encoding='utf-8') as outfile_c:
        json.dump(commad_tree, outfile_c, indent=4,
                  ensure_ascii=False)
    times = id_time_work[str(message.chat.id)]['time']
    sett = id_time_work[str(message.chat.id)]['set']
    times[len(times) - 1].update({'day': message.text, 'works': []})
    id_time_work.update({str(message.chat.id): {'time': times, 'set': sett}})
    print(commad_tree)
    print(id_time_work)


@bot.message_handler(func=lambda message: commad_tree[str(message.chat.id)] == 'works' and commad_tree[
    str(message.chat.id)] != 'wait' and (
                                                  message.text != command[0] or message.text != command[1]))
def Accept(message):
    times = id_time_work[str(message.chat.id)]['time']
    works = times[len(times) - 1]['works']
    works.append(message.text)
    times[len(times) - 1].update({'works': works, 'do': False})
    sett = id_time_work[str(message.chat.id)]['set']
    id_time_work.update({str(message.chat.id): {'time': times, 'set': sett}})
    with open('id_bd.json', 'w', encoding='utf-8') as outfile_bd:
        json.dump(id_time_work, outfile_bd, indent=4,
                  ensure_ascii=False)
    print(id_time_work)


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        exit()
