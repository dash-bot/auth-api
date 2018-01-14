"""
REST API for distributing and validating crypto-tickets for authorized users.
Considered the authorization authority for our banking app.
"""
import auth_db
from flask import Flask, g, jsonify
from flask_sslify import SSLify

app = Flask(__name__)
application = app
sslify = SSLify(app)


@app.before_first_request
def get_db():
    db = getattr(g, "_dbconn", None)
    if not db:
        db = g._dbconn = auth_db.AuthDBConnection()
    return db


@app.teardown_appcontext
def shutdown_db(exception):
    print("Shutting down database!")
    db = getattr(g, "_dbconn", None)
    if db:
        db.close()


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

    # TODO: validate input credentials

    # valid login - issue ticket
    ticket, issued, expiry = get_db().issue_ticket()
    return jsonify({
        "ticket": ticket,
        "issued": issued,
        "expiry": expiry,
        "authenticated": True,
        "error": None
    })


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

    # TODO: validate credentials

    # valid login - issue ticket
    ticket, issued, expiry = get_db().issue_ticket()
    return jsonify({
        "ticket": ticket,
        "issued": issued,
        "expiry": expiry,
        "authenticated": True,
        "error": None
    })


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


if __name__ == "__main__":
    app.run()
