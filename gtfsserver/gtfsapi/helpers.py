from multigtfs.models import Agency, Route, Stop, Feed, Service, ServiceDate, Trip
from django.db.models import Q

def active_services_from_date(requested_date, queryset=None):
    qset = queryset or Service.objects.all()

    days = ["sunday", "monday", "tuesday","wednesday","thursday","friday","saturday" ]
    days_pos = int(requested_date.strftime("%w"))
    current_day = days[days_pos]
    params = { current_day : True }
    qset = qset.filter(**params)
    start_date_q = Q(start_date=None) |  Q(start_date__lte=requested_date)
    end_date_q= Q(end_date=None) |  Q(end_date__gte=requested_date)
    qset = qset.filter (start_date_q | end_date_q)

    #considering calendar dates (service_dates)
    valid_dates = ServiceDate.objects.filter(date=requested_date, exception_type=1)
    services_for_valid = valid_dates.values_list('service', flat=True)
    qset = qset.filter(pk__in=services_for_valid)

    invalid_dates = ServiceDate.objects.filter(date=requested_date, exception_type=2)
    services_for_invalid = invalid_dates.values_list('service', flat=True)
    qset = qset.exclude(pk__in=services_for_invalid)

    return qset
