import calendar as cal
import random
import string
from datetime import datetime, timedelta
from unittest import TestCase

from django.core.urlresolvers import reverse
from django.test import RequestFactory

from app.models import Dog, Visit
from app.views import calendar, boardings

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
from django.db.models import Q


class CalendarTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.first_name = "".join([random.SystemRandom().choice(string.ascii_letters) for i in range(10)])
        self.last_name = "".join([random.SystemRandom().choice(string.ascii_letters) for i in range(10)])
        self.dog = Dog.objects.create(
            first_name=self.first_name,
            last_name=self.last_name
        )
        self.start_date = datetime.today().date()
        self.end_date = self.start_date + timedelta(days=15)
        self.visit = Visit.objects.create(
            dog=self.dog,
            start_date=self.start_date,
            end_date=self.end_date
        )

    def test__get_calendar__returns_status_200(self):
        request = self.factory.get(reverse('app:calendar'))
        response = calendar(request)
        self.assertEqual(response.status_code, 200)

    def test__post_calendar_with_period__returns_calender_with_period(self):
        start_date, end_date = self.start_date.strftime("%Y-%m-%d"), self.end_date.strftime("%Y-%m-%d")
        request = self.factory.post(
            reverse('app:calendar'), data={'start_date': start_date, 'end_date': end_date})
        response = calendar(request)
        self.assertEqual(response.status_code, 200)

        parsed_start_month = self.start_date.strftime("%B %Y")
        parsed_end_month = self.end_date.strftime("%B %Y")
        parsed_html = BeautifulSoup(response.content, "html.parser")
        self.assertIn(parsed_start_month, parsed_html.body.find(id="calendar").text)
        self.assertIn(parsed_end_month, parsed_html.body.find(id="calendar").text)


class BoardingsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.first_name = "".join([random.SystemRandom().choice(string.ascii_letters) for i in range(10)])
        self.last_name = "".join([random.SystemRandom().choice(string.ascii_letters) for i in range(10)])
        self.dog = Dog.objects.create(
            first_name=self.first_name,
            last_name=self.last_name
        )
        self.start_date = datetime.today().date()
        self.end_date = self.start_date + timedelta(days=3)
        self.visit = Visit.objects.create(
            dog=self.dog,
            start_date=self.start_date,
            end_date=self.end_date
        )

    def test__get_boarding_list_with_date__returns_list_of_dogs(self):
        request = self.factory.get(reverse('app:boardings'), data={'date': self.start_date.strftime("%Y-%m-%d")})
        response = boardings(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.visit.dog.first_name.title() in response.content)
