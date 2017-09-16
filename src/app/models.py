from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.utils import IntegrityError
from schedule.models import Event, Calendar, EventRelation
from django.core.urlresolvers import reverse


# Create your models here.
class Dog(models.Model):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('first_name', 'last_name')

    def __unicode__(self):
        return "%s %s" % (str(self.first_name.title()), str(self.last_name.title()))

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.lower()
        if self.last_name:
            self.last_name = self.last_name.lower()
        try:
            super(Dog, self).save(*args, **kwargs)
        except IntegrityError as e:
            print "error"
            raise IntegrityError("Dog with name [%s %s] already exists" % (self.first_name, self.last_name))
            