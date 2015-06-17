# -*- coding: utf-8 -*-
import contextlib
from inbox import Inbox


class Account(object):
    # This constructor allows using `with Account(...)` such that close() is automatically called for logout
    def __new__(cls, username, password, host=None):
        account = super().__new__(cls)
        account.__init__(username, password, host)
        return contextlib.closing(account)

    def __init__(self, username, password, host=None):
        self.username = username
        self.password = password
        self.inbox = Inbox(self, host).__enter__()

    def close(self):
        self.inbox.close()
