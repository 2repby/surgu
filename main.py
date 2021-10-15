import os
import vk_api
import random
import psycopg2

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('token')
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


connection = psycopg2.connect(
    host=os.getenv('host'),
    port=os.getenv('port'),
    user=os.getenv('user'),
    password=os.getenv('password'),
    database=os.getenv('database')
)


# with connection:
#     cur = connection.cursor()
#     cur.execute("SELECT * FROM employee")
#
#     rows = cur.fetchall()
#
#     for row in rows:
#         print("{0} ФИО: {1} {2}".format(row['id'], row['name'], row['phone']))

def send_msg(user_id, message, keyboard='{}'):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 1000), "keyboard":keyboard})

# Основной цикл
with connection:
    for event in longpoll.listen():
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("Сотрудники", color=VkKeyboardColor.PRIMARY, payload={"button": "1"})
        keyboard.add_button("Отделы", color=VkKeyboardColor.PRIMARY, payload={"button": "2"})
        keyboard = keyboard.get_keyboard()

        # Если пришло новое сообщение
        if event.type == VkEventType.MESSAGE_NEW:

            # Если оно имеет метку для меня( то есть бота)
            if event.to_me:
                # send_msg(event.user_id, "Пример клавиатуры",keyboard)

                # Сообщение от пользователя
                request = event.text
                print (event)

                # логика ответа
                if request == "привет":
                    send_msg(event.user_id, "Хай",keyboard)
                elif request == "пока":
                    send_msg(event.user_id, "Пока((",keyboard)

                # elif event.message['payload'] == '{"button":"2"}':
                #     send_msg(event.user_id, "Кнопка 2")
                # elif event.message['payload'] == '{"button":"2"}':
                #     send_msg(event.user_id, "Кнопка 1")
                else:

                        cur = connection.cursor()
                        cur.execute("SELECT E.name EN, E.phone, D.name DN  FROM employee E,department D WHERE E.dep_id = D.id\
                         and (E.name LIKE '%"+request+"%' OR D.name LIKE '%"+request+"%')")

                        rows = cur.fetchall()
                        print(rows)
                        for row in rows:
                            # print("{0} ФИО: {1} {2}".format(row['id'], row['name'], row['phone']))
                            send_msg(event.user_id, row[0]+' '+row[1]+' = '+row[2], keyboard)

                # else:
                #     send_msg(event.user_id, "Не поняла вашего ответа......",keyboard)

