import vk
import logging
import version

vk_token = '0fd3e5674fbea380f6e011336a3e526fcbf950d3deab8b7dc4c6dff05fb166cac329e91e07715b3b4c206'
session = vk.Session(access_token = vk_token)
v = version.get_version()
form = logging.Formatter(fmt = '[%(asctime)s | %(levelname)s]: %(message)s', datefmt = '%m.%d.%Y %H:%M:%S')
to_console = logging.StreamHandler()
to_file = logging.FileHandler(filename = 'verify.log')
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
