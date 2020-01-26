import time
from tg_bot import *
import os.path
from copy import deepcopy
import version 

#vk_token = '0fd3e5674fbea380f6e011336a3e526fcbf950d3deab8b7dc4c6dff05fb166cac329e91e07715b3b4c206' #елкин
vk_token = 'fd2a30aa9b8b12da50a4413607c997a5a04cdbd8aac9be707353cd3c2f95113753c8a08e4abe7ef5dacf2' #чепига
tg_token = '751858938:AAG4i-Ec8VfdnnQcSOGOOCdVwl6jIH1cv6Y'
path_ = os.getcwd() + '//'
#path_ = ''

Bot = MyBot(vktoken = vk_token, tgtoken = tg_token, v=v)
Bot.get_groups_list()
Bot.get_updates()
Bot.save_groups()

while True:
    Bot.read_groups()
    Bot.update_groups_list()
    Bot.get_updates()
    Bot.save_groups()    

    with open(path_ + 'filter.txt', 'r', encoding = 'utf-8') as file:
        post_filter = eval(file.read() )[0].keys()
    
    try:
        Bot.sendAll('-1001430319971')
        Bot.sendAll('-1001185715274', post_filter)
    except:
        raise RuntimeError
    
    sleep(3600)