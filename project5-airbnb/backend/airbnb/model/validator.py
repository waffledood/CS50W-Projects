from datetime import datetime

from django.http import JsonResponse

DATETIMEFORMAT_PYTHON = "%Y-%m-%d"
DATETIMEFORMAT = "YYYY-MM-DD"


def startAndEndDateFormatsAreWrong(startDate, endDate):
    return dateFormatIsWrong(startDate) or dateFormatIsWrong(endDate)


def startDateIsAfterEndDate(startDate, endDate):
    if endDate <= startDate:
        return True
    return False


def startDateIsBeforeToday(startDate):
    if startDate <= datetime.today():
        return True
    return False


def dateFormatIsWrong(dateText):
    try:
        if dateText != datetime.strptime(dateText, DATETIMEFORMAT_PYTHON).strftime(DATETIMEFORMAT_PYTHON):
            raise ValueError
        return True
    except ValueError:
        return False
