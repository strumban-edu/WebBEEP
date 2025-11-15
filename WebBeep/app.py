from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user, UserMixin
)
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv("dotenv.env")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "devkey")

# -------------------------
# Database CONFIG
# -------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------------------------
# Database MODELS
# -------------------------

class User(UserMixin, db.Model):
    __tablename__ = "User"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def get_id(self):
        # Flask-Login expects a string ID
        return str(self.user_id)


class Location(db.Model):
    __tablename__ = "Location"

    locationid = db.Column(db.Integer, primary_key=True)
    locationname = db.Column(db.String(100), nullable=False)
    locationaddress = db.Column(db.String(200), nullable=True)


class Event(db.Model):
    __tablename__ = "Event"
    eventid = db.Column(db.Integer, primary_key=True)
    eventname = db.Column(db.String(255))
    category = db.Column(db.String(255))
    status = db.Column(db.String(255))
    eventtime = db.Column(db.Time)
    locationid = db.Column(db.Integer, db.ForeignKey("Location.locationid"))
    creatorid = db.Column(db.Integer, db.ForeignKey("User.user_id"))


# -------------------------
# LOGIN SETUP
# -------------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -------------------------
# ROUTES
# -------------------------

@app.route("/")
def index():
    events = db.session.query(Event, Location).join(Location).all()
    return render_template("WebBeepMockup.html", events=events)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check for existing username
        if User.query.filter_by(username=username).first():
            return "Username already taken", 400

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw)

        db.session.add(new_user) 
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            return "Invalid credentials", 400

        login_user(user)
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/add-event", methods=["GET", "POST"])
@login_required
def add_event():
    if request.method == "POST":
        eventname = request.form["eventname"]
        category = request.form["category"]
        status = request.form["status"]
        eventtime = request.form["eventtime"]

        # Location info
        location_name = request.form["location_name"]
        location_address = request.form.get("location_address", "")

        # Create location row
        loc = Location(
            locationname=location_name,
            locationaddress=location_address
        )
        db.session.add(loc)
        db.session.flush()  # get locationid

        # Create event row
        event = Event(
            eventname=eventname,
            category=category,
            status=status,
            eventtime=eventtime,
            creatorid=current_user.user_id,
            locationid=loc.locationid
        )

        db.session.add(event)
        db.session.commit()

        return redirect("/")

    return render_template("add_event.html")


# -------------------------
# MAIN
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)
