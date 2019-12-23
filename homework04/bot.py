import requests
import configparser
import telebot
from telebot import apihelper
from bs4 import BeautifulSoup
import datetime


config = configparser.ConfigParser()
config['ACCESS'] = {'access_token': '804157838:AAFYh6pgcPNpnzmH10fQwJ0EfOzHo1L_6fk'}
config['DOMAIN'] = {'domain': 'http://www.ifmo.ru/ru/schedule/0'}
with open('example.ini', 'w') as configfile:
    config.write(configfile)
config.read('example.ini')
access_token = config['ACCESS']['access_token']
bot = telebot.TeleBot(access_token)
apihelper.proxy = {'https': 'https://51.158.68.68:8811'}


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config['DOMAIN']['domain'],
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule(web_page, day):
    soup = BeautifulSoup(web_page, 'html5lib')
    if day == 'monday':
        day = "1day"
    if day == 'tuesday':
        day = '2day'
    if day == 'wednesday':
        day = '3day'
    if day == 'thursday':
        day = '4day'
    if day == 'friday':
        day = '5day'
    if day == 'saturday':
        day = "6day"
    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": day})
    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]
    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    auditory_lst = [room.dd.text for room in locations_list]
    locations_list = [room.span.text for room in locations_list]
    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, auditory_lst, locations_list, lessons_list


def parse_near_schedule(web_page, day):
    stat = True
    soup = BeautifulSoup(web_page, 'html5lib')
    if day == 1:
        day = "1day"
    if day == 2:
        day = "2day"
    if day == 3:
        day = "3day"
    if day == 4:
        day = "4day"
    if day == 6:
        day = "6day"
    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": day})
    if schedule_table is None:
        stat = False
        return stat, None
    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]
    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    auditory_lst = [room.dd.text for room in locations_list]
    locations_list = [room.span.text for room in locations_list]
    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]).replace("\t","").replace("\n", "\n")
                    for lesson_info in lessons_list]

    return stat, times_list, auditory_lst, locations_list, lessons_list


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    day, group, week = message.text.split()
    day = day[1:]
    web_page = get_page(group, week)
    times_lst, auditory_lst, locations_lst, lessons_lst = \
        parse_schedule(web_page, day)
    if times_lst is None:
        resp = "Сегодня отдыхаем"
    else:
        resp = ''
    for time, auditory, location, lesson in zip(times_lst, auditory_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>\n {} {} {}\n'.format(time, auditory, location, lesson)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message): #/near K3142
    """ Получить ближайшее занятие """
    day, group = message.text.split()
    week_n = datetime.date.today().isocalendar()[1]
    week_n = week_n % 2 + 2
    web_page = get_page(group, str(week_n))

    time = datetime.datetime.now().time()
    loctime = str(time).split(":")
    acttime = float(loctime[0] + "." + loctime[1])
    day = datetime.datetime.isoweekday(datetime.datetime.today())

    weekend = False
    found = False
    resp = ''

    while True:
        stat, time, auditory, location, lessons = parse_near_schedule(web_page, day)
        if not stat:
            weekend = True
            day += 1
            if day > 7:
                day = 1
                if week_n == 2:
                    week_n = 1
                else:
                    week_n = 2
                web_page = get_page(group, str(week_n))
            continue
        if weekend:
            resp += '<b>{}</b>\n {}, {}\n {}\n'.format(time, auditory, location, lessons)
            break
        i = -1
        for lessn in time:
            i += 1
            lessn = float(str(lessn).split("-")[0].replace(":", "."))
            if acttime < lessn:
                resp += '<b>{}</b>\n {}, {}\n {}\n'.format(time[i], auditory[i], location[i], lessons[i])
                found = True
            elif i == len(time) - 1:
                weekend = True
                day += 1
                if day > 7:
                    day = 1
                    if week_n == 2:
                        week_n = 1
                    else:
                        week_n = 2
                    web_page = get_page(group, str(week_n))
                continue

        if found:
            break

    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message): #/tomorrow K3142
    try:
        _, group = message.text.split()
        week_n = datetime.date.today().isocalendar()[1]
        week_n = week_n % 2 + 1
        web_page = get_page(group, str(week_n))
        day = datetime.datetime.isoweekday(datetime.datetime.today()) + 1
        if day > 7:
            day = 1
        stat, time, auditory, location, lessons = parse_near_schedule(web_page, day)
        if time is None:
            resp = "Сегодня отдыхаем"
        else:
            resp += '<b>{}</b>\n {} {} {}\n'.format(time, auditory, location, lesson)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    except ValueError:
        bot.send_message(message.chat.id, "Завтра нет пар", parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    _, group, week = message.text.split()
    web_page = get_page(group, week)
    soup = BeautifulSoup(web_page, "html5lib")
    resp = ''

    for day in range(1, 7):
        schedule_table = soup.find("table", attrs={"id": str(day) + "day"})
        if schedule_table is None:
            resp += 'В этот день занятий нет \n'
        else:
            times_list = schedule_table.find_all("td", attrs={"class": "time"})
            times_list = [time.span.text for time in times_list]

            locations_list = schedule_table.find_all("td", attrs={"class": "room"})
            auditory_lst = [room.dd.text for room in locations_list]
            locations_list = [room.span.text for room in locations_list]

            lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
            lessons_list = [lesson.text.split() for lesson in lessons_list]
            lessons_list = [' '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

            for time, auditory, location, lesson in zip(times_list, auditory_lst, locations_list, lessons_list):
                resp += '<b>{}</b>, {}, {}, {}\n\n'.format(time, auditory, location, lesson)
        resp += '\n'
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)