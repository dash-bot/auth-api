import os

# database url and name
DB_NAME = "auth_users"
DB_URL = r'aa1sbw4dz894udn.cv1nhpusk2zj.us-west-2.rds.amazonaws.com'

# database credentials
DB_UNAME = os.environ["DB_UNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]

# expiry time after issue of a ticket (seconds)
TICKET_EXP_TIME = 3 * 60 * 60
