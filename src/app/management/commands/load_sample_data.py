import calendar
import random
import string
import sys
from datetime import timedelta, date, datetime

import holidays
from django.core.management.base import BaseCommand

from app.models import Visit, Dog


class Command(BaseCommand):
    """ Generate fake data"""

    def favorable_days(self, date):
        first_day_of_month = datetime(date.year, date.month, 1)
        last_day_of_month = calendar.monthrange(date.year, date.month)[1]
        # print "last day: ",
        first_friday = first_day_of_month + timedelta(
            days=((1 - calendar.monthrange(date.year, date.month)[0]) + 7) % 7)
        # 4 is friday of week
        days = []
        days.append(first_friday)
        days.append(first_friday + timedelta(days=1))
        for day in [7, 14, 21, 28]:
            friday = first_friday + timedelta(days=day)
            if friday.day <= last_day_of_month:
                days.append(friday)
            saturday = first_friday + timedelta(days=day + 1)
            if saturday.day <= last_day_of_month:
                days.append(saturday)
        return days

    def holidays_list(self, year):
        holidays_list = holidays.US(years=year)
        holidays_dict = {}
        for day in holidays_list:
            holiday = {'start': day - timedelta(days=2), 'end': day + timedelta(days=2)}
            holidays_dict[day.strftime("%Y-%m-%d")] = holiday
        return holidays_dict

    def create_visit(self, dog, start_date, end_date):
        try:
            visit = Visit(
                dog=dog,
                start_date=start_date,
                end_date=end_date
            )
            visit.save()
            print visit
        except Exception as e:
            print "error: ", e.message
            pass

    def handle(self, *args, **options):
        try:
            Visit.objects.all().delete()
            Dog.objects.all().delete()
        except Exception as e:
            print "Error: ", e.message
            sys.exit(1)

        year = 2016
        dogs = ["{} {}".format("".join([random.SystemRandom().choice(string.ascii_letters) for i in range(10)]),
                               "".join([random.SystemRandom().choice(string.ascii_letters) for i in range(10)]))
                for _ in range(10)]

        for dog in dogs:
            first_name, last_name = dog.split(' ')
            try:
                dog = Dog(
                    first_name=first_name,
                    last_name=last_name
                )
                dog.save()
            except Exception as e:
                print "Error: ", e.message
                pass
        dogs = Dog.objects.all()
        holidays = self.holidays_list(year)

        for month in xrange(1, 13):
            month_days = calendar.monthrange(year, month)[1]
            favorable_days = self.favorable_days(date(year, month, 1))
            print "favalorable days:", favorable_days
            for day in range(1, month_days + 1):
                start_date = date(year, month, day)
                for _ in range(5):
                    start_date = random.SystemRandom().choice(favorable_days)
                    delta = timedelta(days=random.randrange(1, 20))
                    end_date = start_date + delta
                    dog = random.SystemRandom().choice(dogs)
                    self.create_visit(dog, start_date, end_date)

                if start_date.strftime("%Y-%m-%d") in holidays.keys():
                    start_date, end_date = holidays[start_date.strftime("%Y-%m-%d")].values()
                    for _ in range(3):
                        dog = random.SystemRandom().choice(dogs)
                        self.create_visit(dog, start_date, end_date)

                delta = timedelta(days=random.randrange(1, 20))
                end_date = start_date + delta
                dog = random.SystemRandom().choice(dogs)
                self.create_visit(dog, date(2016, 01, 01), end_date)
