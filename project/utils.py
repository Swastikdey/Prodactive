from itsdangerous import URLSafeTimedSerializer as Serializer
#from verification_routes import confirm_email
from flask_mail import Message
from flask import url_for
from project.config import mail, app

def generate_token(email):
    s = Serializer(app.config['SECRET_KEY']) 
    return s.dumps(email, salt='email-confirm')

def confirm_token(token, expiration=1800): # this does the verification
    s = Serializer(app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='email-confirm', max_age=expiration)
    except: # expired or invalid
        return False
    return email


def send_verification_email(user):
    token = generate_token(user.email)
    link = url_for('confirm_email', token=token, _external=True)

    msg = Message('Confirm Your Email',
                  sender='swastik.dey.2003@gmail.com',
                  recipients=[user.email])
    msg.body = f'Click this link to verify your email: {link}'
    mail.send(msg)