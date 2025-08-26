from flask import render_template, redirect, flash, url_for, session
from utils import send_verification_email, confirm_token
from flask_login import login_required, current_user
from project.config import db, app
from project.models import User

@app.route('/verify')
@login_required
def verify():
    user = current_user
    send_verification_email(user)
    flash('Verification email sent! Check your inbox. It will be active for 10 minutes. If not found, check spam folder.', 'info')
    return redirect('/')
    
@app.route('/confirm-email/<token>') 
def confirm_email(token): #when the link is clicked
    email = confirm_token(token, 600) #10 mins expiration time
    if not email: 
        flash('The confirmation link is invalid or has expired. Try again', 'danger')
        return redirect('/')

    user = User.query.filter_by(email=email).first()
    if user.is_email_verified:
        flash('Account is already verified.', 'success')
    else:
        user.is_email_verified = True
        db.session.commit()
        flash('✅ Your account has been verified!', 'success')
    return redirect('/')

@app.route("/verify_phone", methods=["GET"])
@login_required
def verify_phone():
    user=current_user
    if current_user.is_phone_verified==True:
        return redirect("/")
    return render_template("verify_number.html", user=user)

@app.route("/api/set_phone_verified", methods=["POST"])
@login_required
def set_phone_verified():
    user = current_user
    user.is_phone_verified=True
    db.session.commit()
    return {"status": "success"}
