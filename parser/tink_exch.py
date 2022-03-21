"""
Descr: various calculations on loans
@author: vitkai
Created: Fri Mar 18 2022 17:46
"""
#import __main__ as main
import json
import logging
import codecs
import re
import ruamel.yaml as yml
import requests
import time
from bs4 import BeautifulSoup
from os import name, path, system
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from subprocess import CREATE_NO_WINDOW
from webdriver_manager.chrome import ChromeDriverManager

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


def get_page_driver(vgm_url):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    chrome_service = Service(ChromeDriverManager().install())
    chrome_service.creationflags = CREATE_NO_WINDOW
    driver_1 = webdriver.Chrome(service=chrome_service, options=options)
    driver_1.get(vgm_url[0])
    driver_2 = webdriver.Chrome(service=chrome_service, options=options)
    driver_2.get(vgm_url[1])

    return driver_1, driver_2


def process_html(drvr, inp_data):
    html_text_1 = drvr[0].page_source
    html_text_2 = drvr[1].page_source
    #print(f'html_text:\n{html_text}')
    soup_1 = BeautifulSoup(html_text_1, 'html.parser')
    soup_2 = BeautifulSoup(html_text_2, 'html.parser')
    #print(f'soup:\n{soup}')

    curr = soup_1.findAll('div', attrs={'class': inp_data['tink_div_classes'][0]})
    price = soup_1.findAll('div', attrs={'class': inp_data['tink_div_classes'][1]})
    outp = 'Tinkoff:\n' + '---===***'*3 + '===---\n'
    if len(curr) > 1:
        for idx, item in enumerate(curr):
            outp += f'{item.text}:\n {price[idx*2].text} / {price[idx*2+1].text}\n'
    outp += '---===***' * 3 + '===---'

    curr = soup_2.findAll('div', attrs={'class': inp_data['vtb_div_classes'][0]})
    #price = soup_2.findAll('div', attrs={'class': inp_data['vtb_div_classes'][1]})

    outp += '\n\nVTB:\n' + '---===***'*3 + '===---\n'
    if len(curr) > 1:
        #outp += '\ncurr:\n\n'
        for idx, item in enumerate(curr):
            if idx in inp_data['vtb_div_class_ids']:
                outp += f'{item.text}\n'
    outp += '---===***' * 3 + '===---'

    cls()
    for phr in inp_data['to_remove']:
        outp = outp.replace(phr, '')
    outp = '\n'.join(outp.split('\n\n'))
    print(outp)


def main():
    global full_path, filename
    logger = logging_setup()

    # get script path
    full_path, filename = path.split(__file__)
    full_path = full_path + '/'
    logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))

    cfg_data = load_cfg()

    page_drivers = get_page_driver(cfg_data['url'])

    cnt = 0
    while cnt < cfg_data['exit_after_sec']:
        #cls()
        process_html(page_drivers, cfg_data)
        time.sleep(cfg_data['refresh_delay_sec'])
        cnt += cfg_data['refresh_delay_sec']
        page_drivers[0].refresh()
        page_drivers[1].refresh()

    page_driver.quit()
    logger.debug("That's all folks")
    print("\nThat's all folks")


# main starts here
if __name__ == '__main__':
    global full_path, filename
    main()
