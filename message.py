from send import send_msg
import vk_api

import database
connection = database.connection


def send_studentgroup_message(vk):
    n = 0;
    cur = connection.cursor()
    cur.execute("select * from message where message.sent_at is null and message.send_at <= now()")
    print ("select * from message where message.sent_at is null and message.send_at <= now()")
    n = cur.rowcount
    print('найдено', n, 'сообщений для рассылки')
    if n > 0:
        rows = cur.fetchall()
        cur.close()
        for row in rows:
            cur = connection.cursor()
            cur.execute("select vk_id, content from message, studentgroup_message, studentgroup, users \
            where message.id = studentgroup_message.message_id \
            and studentgroup_message.studentgroup_id = studentgroup.id \
            and studentgroup.id = users.studentgroup_id \
            and message.id = " + str(row[0]))
            rows2 = cur.fetchall()
            cur.close()
            for row2 in rows2:
                print ("Отправка сообщения ", row2[1], "ВК-пользователю", row2[0])
                send_msg(vk,row2[0],row2[1])
            cur = connection.cursor()
            cur.execute("update message set sent_at = now() where message.id = " + str(row[0]))
            connection.commit()
            cur.close()