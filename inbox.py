# -*- coding: utf-8 -*-
import contextlib
import logging
import email.parser
import os
from imapclient import IMAPClient
from exceptions import HostNotFoundException
from contextual import Contextual


class Inbox(Contextual):
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
        self.client = IMAPClient(host, use_uid=True, ssl=True)  # TODO: treat non-ssl
        msg = self.client.login(account.username, account.password)
        logging.debug(msg)

    def close(self):
        msg = self.client.logout()
        logging.debug(msg)

    def messages(self, folder="INBOX", searchstring="NOT DELETED", keep_listening=True):
        fetchstr = b'RFC822'
        selection = self.client.select_folder(folder)
        logging.debug("IMAP selection: %s", selection)
        uids = self.client.search(searchstring)
        #uids = self.client.search("SUBJECT test")
        logging.debug('Found %i messages matching "%s", %s', len(uids), searchstring, uids)
        for uid in uids:
            logging.debug("Fetching message %s", uid)
            msg_bytes = self.client.fetch(uid, [fetchstr])[uid][fetchstr]
            logging.debug("Parsing fetched message" + os.linesep + "%s", msg_bytes.decode('utf-8'))
            msg = email.parser.BytesParser().parsebytes(msg_bytes)
            yield uid, msg
        logging.debug("All messages fetched")
        if not keep_listening:
            return
        msg = self.client.subscribe_folder(folder)
        logging.debug(str(msg))
        while True:  # TODO: maybe a better abortion mechanism
            logging.debug("Idling...")
            self.client.idle()
            idle = self.client.idle_check()  # TODO: use timeout
            msg = self.client.idle_done()
            # FIXME: while the new messages are fetched, new incoming ones aren't discovered!
            logging.debug(str(msg))
            for msg in idle:
                logging.debug('Idle response: "%"', msg)
                uid, state = msg
                if state == "EXISTS":
                    logging.debug("Fetching message %s", uid)
                    msg_bytes = self.client.fetch(uid, [fetchstr])[uid][fetchstr]
                    logging.debug("Parsing fetched message" + os.linesep + "%s", msg_bytes.decode('utf-8'))
                    msg = email.parser.BytesParser().parsebytes(msg_bytes)
                    yield uid, msg
