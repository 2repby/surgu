import vk_api

import psycopg2
import os

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
print(datetime.now())

from message import send_studentgroup_message
from send import send_msg
import database



token = os.getenv('token')
print
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)





# with connection:
#     cur = connection.cursor()
#     cur.execute("SELECT * FROM employee")
#
#     rows = cur.fetchall()
#
#     for row in rows:
#         print("{0} ФИО: {1} {2}".format(row['id'], row['name'], row['phone']))

connection = database.connection

# Основной цикл
with connection:
    for event in longpoll.listen():
        print('Начало цикла')
        send_studentgroup_message(vk)
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("Сотрудники", color=VkKeyboardColor.PRIMARY, payload={"button": "1"})
        keyboard.add_button("Отделы", color=VkKeyboardColor.PRIMARY, payload={"button": "2"})
        keyboard = keyboard.get_keyboard()

        # Если пришло новое сообщение
        if event.type == VkEventType.MESSAGE_NEW:

            # Если оно имеет метку для меня( то есть бота)
            if event.to_me:

                print('Пришло сообщение')

                # send_msg(event.user_id, "Пример клавиатуры",keyboard)

                # Сообщение от пользователя
                request = event.text
                user = vk.method("users.get",{"user_ids":event.user_id,"fields": "photo_id, verified, sex, bdate, city, country, home_town, has_photo, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, domain, has_mobile, contacts, site, education, universities, schools, status, last_seen, followers_count, occupation, nickname, relatives, relation, personal, connections, exports, activities, interests, music, movies, tv, books, games, about, quotes, can_post, can_see_all_posts, can_see_audio, can_write_private_message, can_send_friend_request, is_favorite, is_hidden_from_feed, timezone, screen_name, maiden_name, crop_photo, is_friend, friend_status, career, military, blacklisted, blacklisted_by_me, can_be_invited_group"})[0]
                print(user["first_name"])
                # логика ответа
                if request == "привет":
                    send_msg(vk, event.user_id, "Хай",keyboard)
                elif request == "пока":
                    send_msg(vk, event.user_id, "Пока((",keyboard)

                # elif event.message['payload'] == '{"button":"2"}':
                #     send_msg(event.user_id, "Кнопка 2")
                # elif event.message['payload'] == '{"button":"2"}':
                #     send_msg(event.user_id, "Кнопка 1")
                else:
                        cur = connection.cursor()
                        cur.execute("SELECT *  FROM users WHERE vk_id="+str(event.user_id))
                        n = cur.rowcount
                        cur.close()
                        if n == 0:
                            cur = connection.cursor()
                            cur.execute("INSERT INTO users (first_name, last_name, vk_id) VALUES (%s, %s, %s)",(user["first_name"],user["last_name"],user["id"]))
                            connection.commit()
                            cur.close()
                        # Получение id пользователя - добавленного или имеющегося
                        cur = connection.cursor()
                        cur.execute("SELECT *  FROM users WHERE vk_id=" + str(event.user_id))
                        rows = cur.fetchall()
                        for row in rows:
                            id_user = row[0]
                        print(id_user)

                        # Проверка кодового слова и что кодовое слово было введено пользователем в период урока
                        cur = connection.cursor()
                        print("SELECT *  FROM lesson WHERE LOWER(keyword)='" + request.lower()+"' AND '"\
                                    + str(datetime.now()) + "' > start_at AND '" + str(datetime.now()) + "'< end_at")
                        cur.execute("SELECT *  FROM lesson WHERE LOWER(keyword)='" + request.lower()+"' AND '"\
                                    + str(datetime.now()) + "' > start_at AND '" + str(datetime.now()) + "'< end_at")
                        n = cur.rowcount
                        print ('найдено', n)
                        msg = ''
                        if n > 0:
                            rows = cur.fetchall()
                            row = rows[0]
                            msg = 'Спасибо. Я вижу, что ты был уроке (мероприятии) "' + str(row[1]) + \
                                  '". Тема: "' + str(row[7]) + '". Начало: ' + str(row[4]) + '. Окончание: ' + str(row[5]) +'' \
                                '. Вместе с тобой присутствовали:\n'

                            for row in rows:
                                id_lesson = row[0]
                            print(id_lesson)
                            cur.close()
                            # Проверка на повтороную запись посещения
                            cur = connection.cursor()
                            cur.execute("SELECT *  FROM visit WHERE id_user="+str(id_user) + " AND id_lesson="+str(id_lesson))
                            n = cur.rowcount
                            if n==0:
                                #Добавление посещения
                                cur = connection.cursor()
                                cur.execute("INSERT INTO visit (id_user,id_lesson) VALUES (%s, %s)",(id_user,id_lesson))
                                connection.commit()
                                cur.close()
                            #Вывод списка присуствующих
                            cur = connection.cursor()
                            cur.execute("SELECT *  FROM visit,users WHERE visit.id_user = users.id AND  id_lesson=" + str(id_lesson)+"ORDER BY users.last_name")
                            rows = cur.fetchall()
                            cur.close()
                            print(rows)
                            for row in rows:
                                # print("{0} ФИО: {1} {2}".format(row['id'], row['name'], row['phone']))
                                msg = msg + str(row[4]) + ' ' + str(row[5]) + '\n'
                        else:
                            msg = 'Кодовое слово не найдено или урок (мероприятие) уже завершилось.'
                        msg = msg + '\nПодробная информация на http://metodist.herokuapp.com'
                        send_msg(vk, event.user_id, msg, keyboard)
                        cur = connection.cursor()
                        cur.execute("SELECT E.name EN, E.phone, D.name DN  FROM employee E,department D WHERE E.dep_id = D.id\
                         and (E.name LIKE '%"+request+"%' OR D.name LIKE '%"+request+"%')")

                        rows = cur.fetchall()
                        cur.close()
                        print(rows)
                        for row in rows:
                            # print("{0} ФИО: {1} {2}".format(row['id'], row['name'], row['phone']))
                            send_msg(vk, event.user_id, row[0]+' '+row[1]+' = '+row[2], keyboard)

                # else:
                #     send_msg(event.user_id, "Не поняла вашего ответа......",keyboard)

