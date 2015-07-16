import datetime

from django.contrib.gis.geos import Point, Polygon
from django.contrib.gis.measure import D

from rest_framework import filters
from rest_framework import generics
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
import django_filters

from multigtfs.models import Stop, Service, Trip, StopTime, Route

from .helpers import active_services_from_date
from .serializers import (
    StopSerializerWithDistance,StopWithTripsAndRoutesSerializer, ServiceSerializer, TripSerializer, StopSerializer,
    GeoStopSerializerWithDistance, StopTimeSerializer )
from .base_views import (
    FeedNestedListAPIView, FeedThroughServiceNestedListAPIView, FeedStopNestedListAPIView,
    FeedThroughStopNestedListAPIView )

from .filters import TripFilter, ServiceFilter, StopFilter

class StopsNearView(generics.ListAPIView):
    serializer_class = StopSerializerWithDistance
    queryset = Stop.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('feed', )


    def get_queryset(self):
        queryset = super(StopsNearView, self).get_queryset()
        radius = self.request.query_params.get('radius', 1.0)
        radius = float(radius)
        x = self.kwargs['x']
        y = self.kwargs['y']
        point = Point(float(x), float(y))
        queryset = queryset.distance(point).filter(point__distance_lt=(point, D(km=radius)))
        return queryset


class FeedStopsNearView(StopsNearView, FeedNestedListAPIView):
    pass

class GeoStopsNearView(StopsNearView):
    serializer_class = GeoStopSerializerWithDistance
    pagination_class = None

class FeedGeoStopsNearView(GeoStopsNearView, FeedNestedListAPIView ):
    pass


class ServicesActiveView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ServiceFilter
    filter_fields = ('feed')

    def get_queryset(self):
        qset = super(ServicesActiveView, self).get_queryset()
        if year:
            year, month, day = int(self.kwargs['year']), int(self.kwargs['month']), int(self.kwargs['day'])
            requested_date = datetime.date(year, month, day)
        else:
            requested_date = datetime.date.today()
        qset = active_services_from_date(requested_date, qset)
        return qset

class FeedServiceActiveView(ServicesActiveView, FeedNestedListAPIView):
    pass



class TripActiveView(generics.ListAPIView):
    serializer_class = TripSerializer
    queryset = Trip.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = TripFilter
    #filter_fields = ('service__feed', )

    def get_queryset(self):
        qset = super(TripActiveView, self).get_queryset()
        year = self.kwargs.get('year', None)
        if year:
            year, month, day = int(self.kwargs['year']), int(self.kwargs['month']), int(self.kwargs['day'])
            requested_date = datetime.date(year, month, day)
        else:
            requested_date = datetime.date.today()
        services = active_services_from_date(requested_date)
        active_trips = qset.filter(service__in=services)
        return active_trips

class FeedTripActiveView(TripActiveView, FeedThroughServiceNestedListAPIView):
    pass


class StopsActiveView(generics.ListAPIView):
    """
    Stops associated with Active Trips
    """
    serializer_class = StopSerializer
    queryset = Stop.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    #filter_class = StopFilter
    #filter_fields = ('service__feed', )

    def get_queryset(self):
        qset = super(StopsActiveView, self).get_queryset()
        year = self.kwargs.get('year', None)
        if year:
            year, month, day = int(self.kwargs['year']), int(self.kwargs['month']), int(self.kwargs['day'])
            requested_date = datetime.date(year, month, day)
        else:
            requested_date = datetime.date.today()

        services = active_services_from_date(requested_date)
        active_trips = Trip.objects.filter(service__in=services)
        route = self.request.query_params.get('route', None)
        route_id = self.request.query_params.get('route_id', None)

        if route:
            active_trips = active_trips.filter(route=route)
        if route_id:
            active_trips = active_trips.filter(route__route_id=route_id)

        active_stop_times_pks = StopTime.objects.filter(trip__in=active_trips).values_list('stop__pk', flat=True)
        active_stops = qset.filter(pk__in=active_stop_times_pks).distinct()
        return active_stops

class FeedStopActiveView(StopsActiveView, FeedNestedListAPIView):
    pass



class StopTimesActiveView(generics.ListAPIView):
    """
    Stops associated with Active Trips
    """
    serializer_class = StopTimeSerializer
    queryset = StopTime.objects.all()
    #filter_backends = (filters.DjangoFilterBackend,)
    #filter_class = StopFilter
    #filter_fields = ('service__feed', )

    def get_queryset(self):
        qset = super(StopTimesActiveView, self).get_queryset()
        year = self.kwargs.get('year', None)
        if year:
            year, month, day = int(self.kwargs['year']), int(self.kwargs['month']), int(self.kwargs['day'])
            requested_date = datetime.date(year, month, day)
        else:
            requested_date = datetime.date.today()

        services = active_services_from_date(requested_date)
        active_trips = Trip.objects.filter(service__in=services)

        route = self.request.query_params.get('route', None)
        route_id = self.request.query_params.get('route_id', None)
        if route:
            active_trips = active_trips.filter(route=route)
        if route_id:
            active_trips = active_trips.filter(route__route_id=route_id)

        active_stop_times = qset.filter(trip__in=active_trips)

        stop = self.request.query_params.get('stop', None)
        stop_id = self.request.query_params.get('stop_id', None)

        if stop:
            active_stop_times = active_stop_times.filter(stop__pk=stop)
        if stop_id:
            active_stop_times = active_stop_times.filter(stop__stop_id=stop_id)



        return active_stop_times

class FeedStopStopTimesActiveView(StopTimesActiveView, FeedStopNestedListAPIView):
    """
    Active stop times for a feed and a stop (lookup by stop_id)
    """
    pass

class FeedStopTimesActiveView(StopTimesActiveView, FeedThroughStopNestedListAPIView):
    """
    Active stop times for a feed.
    """
    pass




class TrajectoriesView(APIView):
    def get(self, request, year=None, month=None, day=None, hour=None, bbox=None):
        out = {}
        today = datetime.date.today()
        bbox=[float(x) for x in bbox.split(",")]
        if year:

            year, month, day, hour = int(year), int(month), int(day), int(hour)
            requested_datetime = datetime.datetime(year, month, day, hour)
            requested_date = datetime.date(year, month, hour)
        else:
            if hour:
                hour = int(hour)
                requested_datetime = datetime.datetime(today.year, today.month, today.day, hour)
            else:
                now = datetime.datetime.now()
                requested_datetime = datetime.datetime(now.year, now.month, now.day, now.hour)
            requested_date = today

        end_datetime = requested_datetime + datetime.timedelta(hours=1)


        geom = Polygon.from_bbox(bbox)
        matching_routes = Route.objects.filter(geometry__within=geom)
        feeds = matching_routes.values_list('feed', flat=True).distinct()
        services = active_services_from_date(requested_date, Service.objects.filter(feed__in=feeds))
        active_trips = Trip.objects.filter(route__in=matching_routes, service__in=services)

        def in_hour(seconds):
            return end_datetime.hour * 60 * 60 < seconds and seconds > requested_datetime.hour * 60 * 60

        stop_times = StopTime.objects.filter(
            trip__in=active_trips,
            stop__point__within=geom).order_by('stop_sequence')
            
        for t in stop_times:
            if not in_hour(t.arrival_time.seconds):
                continue
            if t.trip.trip_id not in out:
                out[t.trip.trip_id] = {
                    "route" : t.trip.route.route_id,
                    "feed" : t.trip.route.feed.pk,
                    "positions" : {}
                }

            out[t.trip.trip_id]["positions"][t.arrival_time.seconds] = t.stop.point.get_coords()

        return Response(out)
