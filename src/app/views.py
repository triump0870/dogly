import json
from datetime import datetime, timedelta

from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render_to_response, render
from django.utils.safestring import mark_safe
from django.views.generic import DetailView, ListView

from app.models import Visit
from app.utils import BoardingCalendar


def boarding_list(request):
    if request.method == 'POST':
        start = request.POST.get('start', "")
        end = request.POST.get('end', "")
        if not start:
            return HttpResponse('Start date was not provided')
        if not end:
            return HttpResponse('End date was not provided')
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()

    else:
        start_date = datetime.strptime("2016-01-01", "%Y-%m-%d").date()
        end_date = datetime.strptime("2016-01-31", "%Y-%m-%d").date()

    visits = Visit.objects.filter(
        Q(start_date__range=(start_date, end_date)) |
        Q(end_date__range=(start_date, end_date))
    )
    cal = BoardingCalendar(visits).formatmonth(start_date.year, start_date.month)
    return render(request, 'boarding.html', {'calendar': mark_safe(cal)})

def in_the_house_view(request):
    date = request.GET.get('date')
    date = datetime.strptime(date, "%Y-%m-%d").date()
    visits = Visit.objects.filter(
        Q(start_date__lte=date) &
        Q(end_date__gt=date)
    )
    context = {
        'visits': visits
    }
    return render_to_response('detail_view.html', context)


def load_sample_data_view(request):
    call_command('load_sample_data')
    return HttpResponse('Data loaded')
