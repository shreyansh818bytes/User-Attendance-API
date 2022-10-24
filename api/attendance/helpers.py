from api.models.user import User
from api.models.absentee import Absentee


def absentee_model_mapper(absentee_record: Absentee, user_record: User):
    absentee = {
        "user_id": None,
        "name": None,
        "email": None,
        "is_active": None,
        "role": None,
        "absent_date": None,
    }
    if absentee_record:
        absentee["absent_date"] = absentee_record.absent_date
        absentee["user_id"] = absentee_record.user_id
    if user_record:
        absentee["user_id"] = user_record.id
        absentee["name"] = user_record.name
        absentee["email"] = user_record.email
        absentee["is_active"] = user_record.is_active
        absentee["role"] = user_record.role

    return absentee
