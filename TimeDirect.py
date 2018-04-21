import datetime
import time
import json
import telebot

Mes = {'Январь': 1, 'Февраль': 2, 'Март': 3,
       'Апрель': 4, 'Май': 5, 'Июнь': 6,
       'Июль': 7, 'Август': 8, 'Сентябрь': 9,
       'Октябрь': 10, 'Ноябрь': 11,
       'Декабрь': 12}
commad_tree = {}
VramOjid = dict()
token = '495867379:AAGXNK7fwLCtK1IITDbQzItEcnC5hqt3CXA'
bot = telebot.TeleBot(token)


def kusok():
    commad_tree.update({us: 'wait'})
    with open('command_tree.json', 'w', encoding='utf-8') as outfile_c:
        json.dump(commad_tree, outfile_c, indent=4, ensure_ascii=False)
    count = 0
    mes_works = 'Дата: %s.%s\n' % (times['day'], times['month'])
    for works in times['works']:
        count += 1
        mes_works = mes_works + '[%d]    %s\n' % (count, works)
    bot.send_message(int(us),
                     'Ваши дела \n.Для того чтобы отметить прочтение отправьте /stop \n' + mes_works)


def datesravn(now,times,dannye,Mes,us):
    try:
        if now.month > Mes[times['month']] and times['do'] == False:
            kusok()
        elif now.month == Mes[times['month']]and times['do'] == False:
            if now.day > int(times['day'])and times['do'] == False:
                kusok()
            elif now.day == int(times['day']):
                if now.hour > int(dannye[us]['set'][0])and times['do'] == False:
                    kusok()
                elif now.hour == int(times['day'])and times['do'] == False:
                    if now.minute >= int(dannye[us]['set'][1])and times['do'] == False:
                        kusok()
    except KeyError:
        bot.send_message(int(us),'Ошибка структуры данных')

while True:
    now = datetime.datetime.now()
    print(now.date(), now.time())

    with open('id_bd.json', 'r', encoding='utf-8') as outfile_bd:
        try:
            dannye = json.load(outfile_bd)
        except json.JSONDecodeError:
            dannye = {}
    for us in dannye:
        mes_works = ''
        for times in dannye[us]['time']:
            print('v baze', us, Mes[times['month']], int(times['day']), int(dannye[us]['set'][0]),
                  int(dannye[us]['set'][1]),
                  times['do'])
            print('seqcas', us, now.month, now.day, now.hour, int(dannye[us]['set'][1]), times['do'])
            datesravn(now,times,dannye,Mes,us)
    time.sleep(60)
