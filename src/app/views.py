import json
from datetime import datetime, timedelta

from django.db.models import Q
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render_to_response, render
from django.utils.safestring import mark_safe
from django.views.generic import DetailView, ListView

from app.models import Visit
from app.utils import BoardingCalendar


def calendar_view(request):
    start = request.POST.get('start', "")
    end = request.POST.get('end', "")

    if not start:
        start_date = datetime.today().date()
    else:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()

    if not end:
        end_date = datetime.today().date() + timedelta(days=30)
    else:
        end_date = datetime.strptime(end, "%Y-%m-%d").date()

    visits = Visit.objects.filter(
        Q(start_date__range=(start_date, end_date)) |
        Q(end_date__range=(start_date, end_date))
    )
    cal = BoardingCalendar(visits).formatmonth(start_date.year, start_date.month, end_date.month)
    return render(request, 'fullcalendar.html', {'calendar': mark_safe(cal)})
    # return render_to_response('fullcalendar.html', {'calendar': mark_safe(cal), })


def boarding_feed(request):
    from django.utils.timezone import utc
    from django.core.serializers.json import DjangoJSONEncoder

    if request.is_ajax():
        print 'Its ajax from fullCalendar()'

    try:
        start = datetime.fromtimestamp(int(request.GET.get('start', False))).replace(tzinfo=utc)
        end = datetime.fromtimestamp(int(request.GET.get('end', False)))
    except ValueError:
        start = datetime.now().replace(tzinfo=utc)
        end = start + timedelta(days=7)

    entries = Visit.objects.all()
    print entries
    json_list = []
    for entry in entries:
        id = entry.id
        start = entry.start_date.strftime("%Y-%m-%dT%H:%M:%S")
        allDay = False

        json_entry = {'id': id, 'start': start, 'allDay': allDay, 'title': entry.dog.first_name}
        json_entry = json.dumps(json_entry, cls=DjangoJSONEncoder)
        json_list.append(json_entry)
    json_list.append({"date": "2017-06-24"})
    return HttpResponse(json.dumps(json_list), content_type='application/json', )


class BoardingView(DetailView):
    model = Visit


class BoardingView(ListView):
    model = Visit
    template_name = 'fullcalendar.html'


def in_the_house_view(request):
    date = request.GET.get('date')
    print "date:", date
    date = datetime.strptime(date, "%Y-%m-%d").date()
    print "new date: ", date, type(date)
    visits = Visit.objects.filter(
        Q(start_date__lte=date) &
        Q(end_date__gt=date)
    )
    context = {
        'visits': visits
    }
    return render_to_response('detail_view.html', context)
