import time
from tg_bot import *
import os.path
print('imported')

path_ = os.getcwd() + '//' + 'aatelebot' + '//' 
last_upd = time()
groups = get_groups_list()

while True:
    with open(path_ + 'filter.txt', 'r', encoding = 'utf-8') as file:
        groups = eval(file.read() )
    print(groups)

    if (time() - last_upd)//3600 > 0:
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