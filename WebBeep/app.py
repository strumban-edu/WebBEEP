import sqlite3
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


class RSVP(db.Model):
    __tablename__ = "RSVP"
    rsvp_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("Event.eventid"))
    user_id = db.Column(db.Integer, db.ForeignKey("User.user_id"))



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
    show_mine = request.args.get("my") == "1"
    search = request.args.get("search", "")
    search_field = request.args.get("field", "eventname")

    # Base query joining Location and User for creator username
    query = db.session.query(Event, Location, User)\
        .join(Location, Event.locationid == Location.locationid)\
        .join(User, Event.creatorid == User.user_id)

    # Filter for "My Events Only"
    if current_user.is_authenticated and show_mine:
        query = query.filter(Event.creatorid == current_user.user_id)

    # Search filter
    if search:
        search_pattern = f"%{search}%"
        if search_field == "eventname":
            query = query.filter(Event.eventname.ilike(search_pattern))
        elif search_field == "location":
            query = query.filter(Location.locationname.ilike(search_pattern))
        elif search_field == "creator":
            query = query.filter(User.username.ilike(search_pattern))

    events = query.all()

    #RSVP dictionary
    rsvp_rows = db.session.query(RSVP.event_id, User.username)\
        .join(User, RSVP.user_id == User.user_id)\
        .all()

    event_rsvp_dict = {}
    for event_id, username in rsvp_rows:
        event_rsvp_dict.setdefault(event_id, []).append(username)

    return render_template("WebBeepMockup.html", events=events, event_rsvp_dict=event_rsvp_dict)






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

@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.filter_by(eventid=event_id, creatorid=current_user.user_id).first()

    if not event:
        return "Unauthorized", 403

    # Fetch the location object for the event
    location = Location.query.filter_by(locationid=event.locationid).first()

    if request.method == "POST":
        event.eventname = request.form["eventname"]
        event.category = request.form["category"]
        event.status = request.form["status"]
        event.eventtime = request.form["eventtime"]

        # Update location name if present
        location.locationname = request.form["location_name"]

        db.session.commit()
        return redirect(url_for("index"))

    return render_template("edit_event.html", event=event, location=location)

@app.route("/delete_event/<int:event_id>", methods=["POST"])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)

    if event.creatorid != current_user.user_id:
        abort(403)

    RSVP.query.filter_by(event_id=event.eventid).delete()

    db.session.delete(event)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/rsvp/<int:event_id>", methods=["POST"])
@login_required
def rsvp_event(event_id):
    # Check if RSVP already exists
    rsvp = RSVP.query.filter_by(event_id=event_id, user_id=current_user.user_id).first()
    
    if rsvp:
        # Cancel RSVP
        db.session.delete(rsvp)
    else:
        # Add RSVP
        new_rsvp = RSVP(event_id=event_id, user_id=current_user.user_id)
        db.session.add(new_rsvp)
    
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/profile")
@login_required
def profile():
    created_events = Event.query.filter_by(creatorid=current_user.user_id).all()

    rsvped_events = db.session.query(Event).join(RSVP, Event.eventid == RSVP.event_id)\
                      .filter(RSVP.user_id == current_user.user_id).all()
    
    return render_template("profile.html" ,created_events=created_events, rsvped_events=rsvped_events)


# -------------------------
# MAIN
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)
