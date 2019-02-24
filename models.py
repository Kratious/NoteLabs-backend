from app import db, ma
from sqlalchemy.orm.attributes import QueryableAttribute
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow_sqlalchemy import ModelSchema


class User(db.Model):
    """Model for the users table"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    notebooks = db.relationship('Notebook', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_one_user(id):
        return User.query.get(id)

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

class Notebook(db.Model):
    """Model for the notebooks table"""
    __tablename__ = 'notebooks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    notes = db.relationship('Note', backref='notebook', lazy='dynamic')

    def __repr__(self):
        return '<Notebook {}>'.format(self.title)


class Note(db.Model):
    """Model for the notes table"""
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    notebook_id = db.Column(db.Integer, db.ForeignKey('notebooks.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Note {}>'.format(self.content)



class NoteSchema(ma.ModelSchema):
    class Meta:
        model = Note

class NotebookSchema(ma.ModelSchema):
    #notes = ma.Nested(NoteSchema, many=True, only=('id'))
    class Meta:
        model = Notebook
        fields = ('id', 'title')

class UserSchema(ma.ModelSchema):
    notebooks = ma.Nested(NotebookSchema, many=True)
    class Meta:
        model = User
    

