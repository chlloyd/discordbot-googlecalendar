from icalendar import Calendar, Event
from datetime import datetime
from pytz import UTC # timezone

cal = Calendar()
cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')

event = Event()
event.add('summary', 'Python meeting about calendaring')
event.add('dtstart', datetime(2005,4,4,8,0,0,tzinfo=UTC))
event.add('dtend', datetime(2005,4,4,10,0,0,tzinfo=UTC))
event.add('dtstamp', datetime(2005,4,4,0,10,0,tzinfo=UTC))
event['uid'] = '20050115T101010/27346262376@mxm.dk'
event.add('priority', 5)

cal.add_component(event)

f = open('basic.ics', 'wb')
f.write(cal.to_ical())
f.close()
