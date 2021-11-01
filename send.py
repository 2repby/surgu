import random

def send_msg(vk, user_id, message, keyboard='{}'):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 1000), "keyboard":keyboard})
