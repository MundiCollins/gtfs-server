from rest_framework.decorators import detail_route, list_route
from rest_framework_gis.filters import InBBoxFilter
from multigtfs.models import Agency, Route, Service, Trip, ServiceDate, Stop
from .serializers import  (
    AgencySerializer, RouteSerializer, GeoRouteSerializer, ServiceSerializer,
    TripSerializer, StopSerializer, GeoStopSerializer,
    ServiceDateSerializer, ServiceWithDatesSerializer )

from .base_views import  (FeedNestedViewSet, FeedNestedCachedViewSet,
    FeedServiceNestedViewSet, FeedThroughServiceNestedViewSet,
    FeedRouteNestedViewSet, FeedThroughRouteNestedViewSet )

class InBBoxFilterBBox(InBBoxFilter):
    bbox_param = "bbox"


class FeedAgencyViewSet(FeedNestedViewSet):
    """
    Viewset for agencies (nested into feed - lookup by agency_id)
    """
    lookup_field = "agency_id"
    serializer_class = AgencySerializer
    queryset = Agency.objects.all()


class FeedRouteViewSet(FeedNestedViewSet):
    """
    Viewset for Route (nested in feed - lookup by route_id)
    """
    lookup_field = "route_id"
    serializer_class = RouteSerializer
    queryset = Route.objects.all()

    @list_route()
    def _rtype(self, request, feed_pk=None):
        """
        Get an object with the occurring values/descriptions of "rtype" (route type) field.
        """
        types = self.queryset.filter(feed__pk=feed_pk).values_list('rtype', flat=True).distinct()
        avail_types = dict(Route._meta.get_field('rtype').choices)
        out_types = {}
        for x in types:
            out_types[x] = avail_types[x]
        return Response(out_types)


class FeedGeoRouteViewSet(FeedNestedCachedViewSet):
    """
    GeoViewset for Route (nested in feed - lookup by route_id)
    """
    lookup_field = "route_id"
    serializer_class = GeoRouteSerializer
    queryset = Route.objects.all()
    pagination_class = None
    filter_backends = (InBBoxFilterBBox, )
    bbox_filter_field = 'geometry'


class FeedStopViewSet(FeedNestedViewSet):
    """
    Viewset for Stop (nested in feed - lookup by stop_id)
    """
    lookup_field = "stop_id"
    serializer_class = StopSerializer
    queryset = Stop.objects.all()



class FeedGeoStopViewSet(FeedNestedCachedViewSet):
    """
    GeoViewset for Stop (nested in feed - lookup by stop_id)
    """
    lookup_field = "stop_id"
    serializer_class = GeoStopSerializer
    queryset = Stop.objects.all()
    pagination_class = None
    filter_backends = (InBBoxFilterBBox, )
    bbox_filter_field = 'point'



class FeedServiceViewSet(FeedNestedViewSet):
    """
    Viewset for Service (nested in feed - lookup by service_id)
    """
    lookup_field = "service_id"
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceSerializer
        if self.action == 'retrieve':
            return ServiceWithDatesSerializer
        return serializers.Default


class ServiceServiceDateViewSet(FeedServiceNestedViewSet):
    """
    Viewset for getting service dates nested into services
    lookup is done by feed_pk, service_id (and id for getting single object)
    """
    serializer_class = ServiceDateSerializer
    queryset = ServiceDate.objects.all()

class FeedServiceDateViewSet(FeedThroughServiceNestedViewSet):
    """
    Viewset for getting ServiceDate directly from feed
    lookup is done by feed_id (and id for getting single object)
    """
    serializer_class = ServiceDateSerializer
    queryset = ServiceDate.objects.all()


class RouteTripViewSet(FeedRouteNestedViewSet):
    """
    Viewset for Trip nested into Route nested into Feed
    lookup by feed_id, route_id, trip_id
    """
    lookup_field = "trip_id"
    serializer_class = TripSerializer
    queryset = Trip.objects.all()

class FeedRouteTripViewSet(FeedThroughRouteNestedViewSet):
    """
    Viewset for Trip nested into  Feed
    lookup by feed_id, trip_id
    """
    lookup_field = "trip_id"
    serializer_class = TripSerializer
    queryset = Trip.objects.all()
