from . import jalali
from django.utils import timezone

def persianNumbersConverter(str):
    numbers = {
        "0" : "۰",
        "1" : "۱",
        "2" : "۲",
        "3" : "۳",
        "4" : "۴",
        "5" : "۵",
        "6" : "۶",
        "7" : "۷",
        "8" : "۸",
        "9" : "۹",
    }
    
    for e, p in numbers.items():
        str = str.replace(e, p)
    
    return str

def jalali_converter(time):
    jmonths = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور ", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
    time = timezone.localtime(time)
    
    timeToStr = "{},{},{}".format(time.year, time.month, time.day)
    timeToTuple = jalali.Gregorian(timeToStr).persian_tuple()
    timeToList = list(timeToTuple)
    
    
    for index, month in enumerate(jmonths):
        if timeToList[1] == index + 1:
            timeToList[1] = month
            break
            
    output = "{} {} {}, ساعت {}:{}".format(
        timeToList[2],
        timeToList[1],
        timeToList[0],
        time.hour,
        time.minute,
    )
    
    return persianNumbersConverter(output)