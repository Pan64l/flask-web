# creat a database models
from website import database
from flask_login import UserMixin
from sqlalchemy import func
#flask requires a user model, UserMixin is used to create a class that inherits from UserMixin that have functions authenticate


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(120), unique=True)
    password = database.Column(database.String(100))
    first_name = database.Column(database.String(100))
    notes = database.relationship('Note')
    # reference the class note, is upper case

# class picture(database.Model):
#     id = database.Column(database.Integer, primary_key=True)
# ----- I want to store the picture in the database ----- #
    
class Note(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    data = database.Column(database.String(10000))
    date = database.Column(database.DateTime(timezone= True), default = func.now())
    u_id = database.Column(database.Integer, database.ForeignKey('user.id')) # we must pass the id of the user to the note table
    # when you do foreignkey the class is lower case
    
