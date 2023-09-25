from django.utils import timezone
from calendar import monthrange
from django.shortcuts import render
import calendar

def generate_monthly_calendar(year, month):
    # Generate the calendar data for the given year and month
    _, num_days = monthrange(year, month)
    first_day_weekday, _ = monthrange(year, month)
    monthly_calendar = []
    day_counter = 1
    for week_num in range(6):
        week = []
        for day_num in range(7):
            if week_num == 0 and day_num < first_day_weekday:
                week.append(None)
            elif day_counter <= num_days:
                week.append(day_counter)
                day_counter += 1
            else:
                week.append(None)
        monthly_calendar.append(week)
    return monthly_calendar


def calendar_view(request):
    # Get the current year and month
    today = timezone.now()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    # Generate the calendar data for the selected year and month
    monthly_calendar = generate_monthly_calendar(year, month)

    # Calculate the previous and next months
    prev_month = today.replace(
        year=year, month=month, day=1) - timezone.timedelta(days=1)
    next_month = today.replace(
        year=year, month=month, day=1) + timezone.timedelta(days=32)

    return render(request, 'calendar.html', {
        'monthly_calendar': monthly_calendar,
        'prev_month': prev_month,
        'next_month': next_month,
    })
