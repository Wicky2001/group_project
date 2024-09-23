from datetime import datetime

def parseDateTime(startDate, endDate, startTime, endTime):
    parsedStartDate = datetime.strptime(startDate, "%Y-%m-%d")
    parsedEndDate = datetime.strptime(endDate, "%Y-%m-%d")
    parsedStartTime = datetime.strptime(startTime, "%H:%M:%S")
    parsedEndTime = datetime.strptime(endTime, "%H:%M:%S")

    return {
        'startYear': parsedStartDate.year,
        'startMonth': parsedStartDate.month,
        'startDay': parsedStartDate.day,
        'endYear': parsedEndDate.year,
        'endMonth': parsedEndDate.month,
        'endDay': parsedEndDate.day,
        'startHour': parsedStartTime.hour,
        'startMinute': parsedStartTime.minute,
        'startSecond': parsedStartTime.second,
        'endHour': parsedEndTime.hour,
        'endMinute': parsedEndTime.minute,
        'endSecond': parsedEndTime.second,
    }

