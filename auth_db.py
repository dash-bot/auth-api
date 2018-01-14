import os
import base64
import hashlib
import psycopg2
from datetime import datetime, timedelta
from settings import DB_NAME, DB_URL, DB_UNAME, DB_PASSWORD, TICKET_EXP_TIME


class AuthDBConnection(object):
    """ Class for accessing and persisting a connection to the authorization DB. """
    def __init__(self):
        self._conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s" %
                                      (DB_NAME, DB_UNAME, DB_PASSWORD, DB_URL))

    def issue_ticket(self):
        # generate 1024 random bits
        ticket = os.urandom(128)
        ticket_hash = hashlib.sha256(ticket).digest()

        # determine issue and expiry time
        issued_time = datetime.utcnow()
        expiry_time = issued_time + timedelta(seconds=TICKET_EXP_TIME)

        # log hash of ticket (SHA256), issued time, expiry time
        cur = self._conn.cursor()
        cur.execute("INSERT INTO data_tickets VALUES (%s, %s, %s);",
                    (base64.b64encode(ticket_hash), issued_time, expiry_time))
        self._conn.commit()

        return base64.b64encode(ticket).decode(), issued_time, expiry_time

    def close(self):
        self._conn.close()
