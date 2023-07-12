from models import User, Post, db, connect_db
from app import app

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()


        User.query.delete()

        user1 = User(first_name="Johnny", last_name="Doe", img="https://hips.hearstapps.com/hmg-prod/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg?crop=0.752xw:1.00xh;0.175xw,0&resize=1200:*")
        user2 = User(first_name="Sarah", last_name="Longbrow", img="https://t4.ftcdn.net/jpg/00/97/58/97/360_F_97589769_t45CqXyzjz0KXwoBZT9PRaWGHRk5hQqQ.jpg")
        user3 = User(first_name="Buddy", last_name="Boy", img="https://images.unsplash.com/photo-1552728089-57bdde30beb3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8YmlyZHxlbnwwfHwwfHx8MA%3D%3D&w=1000&q=80")

        post1 = Post(title="I have the most generic name; a story", content="I thought I had more space to type smh, but yeah anyway my name is generic.", user_id=1)
        post2 = Post(title="My eyebrows aren't even long", content="My name suggests I have long eyebrows but I really don't, it's not like a hereditary thing or something smh.", user_id=2)
        post3 = Post(title="*Bird noises", content="Chirp chirp chirp, chirp CHIRP c h i r p.", user_id=3)

        db.session.add_all([user1, user2, user3])

        db.session.commit()

        db.session.add_all([post1, post2, post3])

        db.session.commit()
seed()
