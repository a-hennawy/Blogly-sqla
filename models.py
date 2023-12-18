"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


def connect_db(app):
    db.init_app(app)
    app.app_context().push()
    return db
# Model class


class User(db.Model):

    def __repr__(self):
        """Shows user information"""
        u = self
        return f"<User: id={u.id}, name={u.first_name + ' '+u.last_name}>"

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)

    first_name = db.Column(db.String(15),
                           nullable=False)

    last_name = db.Column(db.String(15),
                          nullable=False)

    image_url = db.Column(db.String,
                          nullable=False,
                          default=DEFAULT_IMAGE_URL)

    # def get_full_name(self):
    #     return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
