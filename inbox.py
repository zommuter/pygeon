# -*- coding: utf-8 -*-
import contextlib
import logging
from imapclient import IMAPClient
from exceptions import HostNotFoundException


class Inbox(object):
    # This constructor allows using `with Inbox(...)` such that close() is automatically called for logout
    def __new__(cls, account, host=None):
        inbox = super().__new__(cls)
        inbox.__init__(account, host)
        return contextlib.closing(inbox)

    def __init__(self, account, host=None):
        if host is None or host=="":
            logging.debug("No hostname provided, trying detection from username %s",
                          account.username)
            try:
                host = account.username.split("@")[1]
                logging.debug("Using hostname %s", host)
            except IndexError as e:
                raise HostNotFoundException("No hostname provided, username {0} contains none as well".format(
                    account.username)) from e
        self.client = IMAPClient(host, ssl=True)  # TODO: treat non-ssl
        msg = self.client.login(account.username, account.password)
        logging.debug(msg)

    def close(self):
        msg = self.client.logout()
        logging.debug(msg)
