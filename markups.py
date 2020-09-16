from telebot import types


func_markup = types.ReplyKeyboardMarkup(True, True)
func_markup.row('/newtask', '/tasks')
func_markup.row('/droptask')
func_markup.row('/help')