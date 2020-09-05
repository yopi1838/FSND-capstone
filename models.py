'''
This script is used to define the database using Flask-SQLAlchemy.
The database was created locally before deployed using Heroku
'''
#import required dependencies
import os 
from sqlalchemy import Column, String, Integer, create_engine, DateTime
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json


#Coded by self at Mon, 17th Aug 2020 23:49 JST
#define the name of the database and the postgres path. 
# Make sure the name matches to the created local database

db_name = "casting_yopi"
db_path = os.environ["DATABASE_URL"]
db = SQLAlchemy()

'''
setup_db (app)
binds flask app and SQLAlchemy service
'''

def setup_db(app, database_path=db_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    init_db()

'''
Define the table as class
Movie
'''

class Movie(db.Model):
    __tablename__='movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(DateTime, default=datetime.utcnow) 

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return '<Title %r, Release Date %r>' % self.title, self.release_date

    def format(self):
        return{
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

'''
Define the table as class
Actors
'''
class Actor(db.Model):
    __tablename__='actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
    
    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return '<Name %r, Age %r, Gender %r>' % self.name, self.age, self.gender

    def format(self):
        return{
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

#Populate database
#Inspiration from https://github.com/InfinityByTen/fsnd-capstone/blob/ad8618411849ee9b4d2a255065b5e07e7e9bb99b/models.py#L109
def init_db():
    actors = [
        Actor(name="Tom Holland", age=23, gender="Male"),
        Actor(name="Tim Daly", age=58, gender="Male"),
        Actor(name="Amber Heard", age=30, gender="Female"),
        Actor(name="Chris Evans", age=34, gender="Male"),
        Actor(name="Halle Berry", age=57, gender="F")
    ]

    db.session.add_all(actors)

    movies = [
        Movie(title="Jumanji",
              release_date="2020-02-29 16:33:41"),
        Movie(title="Deadpool",
              release_date="2020-02-29 16:33:41"),
        Movie(title="The Karate Kid",
              release_date="2020-01-19 01:06:47")
    ]
    db.session.add_all(movies)
    db.session.commit()