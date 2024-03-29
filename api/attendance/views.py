from datetime import date
from http import HTTPStatus

from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields, reqparse
from werkzeug.exceptions import BadRequest, Conflict, NotFound

from api.attendance.helpers import absentee_model_mapper
from api.models.absentee import Absentee
from api.models.user import User
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
    @attendance_namespace.expect(absent_request_parser)
    @jwt_required()
    def post(self, user_id):
        """
        Add absentee record
        """
        # Add role permission check here
        absent_date = absent_request_parser.parse_args().get("absent_date")
        if absent_date:
            absent_date = toDate(absent_date)
        else:
            absent_date = date.today()

        user = User.get_by_id(user_id)

        try:

            new_absentee = Absentee(user_id=user.id, absent_date=absent_date)

            new_absentee.save()

            return absentee_model_mapper(new_absentee, user), HTTPStatus.CREATED

        except Exception:
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
        absentee_record = Absentee.query.filter_by(
            user_id=user_id, absent_date=absent_date
        ).first()

        if not absentee_record:
            raise NotFound(
                f"User or absent record for user on this date does not exist!"
            )

        absentee_record.delete()

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
                absents = [absentee_model_mapper(absent, user) for absent in absents]
            else:
                # If end_date is not None, return a list
                absents = [absentee_model_mapper(user_record=user)]
            return absents, HTTPStatus.OK

        absentee = Absentee.query.filter_by(
            user_id=user_id, absent_date=start_date
        ).first()

        return absentee_model_mapper(absentee, user), HTTPStatus.OK
