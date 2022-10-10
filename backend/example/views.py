import calendar

from django.shortcuts import render
from django.utils import timezone


def index(request):
    now = timezone.now()
    calendar_html = calendar.HTMLCalendar().formatmonth(now.year, now.month)

    return render(
        request,
        "example/calendar.html",
        {
            "current_year": now.year,
            "calendar_html": calendar_html,
        },
    )
