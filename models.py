# models.py

from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__= 'users'
    userID = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    userName = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(30))
    role = db.Column(db.String(10))

    def __repr__(self):
        return f'<User {self.userName}>'

class Attribute(db.Model):
    __tablename__= 'attributes'
    attributeID = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    attributeDescription = db.Column(db.String(200))
    
class Skill(db.Model):
    __tablename__= 'skills'
    skillID = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    skillName = db.Column(db.String(10), unique=True)
    skillDescription = db.Column(db.String(200))

class Discipline(db.Model):
    __tablename__= 'disciplines'
    disciplineID = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    disciplineName = db.Column(db.String(10), unique=True)
    disciplineDescription = db.Column(db.String(200))

class UserDiscipline(db.Model):
    __tablename__= 'user_disciplines'
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'), primary_key=True) # primary keys are required by SQLAlchemy
    disciplineID = db.Column(db.Integer, db.ForeignKey('disciplines.disciplineID'), primary_key=True)
    disciplineLevel = db.Column(db.Integer,nullable=False)

    user = db.relationship('User', back_populates='disciplines')
    discipline = db.relationship('Discipline', back_populates='users')

class UserSkill(db.Model):
    __tablename__= 'user_skills'
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'), primary_key=True) # primary keys are required by SQLAlchemy
    skillID = db.Column(db.Integer, db.ForeignKey('skills.skillID'), primary_key=True)
    skillLevel = db.Column(db.Integer,nullable=False)

    user = db.relationship('User', back_populates='skills')
    skill = db.relationship('Skill', back_populates='users')

    def __repr__(self):
        return f'<UserSkill {self.user.UserName} - {self.skill.SkillName}>'

class UsererAttribute(db.Model):
    __tablename__= 'user_attributes'
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'), primary_key=True) # primary keys are required by SQLAlchemy
    attributeID = db.Column(db.Integer, db.ForeignKey('attributes.attributeID'), primary_key=True)
    attributeLevel = db.Column(db.Integer,nullable=False)

    user = db.relationship('User', back_populates='disciplines')
    discipline = db.relationship('Discipline', back_populates='users')

User.skills = db.relationship('UserSkill', back_populates='user')
Skill.users = db.relationship('UserSkill', back_populates='skill')
User.disciplines = db.relationship('UserDiscipline', back_populates='user')
Discipline.users = db.relationship('UserDiscipline', back_populates='discipline')
User.attributes = db.relationship('UserAttribute', back_populates='user')
Attribute.users = db.relationship('USerAttributes', back_populates='attributes')