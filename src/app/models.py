from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.utils import IntegrityError
from schedule.models import Event, Calendar, EventRelation
from django.core.urlresolvers import reverse


# Create your models here.
class Dog(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('first_name', 'last_name')

    def __unicode__(self):
        return "%s %s" % (str(self.first_name.title()), str(self.last_name.title()))

    def get_full_name(self):
        return "%s %s" % (str(self.first_name.title()), str(self.last_name.title()))

    def save(self, *args, **kwargs):
        if not self.first_name:
            raise ValidationError("First name was not provided")
        self.first_name = self.first_name.lower()
        if self.last_name:
            self.last_name = self.last_name.lower()
        try:
            super(Dog, self).save(*args, **kwargs)
        except IntegrityError as e:
            raise IntegrityError("Dog with name [%s %s] already exists" % (self.first_name, self.last_name))


class Visit(models.Model):
    dog = models.ForeignKey(Dog)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "#%s-%s" % (str(self.id), str(self.dog))

    def save(self, *args, **kwargs):
        visits = Visit.objects.filter(dog=self.dog).filter(
            Q(start_date__lte=self.start_date, end_date__gte=self.start_date) |
            Q(start_date__lt=self.end_date, end_date__gte=self.end_date)
        )
        if visits.exists():
            raise ValidationError('Overlapping boarding visit for dog [%s]' % self.dog.id)

        super(Visit, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('app:boarding-detail', args=(self.id,))
