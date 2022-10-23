from api.utils.db import db


class Absentee(db.Model):
    __tablename__ = "absentee"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False
    )
    absent_date = db.Column(db.Date, unique=True, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
