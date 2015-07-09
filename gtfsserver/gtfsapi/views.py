from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import DjangoFilterBackend
from rest_framework_gis.filters import InBBoxFilter
from rest_framework.response import Response

from multigtfs.models import Agency, Route, Stop, Feed
from .serializers import AgencySerializer, GeoRouteSerializer, RouteSerializer, GeoStopSerializer, StopSerializer, FeedSerializer


class InBBoxFilterBBox(InBBoxFilter):
    bbox_param = "bbox"


class FeedViewSet(ModelViewSet):
    serializer_class = FeedSerializer
    queryset = Feed.objects.all()


class FeedNestedViewSet(ModelViewSet):

    def list(self, request, feed_pk=None):
        queryset= self.queryset.filter(feed=feed_pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, feed_pk=None):
        instance = self.queryset.get(pk=pk, feed_pk=feed_pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)



class AgencyViewSet(FeedNestedViewSet):
    serializer_class = AgencySerializer
    queryset = Agency.objects.all()


class GeoRouteViewSet(FeedNestedViewSet):
    serializer_class = GeoRouteSerializer
    queryset = Route.objects.all()
    pagination_class = None
    filter_backends = (InBBoxFilterBBox, )
    bbox_filter_field = 'geometry'

class RouteViewSet(FeedNestedViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()


class GeoStopViewSet(FeedNestedViewSet):
    serializer_class = GeoStopSerializer
    queryset = Stop.objects.all()
    pagination_class = None
    filter_backends = (InBBoxFilterBBox, )
    bbox_filter_field = 'point'

class StopViewSet(FeedNestedViewSet):
    serializer_class = StopSerializer
    queryset = Stop.objects.all()
