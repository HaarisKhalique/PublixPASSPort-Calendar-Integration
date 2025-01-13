# Publix Schedule Scraper by Haaris Khalique
'''
This module processes the schedule html to 
retrieve the desired information.
'''
import re
from datetime import datetime
from bs4 import BeautifulSoup


# object to hold data for each work shift
class WorkDay:
    def __init__(self, start, end, meal_start, meal_end):
        self.start = start
        self.end = end
        self.meal_start = meal_start
        self.meal_end = meal_end


# This function combines each shift date and time
# into ISO format for Google Calendar.
def format_time(date, time_range):
    date = datetime.strptime(date, '%m/%d/%Y')

    if time_range == None:
        return None, None
    else:
        start_time, end_time = time_range.replace('.', '').split(' - ')

        if ':' in start_time:
            start = datetime.strptime(start_time, '%I:%M %p').time()
        else:
            start = datetime.strptime(start_time, '%I %p').time()

        if ':' in end_time:
            end = datetime.strptime(end_time, '%I:%M %p').time()
        else:
            end = datetime.strptime(end_time, '%I %p').time()
        
        datetime_start = datetime.combine(date,start)
        datetime_end = datetime.combine(date,end)

        iso_start = datetime_start.strftime('%Y-%m-%dT%H:%M:%S')
        iso_end = datetime_end.strftime('%Y-%m-%dT%H:%M:%S')
        
        return iso_start, iso_end
# end of format_time


# This function processes the HTML text using BeautifulSoup4 and retrieves shift dates and times
# Shift information is used to create WorkDay objects which will be sent to calendar as events
def process_html(html_content):
    
    # arrays to store data from HTML
    dates, shifts, meals, workdays = [], [], [], []
    

    # create soup from html
    soup = BeautifulSoup(html_content, 'html.parser')

    #Locate schedule element
    schedule = soup.find('div', id = 'redesignedSchedule')

    #Obtain week start date to extract month, day, year
    week_start_date = schedule.find_next('span').text.strip()

    current_month = 0
    current_day = 0
    current_year = 0
    
    pattern = r"(\d{1,2})/(\d{1,2})/(\d{4})" # mm/dd/yyyy pattern
    date_format = re.match(pattern, week_start_date)
    if date_format:
        current_month = (int)(date_format.group(1))
        current_day = (int)(date_format.group(2))
        current_year = (int)(date_format.group(3))
    
    

    #Obtain shift data for dates scheduled to work. Exclude elements where employee is not scheduled.
    days = schedule.find_all('div', class_= 'pb-3') 
    scheduled_days = [day for day in days if  day.find('div', class_= 'calendar-day-of-month-number')]

    for day in scheduled_days:
        # Find days employee is schedule
        day_number = (int)(day.find('div', class_= 'calendar-day-of-month-number').text.strip())
        
        #Handle transitions to new month and/or year
        if (day_number < current_day):
            current_day = day_number
            current_month += 1
            if(current_month > 12):
                current_month = 1
                current_year +=1

        dates.append(f'{current_month}/{day_number}/{current_year}')

        # Find shift times
        shift = day.find("div", id=lambda x: x and x.startswith('shift-details'))
        if(shift):  
            shift_time = shift.find_next('div', string= lambda x: x and '-' in x)
            shifts.append(shift_time.text.strip())

            # Find meal times
            meal = shift.find('div', class_='pt-3')
            if(meal):
                meal_div = meal.find('div', class_= 'pb-3')
                meal_time = meal_div.find('div', string=lambda x: x and '-' in x)
                meals.append(meal_time.text.strip())

            else:
                meals.append(None)
        else:
            shifts.append(None)
            meals.append(None)
    
    # create WorkDay objects, store in workdays
    for i in range(0, len(dates)):
        shift_start, shift_end = format_time(dates[i], shifts[i])
        meal_start, meal_end = format_time(dates[i], meals[i])
        workdays.append(WorkDay(shift_start,shift_end,meal_start,meal_end))

    return workdays