"""
Descr: various calculations on loans
@author: vitkai
Created: Fri Mar 18 2022 17:46
"""
#import __main__ as main
import json
import logging
import codecs
import ruamel.yaml as yml
import requests
import time
from bs4 import BeautifulSoup
from os import name, path, system


def logging_setup():
    global full_path, filename

    logger = logging.getLogger(__name__)
    filename = path.splitext(__file__)[0] + '.log'
    handler = logging.FileHandler(filename)

    logger.setLevel(logging.DEBUG)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(handler)

    logger.debug("\n{0}Starting program\n{0} Logging was setup".format('-' * 10 + '=' * 10 + '-' * 10 + "\n"))

    return logger


def cls():
    system('cls' if name == 'nt' else 'clear')


def load_cfg():
    global full_path, filename

    """Loads configuration file and initializes variables"""
    # importing configuration
    yaml_name = path.splitext(filename)[0] + ".yml"
    with codecs.open(full_path + yaml_name, 'r', encoding='utf-8') as yaml_file:
        cfg = yml.safe_load(yaml_file)

    return cfg


def check_dict(inp_data, fields):
    #print(f'inp_data:\n {inp_data}')
    #print(f'fields:\n {fields}')

    for key in inp_data:
        if type(inp_data[key]) is dict:
            check_dict(inp_data[key], fields)
        else:
            if key in fields:
                print(f'{key}:\n{inp_data[key]}')


def process_html(inp_data):
    vgm_url = inp_data['url']
    html_text = requests.get(vgm_url).text
    #print(f'html_text:\n{html_text}')
    soup = BeautifulSoup(html_text, 'html.parser')
    #print(f'soup:\n{soup}')

    data = soup.find('script', type='application/json')
    if data is None:
        print(f'Soup returned: {data}')
    else:
        data = json.loads(data.text)
        check_dict(data, inp_data['show_fields'])


def main():
    global full_path, filename
    logger = logging_setup()

    # get script path
    full_path, filename = path.split(__file__)
    full_path = full_path + '/'
    logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))

    src_data = load_cfg()

    cnt = 0
    while cnt < src_data['exit_after_sec']:
        cls()
        process_html(src_data)
        time.sleep(src_data['refresh_delay_sec'])
        cnt += src_data['refresh_delay_sec']

    logger.debug("That's all folks")
    print("\nThat's all folks")


# main starts here
if __name__ == '__main__':
    global full_path, filename
    main()
