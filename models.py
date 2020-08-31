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
db_path = "postgres://{}@{}/{}".format('yopiprabowooktiovan','localhost:5432', db_name)

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
    db.create_all()

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