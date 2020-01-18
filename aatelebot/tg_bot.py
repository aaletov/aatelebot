import vk
import requests
import version
import os
import json
from time import time, sleep
from copy import deepcopy, copy

path_ = os.getcwd() + '//' + 'aatelebot' + '//'
#path_ = 'D:\\py3eg\\tgbots\\aatelebot\\aatelebot\\'

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
        self.owner_id = post['owner_id']
        self.date = post['date']
        self.notext = True

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

    def send(self, chat_id, tgapi_url):
        att_count = len(self.videos + self.photos + self.docs)
        params = {'chat_id': chat_id}
        if self.text != '' and att_count == 0:
            sendMessage(self.group_name + '\n\n' + self.text, params, tgapi_url = tgapi_url)

        if self.photos != []:
            sendPhotos(self.photos, params, self.group_name, self.text, tgapi_url = tgapi_url)
            self.notext = True

        if self.videos != []:
            if self.notext:
                sendVideos(self.videos, params, self.group_name, text = '', tgapi_url = tgapi_url)
            else:
                sendVideos(self.videos, params, self.group_name, text = self.text, tgapi_url = tgapi_url)

            self.notext = True

        if self.docs != []:
            if self.notext:
                sendDocuments(self.docs, params, self.group_name, text = '', tgapi_url = tgapi_url)
            else:
                sendDocuments(self.docs, params, self.group_name, text = self.text, tgapi_url = tgapi_url)

    def sendMessage(text, params, tgapi_url):
        method = 'sendMessage'
        params.update({'text':text})
        return(requests.post(tgapi_url + method, params))

    def sendPhotos(photos, params, group_name, tgapi_url, text = ''):
        if len(photos) == 1:
            method = 'sendPhoto'
            params.update({'photo':photos[0], 'caption': group_name + '\n\n' + text})

        else:
            method = 'sendMediaGroup'
            media_array = [
                        {
                            'type':'photo',
                            'media': photos[0], 
                            'caption': group_name + '\n\n' + text 
                            }
                        ]

            for photo in photos[1:]:
                media_array.append(
                    {
                        'type':'photo', 
                        'media':photo 
                        }
                  )
          
            params.update({'media':json.dumps(media_array) } )

        return(requests.post(tgapi_url + method, params))

    def sendVideos(videos, params, group_name, tgapi_url, text = ''):
        if len(videos) == 1:
            method = 'sendVideo'
            version.download_video_vk(videos[0], 'file')
            files = {'video': open(path_ + 'file.mp4', 'rb')} #multipart/form-data
            params.update({'supports_streaming':True, 'caption':group_name + '\n\n' + text})
            try:
                response = requests.post(tgapi_url + method, params = params, files = files )
            except:
                response = None
                print('Upload Error')

            return response

        else:
            method = 'sendMediaGroup'
            media_array = []
            files = {}

            for i in range(len(videos)):
                filename = 'file' + str(i)
                version.download_video_vk(videos[i], filename)
                media_array.append(
                    {
                        'type':'video', 
                        'media':'attach://' + filename + '.mp4', 
                        'supports_streaming': True 
                        } 
                    )
                files.update({filename + '.mp4': open(path_ + filename + '.mp4', 'rb') } )

            media_array[0].update({'caption':group_name + '\n\n' + text} )
            params.update({'media':json.dumps(media_array)} )
            try:
                response = requests.post(tgapi_url + method, params = params, files = files)
            except:
                response = None
                print('Upload Error')

            return response

    def sendDocuments(docs, params, group_name, tgapi_url, text = ''):
        method = 'sendDocument'
        params1 = copy(params)
        params1.update({'document':docs[0], 'caption': group_name + '\n\n' + text})
        responses = [requests.post(tgapi_url + method, params1)]
        for doc in docs[1:]:
            params1 = copy(params)
            params1.update({'document':doc})
            responses.append(requests.post(tgapi_url + method, params1) )

        return responses 


    def __str__(self):
            return str([self.group_name, self.text, str(self.photos), str(self.videos), str(self.docs)])



class Group():

    def __init__(self, groupobj):
        self.owner_id = '-' + str(groupobj['id'])
        self.name = groupobj['name']
        self.last_count = 0

    def get_group_updates(self, vkapi, v):
        try:
            update = vkapi.wall.get(owner_id = self.owner_id, count = 15, v = v)    
        except:
            print('Unable to get %s \'s posts'%self.name)
            return []
        new_count = update['count'] - self.last_count
        self.last_count = update['count']
        
        if update['count'] == 0:
            print('Group %s has no posts'%self.name)
            update_new = []
        else:
            if update['items'][0].get('is_pinned') != 1:
                update_new = update['items'][:new_count]
            elif new_count != 0:
                update_new = update['items'][1:new_count+1]
            else:
                update_new = []
        
        posts = []
        for post in update_new:
            copy_history = post.get('copy_history')
            if copy_history == None:
                posts.append(VkPost(self.name, post = post ) )

        return posts 



class MyBot():
    def __init__(self, vktoken, tgtoken, v):
        self.tgapi_url = "https://api.telegram.org/bot{}/".format(tgtoken)
        session = vk.Session(access_token = vktoken)
        self.vkapi = vk.API(session)
        self.v = v

    def get_groups_list(self, v=self.v):
    #Получение списка сообществ текущего пользователя

        response = self.vkapi.groups.get(v = v, extended = '1')
        self.groups = [Group(i) for i in response['items'] ]

    def update_groups_list(self, v=self.v):
        new_list = self.get_groups_list()
        new_ids = set([i.owner_id for i in new_list] )
        old_ids = set([i.owner_id for i in self.groups] )
        inter = new_ids & old_ids
        sub = new_ids - inter
        leaved = old_ids - inter
        to_delete = []
        for i in range(len(self.groups ) ):
            if self.groups[i].owner_id in leaved:
                to_delete.append(self.groups[i])

        for group in to_delete:
            self.groups.remove(group)
    
        for i in range(len(new_list )):
            if new_list[i].owner_id in sub:
                self.groups.append(new_list[i] )

    def get_updates(self):
        self.posts = []
        for group in self.groups:
            self.posts += group.get_group_updates(self.vkapi, v = self.v)
            sleep(0.33)

        self.posts = self.get_video_info()
        self.posts.sort(key = lambda post: int(post.date) )

    def get_video_info(self, v=self.v):
    #Разовое получение информации о всех видео из апдейта(не вызывается вручную)
        vkp_list = self.posts
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
            response = self.vkapi.video.get(videos = ','.join(part), v=v )
            items += response['items']

        response = self.vkapi.video.get(videos = ','.join(videos_list[len(videos_list)//100*100: ] ), v=v )
        items += response['items']

        for item in items:
            try:
                urls.append(item['player'])
            except:
                urls.append(None)

        for i in posts:
            for j in range(len(vkp_list[i].videos)):
                if urls[0].find('youtube') == -1 and urls[0].find('vimeo') == -1 and urls[0].find('rutube') == -1 and urls[0].find('yandex') == -1 :
                    vkp_list[i].videos[j] = urls.pop(0)
                else:
                    vkp_list[i].videos.pop(0)
                    vkp_list[i].text += '\n' + urls.pop(0)

        return vkp_list

    def sendAll(self, chat_id, filter = []):
        for post in self.posts:
            if str(post.owner_id) not in filter:
                post.send(chat_id)


def get_post_object(url, vkapi, v = v):
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

if __name__ == '__main__':
    last_upd = time()
    groups = get_groups_list()

    while True:
        with open(path_ + 'filter.txt', 'r', encoding = 'utf-8') as file:
            groups = eval(file.read() )

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

