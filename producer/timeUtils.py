import time
def timestamp2date(timestamp):
    timeArray = time.localtime(timestamp)
    formatTime = time.strftime("%Y-%m-%d", timeArray)
    return formatTime


def date2timestamp(date):
    timeArray = time.strptime(date, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def formatDate(date):
    timeStamp = date2timestamp(date)
    formatTime = timestamp2date(timeStamp)
    return formatTime


if __name__ == '__main__':
    print(formatDate("2020-11-29 14:50:50"))
