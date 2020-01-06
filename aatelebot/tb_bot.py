import vk
import requests
import version
import os
import json
from time import time, sleep

#vk_token = '0fd3e5674fbea380f6e011336a3e526fcbf950d3deab8b7dc4c6dff05fb166cac329e91e07715b3b4c206' #елкин
vk_token = 'da85fb5129c0a72383163ea16171aa2b3d4679595ab28631e1fbe53fa2599f6049c1aae04875b1f65a683' #чепига
tg_token = '751858938:AAG4i-Ec8VfdnnQcSOGOOCdVwl6jIH1cv6Y'
tgapi_url = "https://api.telegram.org/bot{}/".format(tg_token)

session = vk.Session(access_token = vk_token)
vkapi = vk.API(session)
v = version.get_version()

class VkPost():
    def __init__(self, group_name, post = None):
        #
        #post - объект, возвращаемый методом wall.get в поле 'items'
        #
        self.group_name = group_name
        self.text = ''
        self.error = 0
        self.photos = []
        self.videos = []
        self.docs = []
        if post != None:
            if post['marked_as_ads'] == 1:
                self.text = ''
                return

            if post.get('text') != None:
                self.text += post.get('text') 

            attachments = post.get('attachments')
            if attachments != None:
                for attachment in attachments:
                    type = attachment['type']
                    if type == 'photo':
                        self.photos.append(attachment['photo']['sizes'][-1]['url'])

                    elif type == 'video':
                        owner_id = str( attachment['video']['owner_id'] )
                        video_id = str( attachment['video']['id'] )
                        access_key = str( attachment['video']['access_key'] )
                        video = owner_id + '_' + video_id + '_' + access_key 
                        self.videos.append(video)
                        
                    elif type == 'doc':
                        self.docs.append(attachment['doc']['url'])

    def __str__(self):
            return str([self.group_name, self.text, str(self.photos), str(self.videos), str(self.docs)])


def get_post_object(url, v = v):
#Получение объетка по url

    str1 = url.find('wall')
    posts = url[str1+4:]
    str1 = posts.find('_')
    owner_id = posts[:str1]
    post = vkapi.wall.getById(owner_id = owner_id, posts = posts, v=v)
    sleep(0.33)
    group_name = vkapi.groups.getById(group_id = -int(owner_id), v=v)[0]['name']
    try:
        return VkPost(group_name, post = post[0])
    except:
        print(post)
        raise IndexError 

def get_groups_list(v=v):
#Получение списка сообществ текущего пользователя

    groups = vkapi.groups.get(v = v)
    A = []
    IDs = []

    response = vkapi.groups.getById(group_ids = ','.join(map(str,groups['items'])), v=v)

    Names = [group['name'] for group in response]

    for i in range(groups['count']):
        IDs.append(-int(groups['items'][i]) )
    for i in range(len(IDs)):
        A.append({'group_id':IDs[i],'count':0, 'name':Names[i]})

    groups = A 

    return groups 

def get_vk_updates(groups, v=v):
    #Получение обновлений по имеющемуся списку и создание списка из VkPost объектов

    vk_updates = []

    for i in range(len(groups)):
        try:
            update = vkapi.wall.get(owner_id = groups[i]['group_id'], count = 50, v = v)    
        except:
            print('Group %s is blocked'%groups[i]['name'])
        new_count = update['count'] - groups[i]['count']
        update_new = update['items'][:new_count]
        posts = []
        for post in update_new:
            copy_history = post.get('copy_history')
            if copy_history == None:
                posts.append(VkPost(groups[i]['name'], post = post ) )
        
        posts.reverse()
        vk_updates += posts
        groups[i]['count'] = update['count']
        sleep(0.33)

    return(vk_updates , groups)

