from flask import request, jsonify,render_template, flash, render_template, redirect, url_for
from project.config import app,db,bcrypt
from project.models import Reminders, User
from datetime import datetime
import project.verification_routes
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from project.forms import RegisterForm, LoginForm

# @app.context_processor # to inject currrent_user to all the jinja templates
# def inject_user():
#     return dict(user=current_user)

@app.route("/api/reminders", methods = ["GET"])
@login_required
def get_reminders():
    reminders = Reminders.query.filter_by(user_id=current_user.id).all()
    json_reminders = list(map(lambda x: x.to_json(), reminders))
    print(json_reminders)
    return jsonify({"Reminders":json_reminders})

@app.route("/")
def home():
    if current_user.is_authenticated:   # only if logged in
        return render_template("index.html", user=current_user)
    return render_template("index.html", user=None)

@app.route("/add", methods = ["POST"])
@login_required
def post_reminder():
    data = request.json
    if data:
        task_name = data.get('taskName')
        time = data.get('time')
        date = data.get('date')
        try:
            time_obj = datetime.strptime(time, "%H:%M").time()
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"message": "Invalid date or time format"}), 400

        
        reminder_obj = Reminders(task_name = task_name, time = time_obj, date = date_obj, user_id = current_user.id)

        try:
            db.session.add(reminder_obj)
            db.session.commit()
        except Exception as e:
            return jsonify({"message":str(e)}),400
        return jsonify({'message':"task added"}),201

@app.route("/update/<int:task_id>", methods = ["PATCH"])
@login_required
def update_task(task_id):
    task = Reminders.query.get(task_id)
    if not task:
        return jsonify({"message":"Task not found"}),404
    
    data = request.json
    if data:
        task.task_name = data.get("taskName", task.task_name )
        time = data.get("time", task.time.strftime("%H:%M"))
        date = data.get("date", task.date.strftime("%Y-%m-%d")) # in string
        task.completed = data.get("completed", task.completed)
        try:
            task.time = datetime.strptime(time, "%H:%M").time()
            task.date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"message": "Invalid date or time format"}), 400

    db.session.commit()
    return jsonify({'message':"task updated"}),201

@app.route("/delete/<int:task_id>", methods=["DELETE"])
@login_required
def delete_reminder(task_id):
    task = Reminders.query.get(task_id)
    if not task:
        return jsonify({"message":"Task not found"})
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message":"Deleted"})

#Registration and logins, managed using wtforms in forms.py
#these are the routes that manage them without js 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already exists","warning")
            return redirect(url_for('register'))
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, password_hash=hashed, phone=form.phone.data, email=form.email.data ) #
        db.session.add(user)
        db.session.commit()
        flash("Account created!","success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form) #for GET requests

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash("You Logged in!.","success")
            return redirect(url_for('home'))
        flash("Login details are invalid.","danger")
    return render_template('login.html', form=form) #for GET requests

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully","success")
    return redirect(url_for('login'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run() #set debug=True for dev mode