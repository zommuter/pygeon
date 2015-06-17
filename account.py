# -*- coding: utf-8 -*-
import contextlib
from inbox import Inbox


class Account(object):
    def __init__(self, username, password, host=None):
        self.username = username
        self.password = password
        self.inbox = Inbox(self, host)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.inbox.close()
