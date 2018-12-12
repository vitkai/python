#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Bot to reply to Telegram messages.

This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
import codecs
import logging
import __main__ as main
import telegram
import ruamel.yaml as yml
from telegram.error import NetworkError, Unauthorized
from time import sleep
from os import path  # , listdir, remove, makedirs

update_id = None


def main():
    #logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    global logger
    logger = logging_setup()
	
    # get script path
    global full_path
    full_path, filename = path.split(__file__)
    if not full_path == '':
        full_path = full_path + '/'

    #logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))

    params = load_secrets()

    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token
    #bot = telegram.Bot('TOKEN')
    bot = telegram.Bot(params['token'])

    msg = 'Bot run successful'
    logger.info(msg)
    print(msg)
	
    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def echo(bot):
    """Echo the message the user sent."""
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Reply to the message
            update.message.reply_text(update.message.text)
            print(update.message.text)
            logger.debug(update.message.text)

def load_secrets():
    """Loads configuration file and initializes variables"""
    # importing configuration
    yaml_name = 'secrets'
    with codecs.open(full_path + yaml_name, 'r', encoding='utf-8') as yaml_file:
        cfg = yml.safe_load(yaml_file)

    logger.debug("config in {0}:\n{1}".format(yaml_name, cfg))
	
    return cfg


def logging_setup():
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

if __name__ == '__main__':
    main()
