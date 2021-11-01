from main import send_msg
from main import connection

def send_studentgroup_message():
    with connection:
        cur = connection.cursor()
        cur.execute("select vk_id, content from message, studentgroup_message, studentgroup, users \
        where message.id = studentgroup_message.message_id \
        and studentgroup_message.studentgroup_id = studentgroup.id \
        and studentgroup.id = users.studentgroup_id \
        and message.sent_at is null \
        and message.send_at < now()")
        rows = cur.fetchall()
        cur.close()
        for row in rows:
            send_msg(row[0],row[1])
        cur = connection.cursor()
        cur.execute("update message set sent_at = now() where sent_at is null")
        connection.commit()
        cur.close()