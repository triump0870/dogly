import random
import string
from datetime import datetime, timedelta
from unittest import TestCase

from django.core.urlresolvers import reverse
from django.test import RequestFactory

from app.models import Dog, Visit
from app.views import boarding_list, in_the_house_view


class BoardingListTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_boarding_list(self):
        request = self.factory.get(reverse('app:boarding-list'))
        response = boarding_list(request)
        self.assertEqual(response.status_code, 200)

    def test_post_boarding_list(self):
        start_date, end_date = "2016-01-01", "2016-02-01"
        request = self.factory.post(
            reverse('app:boarding-list'), data={'start': start_date, 'end': end_date})
        response = boarding_list(request)
        self.assertEqual(response.status_code, 200)


class InTheHouseViewTestCase(TestCase):
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

    def test_get_in_the_house_view(self):
        request = self.factory.get(reverse('app:in-the-house'), data={'date': self.start_date.strftime("%Y-%m-%d")})
        response = in_the_house_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.visit.dog.first_name.title() in response.content)
