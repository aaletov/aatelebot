import time
from tg_bot import *
import os.path
from copy import deepcopy
import version 

vk_token = process.env.VK_TOKEN
tg_token = process.env.TG_TOKEN
path_ = os.getcwd() + '//' + 'aatelebot' + '//' 
#path_ =  'D:\\py3eg\\tgbots\\aatelebot\\aatelebot\\'

Bot = MyBot(vktoken = vk_token, tgtoken = tg_token, v=v)
Bot.get_groups_list()
Bot.get_updates()
Bot.save_groups()
sleep(600) 

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
