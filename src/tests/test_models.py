from __future__ import unicode_literals

import random
import string
from datetime import datetime, timedelta
from unittest import TestCase

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.utils import IntegrityError

from app.models import Dog, Visit


# from django.db.models.fields import RelatedObjectDoesNotExist

class DogTestCase(TestCase):
    def setUp(self):
        self.first_name = "".join([random.SystemRandom().choice(string.ascii_letters) for i in range(10)])
        self.last_name = "".join([random.SystemRandom().choice(string.ascii_letters) for i in range(10)])
        self.dog = Dog.objects.create(
            first_name=self.first_name,
            last_name=self.last_name
        )

    def test_duplicate_name(self):
        with self.assertRaises(IntegrityError) as e:
            dog1 = Dog.objects.create(
                first_name=self.first_name,
                last_name=self.last_name
            )

    def test_last_blank_get_accepted(self):
        dog = Dog.objects.create(first_name=self.first_name)
        self.assertTrue(dog.first_name, self.first_name)
        self.assertFalse(dog.last_name, "")

    def test_failed_without_first_name(self):
        with self.assertRaises(ValidationError):
            Dog.objects.create(last_name=self.last_name)


class VisitTestCase(TestCase):
    def setUp(self):
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

    def test_without_dog_field(self):
        with self.assertRaises(ObjectDoesNotExist):
            Visit.objects.create(
                start_date=self.start_date,
                end_date=self.end_date
            )

    def test_without_start_date_field(self):
        with self.assertRaises(ValueError):
            Visit.objects.create(
                dog=self.dog,
                start_date=self.start_date
            )

    def test_without_end_date_field(self):
        with self.assertRaises(ValueError):
            Visit.objects.create(
                dog=self.dog,
                end_date=self.end_date
            )

    def test_overlapping_visit(self):
        with self.assertRaises(ValidationError):
            Visit.objects.create(
                dog=self.dog,
                start_date=self.start_date + timedelta(days=1),
                end_date=self.end_date
            )
