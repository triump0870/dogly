from datetime import datetime
import calendar as cal
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
        start_date = request.POST.get('start_date', "")
        end_date = request.POST.get('end_date', "")
        if not start_date:
            return HttpResponse('Start date was not provided')
        if not end_date:
            return HttpResponse('End date was not provided')
    else:
        now = datetime.now()
        start_date = now.replace(day=1).strftime("%Y-%m-%d")
        end_date = now.replace(day=cal.monthrange(now.year, now.month)[1]).strftime("%Y-%m-%d")

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError as e:
        return HttpResponse(e.message)

    if end_date < start_date:
        return HttpResponse("End date can't be less than start date")

    # Fixed the Bug
    visits = Visit.objects.filter(
        Q(start_date__lte=start_date, end_date__gte=start_date) |
        Q(start_date__lt=end_date, end_date__gte=end_date)
    )

    if start_date.month == end_date.month:
        start_month = BoardingCalendar(
            visits,
            start_date.day,
            end_date.day).formatmonth(start_date.year, start_date.month)
        end_month = ""

    elif start_date.month < end_date.month:
        start_month = BoardingCalendar(
            visits,
            start_date.day,
            cal.monthrange(start_date.year, start_date.month)[1]).formatmonth(start_date.year, start_date.month)
        end_month = BoardingCalendar(visits, 1, end_date.day).formatmonth(end_date.year, end_date.month)

    else:
        start_month = BoardingCalendar(
            visits,
            start_date.day,
            cal.monthrange(start_date.year, start_date.month)[1]).formatmonth(start_date.year, start_date.month)
        end_month = ""

    return render(request, 'calendar.html',
                  {'start_month': mark_safe(start_month), 'end_month': mark_safe(end_month)})


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
