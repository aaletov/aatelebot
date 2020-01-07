import time
from tg_bot import *
import os.path

path_ = os.getcwd() + '//' + 'aatelebot' + '//' 
#path_ = 'D:\\py3eg\\tgbots\\aatelebot\\aatelebot\\'
last_upd = time()
groups = get_groups_list()
groups = update_groups_list(groups)
updates, groups = get_vk_updates(groups)

with open(path_ + 'updated.txt', 'w', encoding = 'utf-8') as file:
    file.write(str(groups) )

while True:
    with open(path_ + 'updated.txt', 'r', encoding = 'utf-8') as file:
        groups = eval(file.read() )

    groups = update_groups_list(groups)

    updates, groups = get_vk_updates(groups)

    with open(path_ + 'updated.txt', 'w', encoding = 'utf-8') as file:
        file.write(str(groups) )

    updates = get_video_info(updates)

    with open(path_ + 'filter.txt', 'r', encoding = 'utf-8') as file:
        post_filter = eval(file.read() )[0].keys()

    for post in updates:
        try:
            sendPost(post, '-1001430319971')
            if str(post.group_id) not in post_filter:
                sendPost(post, '-1001185715274')
            sleep(1)
        except:
                print('API_Error\n', post, '\n\n')
                raise IndexError

    sleep(600)