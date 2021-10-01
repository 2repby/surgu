import vk_api
import random

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType

token = "135b460f05ba32607385aeaf2bc9d44653feccb50626694edb020c5455c58ac05b266bffcee0829ec784f"
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def send_msg(user_id, message, keyboard=None):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 1000), "keyboard":keyboard})

# Основной цикл
for event in longpoll.listen():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("The button",color=VkKeyboardColor.PRIMARY)
    keyboard = keyboard.get_keyboard()
    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:

        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:
            send_msg(event.user_id, "Пример клавиатуры",keyboard)

            # Сообщение от пользователя
            request = event.text

            # логика ответа
            if request == "привет":
                send_msg(event.user_id, "Хай")
            elif request == "пока":
                send_msg(event.user_id, "Пока((")
            else:
                send_msg(event.user_id, "Не поняла вашего ответа...")
