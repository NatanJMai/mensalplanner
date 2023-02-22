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
   

# TASK TABLE [3]: task_day
def get_tasks_of_day(day, tasks):
    ltask = []

    for t in tasks:
        if t[3] == day:
            ltask.append(t)
    return ltask


def get_days_and_task(days, tasks):
    dtask = {}
    
    for d in range(0, 31):
        list_tasks = get_tasks_of_day(d + 1, tasks)

        if list_tasks != []:
            dtask[d + 1] = list_tasks
    
    return dtask

# Verify if all items of 'list_received' are in 'list_request_form'
def verifyRequestList(request_method, list_received, list_request_form):
    return(all([it in list_request_form for it in list_received]))