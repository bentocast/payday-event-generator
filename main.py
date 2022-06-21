'''This file contains the main function'''
import calendar
from datetime import date, timedelta
from typing import List, Tuple
from pathlib import Path
import os
from icalendar import Calendar, Event

FRIDAY_WEEKDAY = 4

def main():
    '''Main function'''
    
    year_start, year_end = parse_arguments()
    payday_events: List[date] = collect_paydays(year_start, year_end)

    if not payday_events:
        return

    cal: Calendar = transform_to_cal(payday_events)
    generate_ical_file(cal)

def generate_ical_file(cal):
    '''Generate ical file'''

    directory = str(Path(__file__).parent) + "/output"
    if not os.path.exists(directory):
        os.mkdir(directory)
    
    f = open(os.path.join(directory, 'payday_events.ics'), 'wb')
    f.write(cal.to_ical())
    f.close()


def transform_to_cal(payday_events: List[date]) -> Calendar:
    '''Transform the list of payday events to a Calendar instance'''

    cal = Calendar()
    for payday_event in payday_events:
        event = Event()
        event.add('summary', 'Today is payday')
        event.add('dtstart', payday_event)
        event.add('dtend', payday_event + timedelta(days=1))
        event.add('dtstamp', payday_event)
        cal.add_component(event)

    return cal

def collect_paydays(year_start: int, year_end: int) -> List[date]:
    '''Collects all payday events and return this list'''

    print('Next, please give us more detail about the payday condition')
    is_static_str = input("Is your payday on the fixed date, like 28th of every month? (y / n): ")
    is_static =  is_static_str.lower() == 'y'
    static_date = int(input("Enter the fix date of payday [1-30]: ")) if is_static else None

    if not is_static:
    
        is_days_before_month_str = input("Is your payday depends on the last date of the month, like the 3rd from the last day of every month? (y / n): ")
        is_days_before_month = is_days_before_month_str.lower() == 'y'
        days_before_month = int(input("Enter the number of days before the last days of each month [1-30]: ")) if is_days_before_month else None

    if not is_static and not is_days_before_month:
        print('Unfortunately, this tool does not supprot any other payday conditions. Please comment about the missing conditions in github, so I can improve this.')
        return [] 
    
    is_avoid_on_weekend_str = input("Does your payday avoid the weekend? (y / n): ")
    is_avoid_on_weekend = is_avoid_on_weekend_str.lower() == 'y'

    payday_events: List[date] = []
    for year in range(year_start, year_end + 1):
        for month in range(1, 13):
            
            if static_date:
                payday = static_date
            elif days_before_month:
                payday = calendar.monthrange(year, month)[1] - days_before_month

            # If the 2nd last day is in weekend, it will move to earlier Friday
            last_date_weekday = calendar.weekday(year, month, payday)
            if is_avoid_on_weekend and last_date_weekday > FRIDAY_WEEKDAY:
                payday -= (last_date_weekday - FRIDAY_WEEKDAY)

            # Collect payday event
            print(f'The payday is {date(year, month, payday)}')
            payday_date = date(year, month, payday)
            payday_events.append(payday_date)

    return payday_events


def parse_arguments() -> Tuple[int, int]:
    '''Initialize parser and validate year_start and year_end'''

    print('Hi, welcome to Payday Event Generator.')
    print('Please enter the range of the year you want to generate payday events')
    year_start = int(input("Enter the first year [1900-2500]: "))
    year_end = int(input("Enter the last year [1900-2500]: "))

    # Validate the input
    if 1900 < year_end < year_start < 2500:
        raise ValueError(
            'The `year_start` must be less than the `year_end`, and both of them must be in range [2000, 2500]')

    return year_start, year_end

if __name__ == "__main__":
    main()
