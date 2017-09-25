from datetime import datetime

from django.core.management import call_command
from django.db.models import Q
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render_to_response, render
from django.utils.safestring import mark_safe

from app.models import Visit
from app.utils import BoardingCalendar


def calendar(request):
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
        end_date = datetime.strptime("2016-02-29", "%Y-%m-%d").date()

    # Todo: Bug
    visits = Visit.objects.filter(
        Q(start_date__range=(start_date, end_date)) |
        Q(end_date__range=(start_date, end_date))
    )
    # Todo: FIXbug

    start_month = BoardingCalendar(visits).formatmonth(start_date.year, start_date.month)
    end_month = BoardingCalendar(visits).formatmonth(end_date.year, end_date.month)
    return render(request, 'calendar.html', {'start_month': mark_safe(start_month), 'end_month': mark_safe(end_month)})


def boardings(request):
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
