from flask import Flask, redirect, request, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, Post_tag
import os.path
from datetime import datetime

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
    users = User.query.all()
    return render_template("users.html", users=users, last_updated=dir_last_updated("static"))

@app.route("/users/new")
def new_user():
    """Page to create a new user"""
    return render_template("create_user.html", last_updated=dir_last_updated("static"))

@app.route("/users/new", methods={"POST"})
def create_user():
    """Post route for creating a new user"""
    user = User(first_name=request.form["first"], last_name=request.form["last"], img=request.form["src"])
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:id>")
def get_user(id):
    """Gets user info and displays"""
    user = User.query.get_or_404(id)
    posts = Post.query.filter_by(user_id=id).all()
    return render_template("user_detail.html", id=id, first=user.first_name, last=user.last_name, src=user.img, posts=posts, last_updated=dir_last_updated("static"))

@app.route("/users/<int:id>/edit")
def changing_user(id):
    """User edit page"""
    user = User.query.get(id)
    return render_template("edit_user.html", id=id, first=user.first_name, last=user.last_name, src=user.img, last_updated=dir_last_updated("static"))

@app.route("/users/<int:id>/edit", methods={"POST"})
def edit_user(id):
    """Post route for edit page"""
    user = User.query.get(id)
    user.first_name = request.form["first"]
    user.last_name = request.form["last"]
    user.img = request.form["src"]
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:id>/delete", methods={"POST"})
def delete_user(id):
    """Delete user route"""
    User.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:id>/posts/new")
def new_post(id):
    """Page to create a new post"""
    user = User.query.get(id)
    tags = Tag.query.all()
    return render_template("create_post.html", id=id, first=user.first_name, last=user.last_name, tags=tags, last_updated=dir_last_updated("static"))

@app.route("/users/<int:id>/posts/new", methods={"POST"})
def create_post(id):
    """Post route for new posts"""
    post = Post(title=request.form["title"], content=request.form["content"], user_id=id)
    tags = Tag.query.all()
    post_tags = []
    db.session.add(post)
    db.session.commit()
    for x in tags:
        if (request.form.get((str)(x.id)) != None):
            post_tags.append(Post_tag(post_id=post.id, tag_id=x.id))
        
    db.session.add_all(post_tags)
    db.session.commit()
    return redirect(f"/users/{id}")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Page showing a post"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get(post.user_id)
    return render_template("post.html", post_id=post_id, post=post, user=user, tags=post.tags,  last_updated=dir_last_updated("static"))

###
@app.route("/posts/<int:post_id>/edit")
def changing_post(post_id):
    """Page to edit a post"""
    post = Post.query.get(post_id)
    tags = Tag.query.all()
    return render_template("edit_post.html", post_id=post_id, post=post, tags=tags, last_updated=dir_last_updated("static"))

@app.route("/posts/<int:post_id>/edit", methods={"POST"})
def edit_post(post_id):
    """Post route for editing a post"""
    post = Post.query.get(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    post.tags = []
    post_tags = []
    tags = Tag.query.all()
    for x in tags:
        if (request.form.get((str)(x.id)) != None):
            post_tags.append(Post_tag(post_id=post.id, tag_id=x.id))  
    db.session.add(post)
    db.session.add_all(post_tags)
    db.session.commit()  
    return redirect(f"/users/{post.user_id}")

@app.route("/posts/<int:post_id>/delete", methods={"POST"})
def delete_post(post_id):
    """Post route for deleting a post"""
    post = Post.query.get(post_id)
    id = post.user_id
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f"/users/{id}")

@app.route("/tags")
def show_tags():
    tags = Tag.query.all()
    return render_template("tags.html", tags=tags, last_updated=dir_last_updated("static"))

@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template("show_tag.html", tag=tag, last_updated=dir_last_updated("static"))

@app.route("/tags/new")
def create_tag():
    return render_template("create_tag.html", last_updated=dir_last_updated("static"))

@app.route("/tags/new", methods={"POST"})
def new_tag():
    tag = Tag(name=request.form["tag"])
    db.session.add(tag)
    db.session.commit()
    return redirect("/tags")

@app.route("/tags/<int:tag_id>/edit")
def changing_tag(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template("edit_tag.html", tag=tag, last_updated=dir_last_updated("static"))

@app.route("/tags/<int:tag_id>/edit", methods={"POST"})
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    tag.name = request.form["tag"]
    db.session.add(tag)
    db.session.commit()
    return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete", methods={"POST"})
def delete_tag(tag_id):
    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()
    return redirect("/tags")




