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


def get_page_driver(vgm_url, show_page):
    options = webdriver.ChromeOptions()
    if not show_page:
        options.add_argument("headless")
    chrome_service = Service(ChromeDriverManager().install())
    chrome_service.creationflags = CREATE_NO_WINDOW
    driver_1 = webdriver.Chrome(service=chrome_service, options=options)
    driver_1.get(vgm_url[0])
    driver_2 = webdriver.Chrome(service=chrome_service, options=options)
    driver_2.get(vgm_url[1])

    return driver_1, driver_2


def main():
    global full_path, filename
    global tink_data, vtb_data

    tink_data = []
    vtb_data = []

    logger = logging_setup()

    # get script path
    full_path, filename = path.split(__file__)
    full_path = full_path + '/'
    logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))

    cfg_data = load_cfg()

    page_drivers = get_page_driver(cfg_data['url'], cfg_data['show_page'])

    cnt = 0
    while cnt < cfg_data['exit_after_sec']:
        #cls()
        process_html(page_drivers, cfg_data)
        time.sleep(cfg_data['refresh_delay_sec'])
        cnt += cfg_data['refresh_delay_sec']
        for drv in page_drivers:
            drv.refresh()

    for drv in page_drivers:
        drv.quit()
    logger.debug("That's all folks")
    print("\nThat's all folks")


def process_html(drvr, inp_data):
    global tink_data, vtb_data

    outp = ''
    # html_text_1 = drvr[0].page_source
    # #print(f'html_text:\n{html_text}')
    # soup_1 = BeautifulSoup(html_text_1, 'html.parser')
    #
    # curr = soup_1.findAll('div', attrs={'class': inp_data['tink_div_classes'][0]})
    # price = soup_1.findAll('div', attrs={'class': inp_data['tink_div_classes'][1]})
    # outp += 'Tinkoff:\n' + '---===***'*3 + '===---\n'
    # have_data = False
    # if len(curr) > 1:
    #     tink_data = [curr, price]
    #     have_data = True
    # elif tink_data:
    #     curr = tink_data[0]
    #     price = tink_data[1]
    #     have_data = True
    #
    # if have_data:
    #     for idx, item in enumerate(curr):
    #         outp += f'{item.text}:\n {price[idx*2].text} / {price[idx*2+1].text}\n'
    # outp += '---===***' * 3 + '===---'

    # process VTB
    html_text_2 = drvr[1].page_source
    soup_2 = BeautifulSoup(html_text_2, 'html.parser')
    print(f'soup:\n{soup_2}')

    curr = soup_2.findAll('div', attrs={'class': inp_data['vtb_div_classes'][0]}, partial=True)
    #price = soup_2.findAll('div', attrs={'class': inp_data['vtb_div_classes'][1]})
    #curr = soup_2.select('div[class*=inp_data["vtb_div_classes"][0]]')

    outp += '\n\nVTB:\n' + '---===***'*3 + '===---\n'
    have_data = False
    if len(curr) > 1:
        vtb_data = curr
        have_data = True
    elif vtb_data:
        # restoring previous values if no data received on this run
        curr = vtb_data
        have_data = True

    if have_data:
        for idx, item in enumerate(curr):
            if idx in inp_data['vtb_div_class_ids']:
                outp += f'{item.text}\n'
    outp += '---===***' * 3 + '===---'

    cls()
    for phr in inp_data['to_remove']:
        outp = outp.replace(phr, '')
    outp = '\n'.join(outp.split('\n\n'))
    print(outp)


# main starts here
if __name__ == '__main__':
    global full_path, filename
    main()
