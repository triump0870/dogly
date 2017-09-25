from calendar import HTMLCalendar
from datetime import date
from itertools import groupby

from django.core.urlresolvers import reverse


class BoardingCalendar(HTMLCalendar):
    def __init__(self, visits):
        super(BoardingCalendar, self).__init__()

        # Naming of self.visit was changed to self.boardings for continuity
        self.boardings = self.group_by_day(visits)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            count = 0
            body = ['<p>']
            date_cell = "%s-%s-%s" % (str(self.year), str(self.month), str(day))
            for period in self.boardings.keys():
                # Here period is a tuple of two day elements, e.g (20, 25)
                # Max days in a month is 31, but the Python range(x,y) function iters
                # in the range x<=item<y, but we need the max range (y) inclusive in our range
                # i.e x<=item<=y

                if day in range(period[0], period[1] + 1):
                    count += 1

            body.append('%s %s' % (count, 'Dog' if count == 1 else 'Dogs'))
            return self.day_cell(cssclass, '<a href="%s?date=%s">%d %s</a>' % (
                reverse('app:boardings'), date_cell, day, ''.join(body)))
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(BoardingCalendar, self).formatmonth(year, month)

    def group_by_day(self, visits):
        # Naming was fixed here
        boarding_period = lambda visit: (visit.start_date.day, visit.end_date.day)

        return dict(
            [(period, list(boardings)) for period, boardings in groupby(visits, boarding_period)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)
