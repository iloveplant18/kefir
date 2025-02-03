from datetime import datetime as dt
import datetime

class DateTimeOperationsService(object):

    @staticmethod
    def parseTime(seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        return hours, minutes, seconds

    @staticmethod
    def getNowDateTime():
        timeNow = dt.now().time()
        return dt.combine(dt.min, timeNow)

    @staticmethod
    def getTimeDeltaFromSeconds(seconds):
        parsedSeconds = DateTimeOperationsService.parseTime(seconds)
        time = datetime.time(hour=parsedSeconds[0], minute=parsedSeconds[1], second=parsedSeconds[2])
        timeDelta = dt.combine(dt.min, time) - dt.min
        return timeDelta