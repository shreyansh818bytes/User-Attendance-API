from api.utils.db import db


class Absentee(db.Model):
    __tablename__ = "absentee"

    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), primary_key=True, nullable=False
    )
    absent_date = db.Column(db.Date, primary_key=True, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
