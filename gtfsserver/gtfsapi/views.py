import json
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.filters import DjangoFilterBackend

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.views import APIView

from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from stronghold.decorators import public

from multigtfs.models import Agency, Route, Stop, Feed, Service, ServiceDate, Trip, StopTime, Ride, NewStop
from .serializers import (
    AgencySerializer,
    GeoRouteSerializer, RouteSerializer, RouteWithTripsSerializer,
    GeoStopSerializer, StopSerializer, StopSerializerWithDistance,
    GeoStopSerializerWithDistance,
    FeedSerializer,
    FeedInfoSerializer, ServiceSerializer, ServiceWithDatesSerializer,
    ServiceDateSerializer,
    TripSerializer,
    StopTimeSerializer )



class FeedViewSet(ReadOnlyModelViewSet):
    """
    Viewset for Feed model
    """
    serializer_class = FeedSerializer
    queryset = Feed.objects.all()


class FeedGeoViewSet(FeedViewSet):
    """
    Viewset for Feed model - extended info (changes serializer)
    """
    serializer_class = FeedInfoSerializer


class AgencyViewSet(ReadOnlyModelViewSet):
    """
    Viewset for Agency (global)
    """
    serializer_class = AgencySerializer
    queryset = Agency.objects.all()


class ServiceViewSet(ReadOnlyModelViewSet):
    """
    Viewset for Service (global)
    """
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()


class RouteViewSet(ReadOnlyModelViewSet):
    """
    Viewset for Route (global)
    """
    serializer_class = RouteSerializer
    queryset = Route.objects.all()


class StopViewSet(ReadOnlyModelViewSet):
    """
    Viewset for Stop (global)
    """
    serializer_class = StopSerializer
    queryset = Stop.objects.all()


class TripViewSet(ReadOnlyModelViewSet):
    """
    Viewset for Trip (global)
    """
    serializer_class = TripSerializer
    queryset = Trip.objects.all()


class ServiceDateViewSet(ReadOnlyModelViewSet):
    """
    Viewset for ServiceDate (global)
    """
    serializer_class = ServiceDateSerializer
    queryset = ServiceDate.objects.all()


class StopTimeViewSet(ReadOnlyModelViewSet):
    """
    Viewset for StopTime (global)
    """
    serializer_class = StopTimeSerializer
    queryset = StopTime.objects.all()


class RideView(APIView):
    authentication_classes = []
    permission_classes = []

    @csrf_exempt
    @method_decorator(public)
    def post(self, request):
        json_data = json.loads(request.body)

        data = json_data.get('data', None)

        route_id = data.get('route_id', None)
        route = data.get('route', None)
        stops = data.get('stops', None)

        route_latitude = route.get('latitude', None)
        route_longitude = route.get('longitude', None)

        ride = Ride(route=route_id, route_latitude=route_latitude, route_longitude=route_longitude)
        ride.save()
        ride_id = ride.id

        for i in stops:
            latitude = i.get('latitude', None)
            longitude = i.get('longitude', None)
            arrival_time = i.get('arrival_time', None)
            departure_time = i.get('departure_time', None)
            new_stop = NewStop(ride=ride_id, latitude=latitude, longitude=longitude, arrival_time=arrival_time, departure_time=departure_time)
            new_stop.save()

        return Response({"success": True})