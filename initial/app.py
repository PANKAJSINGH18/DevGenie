from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key_here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("index"))
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
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/todo", methods=["GET", "POST"])
@login_required
def todo():
    if request.method == "POST":
        title = request.form["title"]
        todo = Todo(title=title, user_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("todo"))
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template("todo.html", todos=todos)

@app.route("/todo/<int:todo_id>/delete", methods=["POST"])
@login_required
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo and todo.user_id == current_user.id:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for("todo"))

@app.route("/todo/<int:todo_id>/complete", methods=["POST"])
@login_required
def complete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo and todo.user_id == current_user.id:
        todo.completed = True
        db.session.commit()
    return redirect(url_for("todo"))

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="todos")

if __name__ == "__main__":
    app.run(debug=True, port=5000)