from enum import Enum

from api.utils.db import db


class UserRole(Enum):
    SECRETARY = 'secretary'
    VOLUNTEER = 'volunteer'
    MEMBER = 'member'


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(30), nullable=False)
    password_hash = db.Column(db.Text(), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    role = db.Column(db.Enum(UserRole), default=UserRole.MEMBER)

    def __repr__(self):
        f"<User {self.id} {self.username}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
