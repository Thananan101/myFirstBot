from datetime import datetime   #To set date and time

def validate_time(alarm_time):
    if len(alarm_time) != 10:
        return "Invalid time format! Please try again..."
    else:
        if int(alarm_time[0:2]) > 12:
            return "Invalid HOUR format! Please try again..."
        elif int(alarm_time[3:5]) > 59:
            return "Invalid MINUTE format! Please try again..."
        elif int(alarm_time[6:8]) > 59:
            return "Invalid SECOND format! Please try again..."
        else:
            return "ok"

def timezoneToTH(alarm_time):
  alarm_hour = int(alarm_time[0:2])
  alarm_min = alarm_time[3:5]
  alarm_sec = alarm_time[6:8]
  alarm_period = alarm_time[8:].upper()

  alarm_hour -= 7
  if alarm_hour < 0:
    alarm_hour += 12
    if alarm_period == "AM":
      alarm_period = "PM"
    else:
      alarm_period = "AM"
  if len(str(alarm_hour)) != 2:
    alarm_hour = "0" + str(alarm_hour)
  return str(alarm_hour) + ":" + alarm_min + ":" + alarm_sec + alarm_period


