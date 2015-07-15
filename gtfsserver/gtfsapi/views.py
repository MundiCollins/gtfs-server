from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.filters import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.views import APIView

from django.db.models import Q

from multigtfs.models import Agency, Route, Stop, Feed, Service, ServiceDate, Trip
from .serializers import ( AgencySerializer,
                            GeoRouteSerializer, RouteSerializer, RouteWithTripsSerializer,
                            GeoStopSerializer, StopSerializer, StopSerializerWithDistance,
                            GeoStopSerializerWithDistance,
                            FeedSerializer,
                            FeedInfoSerializer, ServiceSerializer, ServiceWithDatesSerializer,
                            ServiceDateSerializer,
                            TripSerializer )





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
    Viewset for agencies (global)
    """
    serializer_class = AgencySerializer
    queryset = Agency.objects.all()
