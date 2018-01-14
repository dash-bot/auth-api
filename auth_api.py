"""
REST API for distributing and validating crypto-tickets for authorized users.
Considered the authorization authority for our banking app.
"""
from flask import Flask

app = Flask(__name__)
application = app


@app.route('/login/speech', methods=['POST'])
def speech_login():
    """
    Login using a voice clip. This method checks the identity of a speaker and compares against
    speech profiles stored in the auth database.

    Request:
        WAV-encoded audio file
        Container    WAV
        Encoding    PCM
        Rate    16K
        Sample Format    16 bit
        Channels    Mono

    Response:
        {
            "ticket" : base64,
            "issued" : ISO 8601 datetime,
            "expires" : ISO 8601 datetime,
            "authenticated" : true/false,
            "error" : None or message if error
        }
    """
    return "Not implemented"


@app.route("/login/text", methods=['POST'])
def text_login():
    """
    Login using a traditional e-mail/password approach.

    Request:
        e-mail: standard e-mail address
        password: password string

    Response:
        {
            "ticket" : base64,
            "issued" : ISO 8601 datetime,
            "expires" : ISO 8601 datetime,
            "authenticated" : true/false,
            "error" : None or message if error
        }
    """
    return "Not implemented"


@app.route("/auth/check", methods=['GET'])
def check_ticket():
    """
    Checks that a provided ticket exists in the database and has not expired.

    Request:
        ticket: Base64

    Response:
        {
            "authenticated" : True/False
            "error" : None of message if error
        }
    """
    return "Not implemented"

app.run()
