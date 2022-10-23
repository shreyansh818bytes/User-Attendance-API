from datetime import date
from flask_restx import Resource, Namespace, fields, reqparse
from api.models.user import User
from api.models.absentee import Absentee
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import BadRequest, Conflict
from api.utils.helpers import toDate

attendance_namespace = Namespace("attendance", description="Attendance Namespace")

user_attendance_model = attendance_namespace.model(
    "Absentee",
    {
        "user_id": fields.Integer(description="Absentee's user_id"),
        "name": fields.String(description="Full Name"),
        "email": fields.String(description="An email"),
        "is_active": fields.Boolean(description="This shows that User is active"),
        "role": fields.String(description="Role of the user"),
        "absent_date": fields.Date(description="User was absent on this date"),
    },
)

user_attendance_reqeust_parser = reqparse.RequestParser()
user_attendance_reqeust_parser.add_argument(
    "start_date",
    type=str,
    help="Starting date to fetch attendance records. Date format=(%Y-%m-%d)",
)
user_attendance_reqeust_parser.add_argument(
    "end_date",
    type=str,
    help="Ending date to fetch attendance records.\nThis should not be passed if only single date records are needed\nDate format=(%Y-%m-%d)",
)

absent_request_parser = reqparse.RequestParser()
absent_request_parser.add_argument("absent_date")


@attendance_namespace.route("/user/<int:user_id>/absent")
class AddAbsenteeRecord(Resource):
    @attendance_namespace.marshal_with(user_attendance_model)
    @attendance_namespace.doc(description="Add an absentee record for a user")
    @jwt_required()
    def post(self, user_id):
        """
        Add absentee record
        """
        # Add role permission check here
        todays_date = date.today()

        try:
            user = User.get_by_id(user_id)

            new_absentee = Absentee(user_id=user.id, absent_date=todays_date)

            new_absentee.save()

            return {
                "user_id": user.id,
                "name": user.name,
                "email": user.email,
                "is_active": user.is_active,
                "role": user.role,
                "absent_date": new_absentee.absent_date,
            }, HTTPStatus.CREATED

        except Exception as e:
            raise Conflict(description=f"Absentee record already exists.")

    @attendance_namespace.expect(absent_request_parser, validate=True)
    @attendance_namespace.doc(
        description="Delete an absentee record.",
        params={"user_id": "User ID"},
    )
    @jwt_required()
    def delete(self, user_id):
        """
        Delete absentee record
        """
        absent_date = absent_request_parser.parse_args().get("absent_date")
        Absentee.query.filter_by(
            user_id=user_id, absent_date=absent_date
        ).first().delete()

        return {"message": "Absentee record deleted successfuly!"}, HTTPStatus.OK


@attendance_namespace.route("/user/<int:user_id>")
class GetAbsenteeRecord(Resource):
    @attendance_namespace.marshal_with(user_attendance_model)
    @attendance_namespace.doc(
        description="""
        Retrieve all absentee records of a user.
        "absent_date" parameter is null in the results if the user was present at "start_date".
        """
    )
    @attendance_namespace.expect(user_attendance_reqeust_parser, validate=True)
    @jwt_required()
    def get(self, user_id):
        """
        Fetch absentee records between a date range or a single date
        """
        request_args = user_attendance_reqeust_parser.parse_args()
        start_date = request_args.get("start_date")
        end_date = request_args.get("end_date", None)

        user = User.get_by_id(user_id)

        if not start_date:
            raise BadRequest(description="'start_date' parameter not found")

        start_date = toDate(start_date)
        if end_date:
            end_date = toDate(end_date)
            absents = (
                Absentee.query.filter_by(user_id=user_id)
                .filter(Absentee.absent_date.between(start_date, end_date))
                .all()
            )
            if absents:
                absents = [
                    {
                        "user_id": absent.id,
                        "name": user.name,
                        "email": user.email,
                        "is_active": user.is_active,
                        "role": user.role,
                        "absent_date": absent.absent_date,
                    }
                    for absent in absents
                ]
            else:
                absents = {
                    "user_id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "is_active": user.is_active,
                    "role": user.role,
                }
            return absents, HTTPStatus.OK

        absentee = Absentee.query.filter_by(
            user_id=user_id, absent_date=start_date
        ).first()

        if not absentee:
            absentee = {
                "user_id": user.id,
                "name": user.name,
                "email": user.email,
                "is_active": user.is_active,
                "role": user.role,
            }
        else:
            absentee = {
                "user_id": absentee.user_id,
                "name": user.name,
                "email": user.email,
                "is_active": user.is_active,
                "role": user.role,
                "absent_date": absentee.absent_date,
            }
        return absentee, HTTPStatus.OK
