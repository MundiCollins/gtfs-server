import datetime
import time
from django.contrib.gis.geos import Point, Polygon
from django.contrib.gis.measure import D

from rest_framework import filters
from rest_framework import generics
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import cache_response

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

"""
class ProfileList(generics.ListAPIView):

    def dispatch(self, request, *args, **kwargs):
        global dispatch_time
        global render_time

        dispatch_start = time.time()
        ret = super(ProfileList, self).dispatch(request, *args, **kwargs)

        render_start = time.time()
        ret.render()
        render_time = time.time() - render_start

        dispatch_time = time.time() - dispatch_start

        return ret

    def list(self, request, *args, **kwargs):
        global serializer_time
        global db_time

        db_start = time.time()
        queryset = self.filter_queryset(self.get_queryset())
        db_time = time.time() - db_start

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer_start = time.time()
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            serializer_time = time.time() - serializer_start
            return self.get_paginated_response(data)

        serializer_start = time.time()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        serializer_time = time.time() - serializer_start
        return Response(data)


def started(sender, **kwargs):
    global started
    started = time.time()

def finished(sender, **kwargs):
    if 'db_time' not in globals():
        return
    global db_time

    total = time.time() - started
    api_view_time = dispatch_time - (render_time + serializer_time + db_time)
    request_response_time = total - dispatch_time

    print ("Database lookup               | %.4fs" % db_time)
    print ("Serialization                 | %.4fs" % serializer_time)
    print ("Django request/response       | %.4fs" % request_response_time)
    print ("API view                      | %.4fs" % api_view_time)
    print ("Response rendering            | %.4fs" % render_time)


from django.core.signals import request_started, request_finished
request_started.connect(started)
request_finished.connect(finished)
"""


from .cache_helpers import UpdatedAtDayForFeed

class ListCachedForToday(generics.ListAPIView):
    @cache_response(cache="filebased", key_func=UpdatedAtDayForFeed())
    def list(self, request, *args, **kwargs):
        return super(ListCachedForToday, self).list(request, *args, **kwargs)



class ServicesActiveView(ListCachedForToday):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ServiceFilter
    filter_fields = ('feed')


    def get_queryset(self):
        qset = super(ServicesActiveView, self).get_queryset()
        if self.kwargs.get('year', None):
            year, month, day = int(self.kwargs['year']), int(self.kwargs['month']), int(self.kwargs['day'])
            requested_date = datetime.date(year, month, day)
        else:
            requested_date = datetime.date.today()
        qset = active_services_from_date(requested_date, qset)
        return qset

class FeedServiceActiveView(ServicesActiveView, FeedNestedListAPIView):
    pass



class TripActiveView(ListCachedForToday):
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


class StopsActiveView(ListCachedForToday):
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



class StopTimesActiveView(ListCachedForToday):
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


from multigtfs.models.fields.seconds import Seconds

class TrajectoriesView(APIView):
    def get(self, request, feed_pk=None, year=None, month=None, day=None, hour=None, bbox=None):
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
        matching_routes = Route.objects.filter(feed__pk=feed_pk, geometry__within=geom)
        services = active_services_from_date(requested_date, Service.objects.filter(feed__pk=feed_pk))
        active_trips = Trip.objects.filter(route__in=matching_routes, service__in=services)



        e = end_datetime.hour*3600
        s = requested_datetime.hour*3600
        stop_times = StopTime.objects.filter(
            trip__in=active_trips,
            stop__point__within=geom).order_by('arrival_time','stop_sequence').select_related()
                #.filter(arrival_time__gte=s, arrival_time__lte=e)
        #st = StopTimeSerializer(stop_times, many=True)
        #print stop_times.count()
        #return Response(st.data)

        for t in stop_times:
            #if t.arrival_time.seconds < s:
            #    continue
            #if t.arrival_time.seconds > e:
            #        continue
            #print t.arrival_time
            if t.trip.trip_id not in out:
                out[t.trip.trip_id] = {
                    "route" : t.trip.route.route_id,
                    "feed" : t.trip.route.feed.pk,
                    "positions" : {}
                }

            out[t.trip.trip_id]["positions"][t.arrival_time.seconds] = t.stop.point.get_coords()

        return Response(out)
