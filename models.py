"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


def connect_db(app):
    db.init_app(app)
    app.app_context().push()
    return db
# Model class


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(15),
                           nullable=False)

    last_name = db.Column(db.String(15),
                          nullable=False)

    image_url = db.Column(db.String,
                          nullable=False,
                          default=DEFAULT_IMAGE_URL)

    def __repr__(self):
        """Shows user information"""
        u = self
        return f"<User: id={u.id}, name={u.first_name + ' '+u.last_name}>"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    title = db.Column(db.Text,
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)

    usr = db.relationship('User', backref='post')

    # @property
    def time_format(self):
        return self.created_at.strftime("%d/%m/%Y, %-I:%M %p")
