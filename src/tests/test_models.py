from __future__ import unicode_literals

import random
import string
from datetime import datetime, timedelta
from unittest import TestCase

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.utils import IntegrityError

from app.models import Dog, Visit


class DogTestCase(TestCase):
    def setUp(self):
        self.first_name = "".join([random.SystemRandom().choice(string.ascii_letters) for i in range(10)])
        self.last_name = "".join([random.SystemRandom().choice(string.ascii_letters) for i in range(10)])
        self.dog = Dog.objects.create(
            first_name=self.first_name,
            last_name=self.last_name
        )

    def test__duplicate_name__raises_integrity_error(self):
        with self.assertRaises(IntegrityError) as e:
            Dog.objects.create(
                first_name=self.first_name,
                last_name=self.last_name
            )

    def test__last_name_blank__should_create_object(self):
        dog = Dog.objects.create(first_name=self.first_name)
        self.assertTrue(dog.first_name, self.first_name)
        self.assertFalse(dog.last_name, "")

    def test__first_name_blank__raises_validation_error(self):
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

    def test__dog_field_blank__raises_object_does_not_exist(self):
        with self.assertRaises(ObjectDoesNotExist):
            Visit.objects.create(
                start_date=self.start_date,
                end_date=self.end_date
            )

    def test__start_date_blank__raises_value_error(self):
        with self.assertRaises(ValueError):
            Visit.objects.create(
                dog=self.dog,
                start_date=self.start_date
            )

    def test__end_date_blasnk__raises_value_error(self):
        with self.assertRaises(ValueError):
            Visit.objects.create(
                dog=self.dog,
                end_date=self.end_date
            )

    def test__overlapping_visit__raises_validation_error(self):
        with self.assertRaises(ValidationError):
            Visit.objects.create(
                dog=self.dog,
                start_date=self.start_date + timedelta(days=1),
                end_date=self.end_date
            )
