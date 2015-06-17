# -*- coding: utf-8 -*-

class Contextual(object):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
