from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import DjangoFilterBackend
from rest_framework_gis.filters import InBBoxFilter

from multigtfs.models import Agency, Route, Stop
from .serializers import AgencySerializer, GeoRouteSerializer, RouteSerializer, GeoStopSerializer, StopSerializer


class InBBoxFilterBBox(InBBoxFilter):
    bbox_param = "bbox"

class AgencyViewSet(ModelViewSet):
    serializer_class = AgencySerializer
    queryset = Agency.objects.all()


class GeoRouteViewSet(ModelViewSet):
    serializer_class = GeoRouteSerializer
    queryset = Route.objects.all()
    pagination_class = None
    filter_backends = (InBBoxFilterBBox, )
    bbox_filter_field = 'geometry'

class RouteViewSet(ModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()


class GeoStopViewSet(ModelViewSet):
    serializer_class = GeoStopSerializer
    queryset = Stop.objects.all()
    pagination_class = None
    filter_backends = (InBBoxFilterBBox, )
    bbox_filter_field = 'point'

class StopViewSet(ModelViewSet):
    serializer_class = StopSerializer
    queryset = Stop.objects.all()
