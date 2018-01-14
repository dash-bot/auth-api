import os
import hashlib
import psycopg2
from datetime import datetime, timedelta
from settings import DB_NAME, DB_URL, DB_UNAME, DB_PASSWORD, TICKET_EXP_TIME


class AuthDBConnection(object):
    """ Class for accessing and persisting a connection to the authorization DB. """
    def __init__(self):
        self._conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s" %
                                      (DB_NAME, DB_UNAME, DB_PASSWORD, DB_URL))

    def check_ticket(self, ticket):
        """
        Check whether or not a ticket is valid (not expired and issued by this server).
        :param ticket: Ticket bytes.
        :return True/false validity of the ticket.
        """
        ticket_hash = hashlib.sha256(ticket).digest()

        cur = self._conn.cursor()
        cur.execute("SELECT * FROM data_tickets WHERE ticket_val_hash=%s AND expiry>now();",
                    (psycopg2.Binary(ticket_hash),))

        if cur.fetchone():
            return True
        else:
            return False

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
                    (ticket_hash, issued_time, expiry_time))
        self._conn.commit()

        return ticket.hex(), issued_time, expiry_time

    def close(self):
        self._conn.close()
