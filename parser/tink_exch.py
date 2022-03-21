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
    #vgm_url = inp_data['url']
    #driver = webdriver.Chrome(r'C:\Users\corvit\Downloads\chromedriver_win32\chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    chrome_service = Service(ChromeDriverManager().install())
    chrome_service.creationflags = CREATE_NO_WINDOW
    driver = webdriver.Chrome(service=chrome_service, options=options)
    driver.get(vgm_url)

    return driver


def process_html(drvr, inp_data):
    html_text = drvr.page_source
    #print(f'html_text:\n{html_text}')
    soup = BeautifulSoup(html_text, 'html.parser')
    #print(f'soup:\n{soup}')

    curr = soup.findAll('div', attrs={'class': inp_data['tink_div_classes'][0]})
    price = soup.findAll('div', attrs={'class': inp_data['tink_div_classes'][1]})
    outp = '\n' + '---===***'*3 + '===---\n' \
            f'{curr[0].text}:\n {price[0].text} / {price[1].text}\n' + \
            f'{curr[1].text}:\n {price[2].text} / {price[3].text}\n' + \
            f'{curr[2].text}:\n {price[4].text} / {price[5].text}\n' + \
           '---===***' * 3 + '===---'
        #print(price)
    cls()
    print(outp)


def main():
    global full_path, filename
    logger = logging_setup()

    # get script path
    full_path, filename = path.split(__file__)
    full_path = full_path + '/'
    logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))

    cfg_data = load_cfg()

    page_driver = get_page_driver(cfg_data['url'])

    cnt = 0
    while cnt < cfg_data['exit_after_sec']:
        #cls()
        process_html(page_driver, cfg_data)
        time.sleep(cfg_data['refresh_delay_sec'])
        cnt += cfg_data['refresh_delay_sec']
        page_driver.refresh()

    page_driver.quit()
    logger.debug("That's all folks")
    print("\nThat's all folks")


# main starts here
if __name__ == '__main__':
    global full_path, filename
    main()
