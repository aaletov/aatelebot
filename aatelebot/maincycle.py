import time
from tg_bot import *
import os.path
from copy import deepcopy
import shelve
import version 

vk_token = '0fd3e5674fbea380f6e011336a3e526fcbf950d3deab8b7dc4c6dff05fb166cac329e91e07715b3b4c206' #елкин
tg_token = '751858938:AAG4i-Ec8VfdnnQcSOGOOCdVwl6jIH1cv6Y'
path_ = os.getcwd() + '//' + 'aatelebot' + '//' 
#path_ = 'D:\\py3eg\\tgbots\\aatelebot\\aatelebot\\'
v = version.get_version()

Bot = MyBot(vktoken = vk_token, tgtoken = tg_token, v=v)
Bot.get_groups_list()
Bot.update_groups_list()
Bot.get_updates()
Bot.sendAll('-1001430319971')

with shelve.open(path_ + 'botfile', flag ='n') as file:
    file['Bot'] = Bot

while True:
    with shelve.open(path_ + 'botfile', flag ='r') as file:
        Bot = file['Bot']

    Bot.update_groups_list()
    Bot.get_updates()

    with shelve.open(path_ + 'botfile', flag ='w') as file:
        file['Bot'] = Bot

    with open(path_ + 'filter.txt', 'r', encoding = 'utf-8') as file:
        post_filter = eval(file.read() )[0].keys()
    
    try:
        Bot.sendAll('-1001430319971')
        sleep(1)
        Bot.sendAll('-1001185715274', post_filter)
    except:
        raise RuntimeError
    
    sleep(3600)