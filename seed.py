from models import Blogly, db, connect_db
from app import app

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()


        Blogly.query.delete()

        user1 = Blogly(first_name="Johnny", last_name="Doe", img="https://hips.hearstapps.com/hmg-prod/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg?crop=0.752xw:1.00xh;0.175xw,0&resize=1200:*")
        user2 = Blogly(first_name="Sarah", last_name="Longbrow", img="https://t4.ftcdn.net/jpg/00/97/58/97/360_F_97589769_t45CqXyzjz0KXwoBZT9PRaWGHRk5hQqQ.jpg")
        user3 = Blogly(first_name="Buddy", last_name="Boy", img="https://images.unsplash.com/photo-1552728089-57bdde30beb3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8YmlyZHxlbnwwfHwwfHx8MA%3D%3D&w=1000&q=80")


        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)

        db.session.commit()
seed()
