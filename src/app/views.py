import json
from datetime import datetime, timedelta

from django.db.models import Q
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from django.views.generic import DetailView, ListView

from app.models import Visit
from app.utils import BoardingCalendar


def calendar(request, start="2017-09-01", end="2017-09-30"):
    start_date = datetime.strptime(start, "%Y-%m-%d").date()
    end_date = datetime.strptime(end, "%Y-%m-%d").date()

    visits = Visit.objects.filter(
        Q(start_date__range=(start_date, end_date)) |
        Q(end_date__range=(start_date, end_date))
    )
    cal = BoardingCalendar(visits).formatmonth(start_date.year, start_date.month)
    return render_to_response('fullcalendar.html', {'calendar': mark_safe(cal), })


