import logging
import os.path

path_ = os.getcwd() + '//' + aatelebot + '//'
form = logging.Formatter(fmt = '[%(asctime)s | %(levelname)s]: %(message)s', datefmt = '%m.%d.%Y %H:%M:%S')
to_console = logging.StreamHandler()
to_file = logging.FileHandler(filename = path_ + 'testlog.log')
to_console.setFormatter(logging.Formatter() )
to_file.setFormatter(form)
logging.basicConfig(handlers = (to_file, to_console), level=logging.INFO)
logging.info('Started...')