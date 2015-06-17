# -*- coding: utf-8 -*-
import logging
from inbox import Inbox
from account import Account

if __name__ == "__main__":
    logging.root.setLevel(logging.DEBUG)

    # Please create an account.txt file containing username and password (one line each)
    with open('account.txt', 'r') as account:
        username = account.readline().strip()
        logging.debug("Username: %s", username)
        password = account.readline().strip()
        logging.debug("Password: %s", password)
        host = account.readline().strip()
        logging.debug("Hostname: %s", host)

    account = Account(username, password)
    with Inbox(account, host) as inbox:
        for uid, msg in inbox.messages():
            print(uid, msg['subject'])
