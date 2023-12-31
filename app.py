from flask import Flask, redirect, request, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Blogly
import os.path

app = Flask(__name__)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "32m54hwcon49s1kl6"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sb_blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

with app.app_context():
    connect_db(app)
    db.create_all()

debug = DebugToolbarExtension(app)

def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))
# credit: MarredCheese at https://stackoverflow.com/questions/41144565/flask-does-not-see-change-in-js-file
# is used to automatically update static files without having to hard refresh the browser for every change :D


@app.route("/")
def root():
    return redirect("/users")

@app.route("/users")
def users():
    """Show users page"""
    users = Blogly.query.all()
    return render_template("users.html", users=users, last_updated=dir_last_updated("static"))

@app.route("/users/new")
def new_user():
    """Page to create a new user"""
    return render_template("create_user.html", last_updated=dir_last_updated("static"))

@app.route("/users/new", methods={"POST"})
def create_user():
    """Post route for creating a new user"""
    user = Blogly(first_name=request.form["first"], last_name=request.form["last"], img=request.form["src"])
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:id>")
def get_user(id):
    """Gets user info and displays"""
    user = Blogly.query.get(id)
    return render_template("user_detail.html", id=id, first=user.first_name, last=user.last_name, src=user.img, last_updated=dir_last_updated("static"))

@app.route("/users/<int:id>/edit")
def changing_user(id):
    """User edit page"""
    user = Blogly.query.get(id)
    return render_template("edit_user.html", id=id, first=user.first_name, last=user.last_name, src=user.img, last_updated=dir_last_updated("static"))

@app.route("/users/<int:id>/edit", methods={"POST"})
def edit_user(id):
    """Post route for edit page"""
    user = Blogly.query.get(id)
    user.first_name = request.form["first"]
    user.last_name = request.form["last"]
    user.img = request.form["src"]
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:id>/delete", methods={"POST"})
def delete_user(id):
    """Delete user route"""
    Blogly.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect("/users")




