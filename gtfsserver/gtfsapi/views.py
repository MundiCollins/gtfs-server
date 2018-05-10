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

from multigtfs.models import Agency, Route, Stop, Feed, Service, ServiceDate, Trip, StopTime, Ride, NewStop, NewRoute
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

        print json_data

        data = json_data['data'][0]

        route_id = int(data['route_id'])
        routes = data['route']
        stops = data['stops']

        ride = Ride(route=Route.objects.get(id=route_id))
        ride.save()
        ride_id = ride.id

        print route_id
        print routes
        print stops

        for i in routes:
            route = NewRoute(ride=Ride.objects.get(id=ride_id), latitude=i['latitude'], longitude=i['longitude'], time=i['time'])
            route.save()

        for i in stops:
            latitude = i['latitude']
            longitude = i['longitude']
            arrival_time = i['arrival_time']
            departure_time = i['departure_time']
            new_stop = NewStop(ride=Ride.objects.get(id=ride_id), latitude=latitude, longitude=longitude, arrival_time=arrival_time, departure_time=departure_time)
            new_stop.save()

        return Response({"success": True})