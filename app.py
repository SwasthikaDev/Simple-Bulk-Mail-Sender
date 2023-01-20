from flask import Flask, render_template, request, redirect, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from models import db, Recipient, User
from forms import LoginForm, TemplateEditorForm, RegisterForm, FileUploadForm, EditUserForm
from config import gmail_user, gmail_password
import smtplib
import struct
import pandas as pd
import time
import auth

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipients.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

scheduler = BackgroundScheduler()

@app.route("/")
@login_required
def index():
    return render_template("index.html")
    
@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = TemplateEditorForm()
    if form.validate_on_submit():
        template = {"subject": form.subject.data, "body": form.body.data}
        session['template'] = template
        return redirect("/preview")
    return render_template("create.html", form=form)

@app.route("/preview")
@login_required
def preview():
    template = session.get('template', None)
    return render_template("preview.html", template=template)

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    form = FileUploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file:
            df = pd.read_excel(file)
            for i in range(len(df)):
                name = df.iloc[i]['Name']
                email = df.iloc[i]['Email']
                priority = df.iloc[i]['Priority']
                recipient = Recipient(
                    name=name, email=email, priority=priority)
                db.session.add(recipient)
            db.session.commit()
            return redirect("/")
    return render_template("upload.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            confirm_password = form.confirm_password.data
            auth.register(email, password, confirm_password)
            return redirect("/login")
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = auth.authenticate(email, password)
            if user and user.is_active:
                login_user(user)
                return redirect("/")
            else:
                return "Invalid credentials or account is inactive"
    return render_template("login.html", form=form)

@app.route("/send", methods=["GET", "POST"])
@login_required
def send():
    template = session.get('template', None)
    if template is None:
        # or some other appropriate action
        flash("Error: Email template not found in session. Please create a template first.")
        return redirect("/create")
    subject = template['subject']
    body = template['body']
    recipients = Recipient.query.order_by(Recipient.priority.asc()).all()
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        for recipient in recipients:
            message = f'Subject: {subject}\n\n{body}'
            server.sendmail(gmail_user, recipient.email, message)
            priority = struct.unpack('<q', recipient.priority)[0]
            print(
                f'Email sent to {recipient.email} with priority {priority}')
        server.close()
    except Exception as e:
        print(f'An error occurred: {e}')
    return redirect("/")

@app.route("/schedule", methods=["GET", "POST"])
@login_required
def schedule():
    # Handle GET requests to display the schedule form
    if request.method == "GET":
        return render_template("schedule.html")

    # Handle POST requests to schedule the emails
    elif request.method == "POST":
        # Retrieve the scheduled time from the form
        scheduled_time = datetime.strptime(request.form.get('scheduled_time'), '%Y-%m-%d %H:%M:%S')
        # Schedule the emails to be sent at the specified time
        schedule_emails(scheduled_time)
        # Redirect the user to the home page
        return redirect("/")


def schedule_emails(scheduled_time):
    # Get the template and recipient information
    template = session.get('template', None)
    if template is None:
        flash("Error: Email template not found in session. Please create a template first.")
        return redirect("/create")
    subject = template['subject']
    body = template['body']
    recipients = Recipient.query.order_by(Recipient.priority.asc()).all()
    try:
        scheduler.add_job(send, 'date', run_date=scheduled_time,
                          args=[subject, body, recipients])
        scheduler.start()
    except:
        flash("Error: Failed to schedule the emails. Please try again.")
        return redirect("/")
    flash("Emails scheduled successfully!")
    return redirect("/")

@app.route("/users")
@login_required
def display_users():
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/edit_user/<user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    user = User.query.get(user_id)
    form = EditUserForm()
    if form.validate_on_submit():
        user.name = form.name.data
      
        user.email = form.email.data
        user.password = form.password.data
        db.session.commit()
        return redirect("/users")
    return render_template("edit_user.html", form=form, user=user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

login_manager.login_view = "login"

if __name__ == "__main__":
    app.run(debug=True)
    while True:
        schedule.run_pending()
        time.sleep(1)
