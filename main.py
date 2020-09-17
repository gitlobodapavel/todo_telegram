import telebot
import constants
from sqlite_db import (
    get_connection,
    add_task,
    get_tasks,
    drop_task,
)
from markups import func_markup

bot = telebot.TeleBot(constants.API_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, constants.START_MESSAGE, reply_markup=func_markup)


@bot.message_handler(commands=['newtask', ])
def handle_start_help(message):
    bot.send_message(message.chat.id, constants.NEWTASK_MESSAGE)
    bot.register_next_step_handler(message, process_newtask_step)


def process_newtask_step(message):
    chat_id = message.chat.id
    task = message.text

    add_task(get_connection(), chat_id, task)
    bot.send_message(message.chat.id, constants.NEWTASK_END, reply_markup=func_markup)


@bot.message_handler(commands=['tasks', ])
def tasks(message):
    tasks_list = get_tasks(get_connection(), message.chat.id, message.text)
    if tasks_list.__len__() == 0:
        bot.send_message(message.chat.id, constants.HAVE_NO_TASKS)
    else:
        for task in tasks_list:
            bot.send_message(message.chat.id, '[ '+str(task[1])+' ]'+' --> ' + str(task[0]))


@bot.message_handler(commands=['droptask', ])
def detect_task_id(message):
    bot.send_message(message.chat.id, constants.WHAT_TASK_TO_DELETE)
    bot.register_next_step_handler(message, delete_task)


def delete_task(message):
    drop_task(get_connection(), message.text)
    bot.send_message(message.chat.id, constants.DROP_SUCCESS, reply_markup=func_markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
