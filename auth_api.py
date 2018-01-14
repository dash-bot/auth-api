"""
REST API for distributing and validating crypto-tickets for authorized users.
Considered the authorization authority for our banking app.
"""
import auth_db
from flask import Flask, g, jsonify, abort, request
from flask_sslify import SSLify
from speech_verification import VerificationServiceHttpClientHelper
from werkzeug.utils import secure_filename
import os

suscription_key = "4a8368646beb44e29eeafd5f86ec86c9"
speech_verification = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(suscription_key)
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_wav_file(req):
    # check if the post request has the file part
    if 'file' not in req.files:
        return False, "No file in request"
    file = req.files['file']
    print(file.filename)
    if file.filename == '':
        return False, "No filename in request"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        curr_folder = os.path.dirname(os.path.abspath(__file__))
        save_folder = os.path.join(curr_folder, app.config['UPLOAD_FOLDER'])
        filepath = os.path.join(save_folder, filename)
        file.save(filepath)
        #TODO: check if wav file meets requirements
        return True, filepath
    return False, "File not allowed"


@app.route('/create/speech-profile')
def speech_create():
    """
    Create a new speech profile
    :return:
    """
    response = speech_verification.create_profile("en-us")
    id = response.get_profile_id()
    # TODO do stuff with id, we are only returning for testing
    return id


@app.route('/enroll/speech', methods=['POST'])
def speech_enroll():
    """
    Enroll profile using a voice clip. Must be done three successful times
    :return: number of remaining enrollments
    """
    # TODO retrieve id from database instead of getting it from request
    id = request.args.get("id")
    if request.method == 'POST':
        success, response = get_wav_file(request)
        if not success:
            return response
        enroll = speech_verification.enroll_profile(id, response)
        print(enroll.get_remaining_enrollments())
        return str(enroll.get_remaining_enrollments())


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

    # TODO retrieve id from database instead of getting it from request
    id = request.args.get("id")
    if request.method == 'POST':
        success, response = get_wav_file(request)
        if not success:
            return response
        verify = speech_verification.verify_file(response, id)
        return jsonify(result=verify.get_result(), confidence=verify.get_confidence())


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
        ticket: Hex string

    Response:
        {
            "authenticated" : True/False
        }
    """
    try:
        ticket = bytes.fromhex(request.args.get("ticket"))
    except (ValueError, TypeError):
        abort(400)

    authenticated = get_db().check_ticket(ticket)
    return jsonify({
        "authenticated": authenticated
    })


if __name__ == "__main__":
    app.run()
