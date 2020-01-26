import vk
import logging
import version
import os

path_ = os.getcwd() + '//' + 'aatelebot' + '//'
vk_token = 'fd2a30aa9b8b12da50a4413607c997a5a04cdbd8aac9be707353cd3c2f95113753c8a08e4abe7ef5dacf2'
session = vk.Session(access_token = vk_token)
v = version.get_version()
form = logging.Formatter(fmt = '[%(asctime)s | %(levelname)s]: %(message)s', datefmt = '%m.%d.%Y %H:%M:%S')
to_console = logging.StreamHandler()
to_file = logging.FileHandler(filename = path_ + 'verify.txt')
to_console.setFormatter(logging.Formatter() )
to_file.setFormatter(form)
logging.basicConfig(handlers = (to_file, to_console), level=logging.INFO)

with open('txt.log') as file:
    lines = file.read().splitlines()
    for line in lines:
        if line[0:5] == 'Saved':
            count = int(line.split()[-1] )
            owner_id = int(line[-4] )

        response = vkapi.wall.get(owner_id = owner_id, v=v)
        actual_count = int(response['items']['count'] )
        if count == actual_count:
            logging.info('Correct count', 'count = ', count, 'actual_count = ', actual_count)
        else: 
            logging.warning('INCORRECT COUNT', 'count = ', count, 'actual_count = ', actual_count)
