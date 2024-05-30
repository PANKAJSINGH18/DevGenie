from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key_here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///leave_management.db"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False)

class Leave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(10), nullable=False, default="pending")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        user = User(username=username, password=generate_password_hash(password), role=role)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/leave_request", methods=["GET", "POST"])
@login_required
def leave_request():
    if request.method == "POST":
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        reason = request.form["reason"]
        leave = Leave(employee_id=current_user.id, start_date=start_date, end_date=end_date, reason=reason)
        db.session.add(leave)
        db.session.commit()
        return redirect(url_for("leave_history"))
    return render_template("leave_request.html")

@app.route("/leave_approval")
@login_required
def leave_approval():
    # TO DO: implement leave approval logic
    pass

@app.route("/leave_history")
@login_required
def leave_history():
    leaves = Leave.query.filter_by(employee_id=current_user.id).all()
    return render_template("leave_history.html", leaves=leaves)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)