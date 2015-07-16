import django_filters
from multigtfs.models import Trip, Service

class TripFilter(django_filters.FilterSet):
    feed = django_filters.CharFilter(name="service__feed")
    route_id = django_filters.CharFilter(name="route__route_id")

    """
    This filter is needed to lookup active trips by "feed" query parameter
    """
    class Meta:
        model = Trip
        fields = ["feed", "route_id", "route"]


class ServiceFilter(django_filters.FilterSet):
    """
    This filter is needed to lookup active trips by "feed" query parameter
    """

    class Meta:
        model = Service
        fields = ["id", "feed", "monday"]
