import calendar
from datetime import datetime

def get_days_of_date(**kwargs):
    if 'month' and 'year' in kwargs:
        month = kwargs['month']
        year  = kwargs['year']
    else:
        month = datetime.now().month
        year  = datetime.now().year

    return (calendar.monthcalendar(year, month))
   

def get_tasks_of_day(day, tasks):
    ltask = []

    for t in tasks:
        if t[4] == day:
            ltask.append(t)
    return ltask


def get_days_and_task(days, tasks):
    dtask = {}
    
    for d in range(0, 31):
        list_tasks = get_tasks_of_day(d + 1, tasks)

        if list_tasks != []:
            dtask[d + 1] = list_tasks
    
    return dtask