#!/usr/local/bin/python
import sys

GOOGLE_CALENDAR_USER = ''
GOOGLE_CALENDAR_PASSWORD = ''

TEMPLATE_FILE = 'cal_template.htm'
OUTPUT_FILE = 'cal_output.htm'
NUM_RESULTS = 6

from datetime import date, datetime, tzinfo, timedelta
from dateutil.parser import *
from dateutil.tz import *

from gdata.calendar.service import *


def getEvents():
    # Log in
    calendar_service = CalendarService()
    calendar_service.email = GOOGLE_CALENDAR_USER
    calendar_service.password = GOOGLE_CALENDAR_PASSWORD

    # Fill out the next line
    calendar_service.source = ''
    
    calendar_service.ProgrammaticLogin()
    
    # Create query
    now = datetime.now()
    later = now + timedelta(days=60)
    
    # Provide the first arguement here
    query = CalendarEventQuery('', 'private', 'full')
    query.start_min = '%i-%02i-%02i' % (now.year, now.month, now.day)
    query.start_max = '%i-%02i-%02i' % (later.year, later.month, later.day)
    feed = calendar_service.CalendarQuery(query)
    events = feed.entry
    
    events_dict = {}
    for event in events:
        for when in event.when:
            events_dict[when.start_time] = [event, when]
    
    # Sort
    keys = events_dict.keys()
    keys.sort()
    sorted_events = map(events_dict.get, keys)
    
    # Get the text
    f = open(TEMPLATE_FILE, 'r')
    template_text = f.read()
    f.close()

    # Print them out
    output_html = ''
    for i, event_info in enumerate(sorted_events):
        if i >= NUM_RESULTS:
            break
        event = event_info[0]
        when = event_info[1]
        start = parse(when.start_time)
        end = parse(when.end_time)
        output_html += template_text.format(event={
            'title': event.title.text,
            'date': '%s %i - %i%s' % (start.strftime('%A, %B'), int(start.strftime('%d')), int(start.strftime('%I')), start.strftime('%p').lower()),
            'where': event.where[0].value_string,
            'link': event.GetHtmlLink().href,
        })
        
    f = open(OUTPUT_FILE, 'w')
    f.write(output_html)
    f.close()

if __name__ == '__main__':
    getEvents()
        