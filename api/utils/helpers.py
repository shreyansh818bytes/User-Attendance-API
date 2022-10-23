from datetime import datetime


def toDate(dateString):
    return datetime.strptime(dateString, "%Y-%m-%d").date()
