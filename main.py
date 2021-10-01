import vk_api
import random
import pymysql

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from pymysql.cursors import DictCursor

token = "135b460f05ba32607385aeaf2bc9d44653feccb50626694edb020c5455c58ac05b266bffcee0829ec784f"
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    db='60971xxx',
    cursorclass=DictCursor
)

with connection:
    cur = connection.cursor()
    cur.execute("SELECT * FROM rating")

    rows = cur.fetchall()

    for row in rows:
        print("{0} {1} {2}".format(row['id'], row['name'], row['description']))

def send_msg(user_id, message, keyboard='{}'):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 1000), "keyboard":keyboard})

# Основной цикл
for event in longpoll.listen():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Сотрудники",color=VkKeyboardColor.PRIMARY, payload={"button": "1"})
    keyboard.add_button("Отделы", color=VkKeyboardColor.PRIMARY, payload={"button": "2"})
    keyboard = keyboard.get_keyboard()
    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:

        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:
            # send_msg(event.user_id, "Пример клавиатуры",keyboard)

            # Сообщение от пользователя
            request = event.text

            # логика ответа
            if request == "привет":
                send_msg(event.user_id, "Хай")
            elif request == "пока":
                send_msg(event.user_id, "Пока((")

            # elif event.message['payload'] == '{"button":"2"}':
            #     send_msg(event.user_id, "Кнопка 2")
            # elif event.message['payload'] == '{"button":"2"}':
            #     send_msg(event.user_id, "Кнопка 1")

            send_msg(event.user_id, "Не поняла вашего ответа......")

