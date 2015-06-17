# -*- coding: utf-8 -*-
import contextlib
from inbox import Inbox
from contextual import Contextual


class Account(Contextual):
    def __init__(self, username, password, host=None):
        self.username = username
        self.password = password
        self.inbox = Inbox(self, host)

    def close(self):
        self.inbox.close()
