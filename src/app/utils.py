from calendar import HTMLCalendar
from datetime import date
from itertools import groupby
from django.core.urlresolvers import reverse


class BoardingCalendar(HTMLCalendar):
    def __init__(self, visits):
        super(BoardingCalendar, self).__init__()
        self.visits = self.group_by_day(visits)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            count = 0
            body = ['<p>']
            date_cell = "%s-%s-%s" % (str(self.year), str(self.month), str(day))
            for visit in self.visits.keys():
                if day in range(visit[0], visit[1] + 1):
                    count += 1
            body.append('%s %s' % (count, 'Dog' if count == 1 else 'Dogs'))
            return self.day_cell(cssclass, '<a href="%s?date=%s">%d %s</a>' % (
                reverse('app:in-the-house'), date_cell, day, ''.join(body)))
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        # a = []
        # a.append('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        # a.append(self.formatmonthname(year, first_month))
        # a.append(self.firstweekday)
        return super(BoardingCalendar, self).formatmonth(year, month)

    def group_by_day(self, visits):
        field = lambda visit: (visit.start_date.day, visit.end_date.day)

        return dict(
            [(day, list(items)) for day, items in groupby(visits, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)


def load_data(db_model):
    db_model.objects.all().delete()
    pass
