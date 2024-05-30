from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key_here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo_list.db"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from models import User, ToDo

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("dashboard"))
        flash("Invalid username or password", "danger")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    todos = ToDo.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", todos=todos)

@app.route("/create_todo", methods=["POST"])
@login_required
def create_todo():
    title = request.form["title"]
    description = request.form["description"]
    due_date = request.form["due_date"]
    todo = ToDo(title=title, description=description, due_date=due_date, user_id=current_user.id)
    db.session.add(todo)
    db.session.commit()
    flash("Todo created successfully", "success")
    return redirect(url_for("dashboard"))

@app.route("/update_todo/<int:todo_id>", methods=["POST"])
@login_required
def update_todo(todo_id):
    todo = ToDo.query.get(todo_id)
    if todo:
        todo.title = request.form["title"]
        todo.description = request.form["description"]
        todo.due_date = request.form["due_date"]
        db.session.commit()
        flash("Todo updated successfully", "success")
    return redirect(url_for("dashboard"))

@app.route("/delete_todo/<int:todo_id>")
@login_required
def delete_todo(todo_id):
    todo = ToDo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        flash("Todo deleted successfully", "success")
    return redirect(url_for("dashboard"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)