def get_video_info(vkp_list, v=v):
    #Разовое получение информации о всех видео из апдейта

    urls = []
    videos_list = []
    posts = []
    items = []
    for i in range(len(vkp_list) ):
        videos = vkp_list[i].videos
        if videos != []:
            videos_list += videos
            posts.append(i)
    
    for i in range(len(videos_list)//100):
        part = videos_list[i*100:(i+1)*100]
        response = vkapi.video.get(videos = ','.join(part), v=v )
        items += response['items']

    response = vkapi.video.get(videos = ','.join(videos_list[len(videos_list)//100*100: ] ), v=v )
    items += response['items']

    for item in items:
        try:
            urls.append(item['player'])
        except:
            urls.append(None)

    for i in posts:
        for j in range(len(vkp_list[i].videos)):
            if urls[0].find('vk') != -1:
                vkp_list[i].videos[j] = urls.pop(0)
            else:
                vkp_list[i].videos.pop(0)
                vkp_list[i].text += '\n' + urls.pop(0)

    return vkp_list
        
def send_post(post, tgapi_url = tgapi_url):
    #Сопоставить типы вложений
    
    params = {'chat_id':'-1001430319971'}
    att_count = len(post.videos + post.photos + post.docs)
    if post.text != '' and att_count == 0:
        method = 'sendMessage'
        params.update({'text':post.group_name + '\n\n' + post.text})

    elif att_count == 1:
        params.update({'caption':post.group_name + '\n\n' + post.text})

        if post.photos != []:
            method = 'sendPhoto'
            params.update({'photo':post.photos[0]})

        elif post.videos != []:
            method = 'sendVideo'
            version.download_video_vk(post.videos[0], 'file')
            files = {'video': open(os.getcwd() + '\\file.mp4', 'rb')} # multipart/form-data
            response = requests.post(tgapi_url + method, params = params, files = files )

            return response
        elif post.docs != []:
            method = 'sendDocument'
            params.update({'document':post.docs[0]})

    else:
        if post.photos != []:
            if len(post.photos) > 1:
                method = 'sendMediaGroup'
                media_array = [
                    {
                        'type':'photo',
                        'media': post.photos[0], 
                        'caption': post.group_name + '\n\n' + post.text 
                        }
                    ]

                for photo in post.photos[1:]:
                    media_array.append(
                        {
                            'type':'photo', 
                            'media':photo 
                            }
                        )
          
                params.update({'media':json.dumps(media_array) } )
                return(requests.post(tgapi_url + method, params = params) )

            else:
                post_copy = post
                post_copy.text, post_copy.videos, post_copy.docs = '', [], []
                send_post(group_name = post.group_name, post = post_copy)
            post.text = ''
        
        if post.videos != []:
            if len(post.videos) > 1:
                method = 'sendMediaGroup'
                media_array = []
                files = {}

                for i in range(len(post.videos)):
                    filename = 'file' + str(i)
                    version.download_video_vk(post.videos[i], filename)
                    media_array.append(
                        {
                            'type':'video',
                            'media':'attach://' + filename + '.mp4',
                            'supports_streaming': True
                            }
                        )
                    files.update({filename + '.mp4': open(os.getcwd() + '\\' + filename + '.mp4', 'rb') } )

                media_array[0].update({'caption':post.group_name + '\n\n' + post.text} )
                params.update({'media':json.dumps(media_array)} )
                return(requests.post(tgapi_url + method, params = params, files = files) )

            else:
                post_copy = post
                post_copy.text, post_copy.photos, post_copy.docs = '', [], []
                send_post(group_name = post.group_name, post = post_copy)
            post.text = ''

    return(requests.post(tgapi_url + method, params))

def update_groups_list(groups, v=v):
    new_list = get_groups_list()
    new_ids = set([i['group_id'] for i in new_list] )
    old_ids = set([i['group_id'] for i in groups] )
    inter = new_ids & old_ids
    sub = new_ids - inter
    leaved = old_ids - inter
    for i in range(len(groups ) ):
        if groups[i]['group_id'] in leaved:
            groups[i].pop()
    
    for i in range(len(new_list )):
        in new_list[i]['group_id'] in sub:
            groups.aapend(new_list[i] )

    return groups

groups = get_groups_list()
updates, groups = get_vk_updates(groups)
updates = get_video_info(updates)
updates = []
sleep(300)
updates, groups = get_vk_updates(groups)
updates = get_video_info(updates)
for post in updates:
    print(post, '\n')

if __name__ == '__main__':
    last_upd = time()
    groups = get_groups_list()

    while True:
        if (time() - last_upd)//3600 > 0:
            groups = update_groups_list(groups)

        updates, groups = get_vk_updates(groups)
        updates = get_video_info(updates)
        for post in updates:
            send_post(post)

        sleep(600)

