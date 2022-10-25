from datetime import datetime

from werkzeug.exceptions import BadRequest


def toDate(date_string):
    try:
        formatted_date = datetime.strptime(date_string, "%Y-%m-%d").date()
    except:
        raise BadRequest("Incorrect date format!")

    return formatted_date
