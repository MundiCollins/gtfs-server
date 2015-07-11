from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import DjangoFilterBackend
from rest_framework_gis.filters import InBBoxFilter
from rest_framework.response import Response

from multigtfs.models import Agency, Route, Stop, Feed
from .serializers import AgencySerializer, GeoRouteSerializer, RouteSerializer, GeoStopSerializer, StopSerializer, FeedSerializer, FeedInfoSerializer
from rest_framework_extensions.cache.decorators import cache_response


import datetime
from django.core.cache import cache
from django.utils.encoding import force_text
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.key_constructor.constructors import (
    DefaultKeyConstructor
)
from rest_framework_extensions.key_constructor.bits import (
    KeyBitBase,
    RetrieveSqlQueryKeyBit,
    ListSqlQueryKeyBit,
    PaginationKeyBit
)

class UpdatedAtKeyBit(KeyBitBase):
    def get_data(self, **kwargs):
        feed_pk = kwargs['kwargs'].get('feed_pk', '0')
        key = '%s_feed_api_updated_at_timestamp' % feed_pk
        value = cache.get(key, None)
        if not value:
            value = datetime.datetime.utcnow()
            cache.set(key, value=value)
        return force_text(value)

class CustomObjectKeyConstructor(DefaultKeyConstructor):
    retrieve_sql = RetrieveSqlQueryKeyBit()
    updated_at = UpdatedAtKeyBit()

class CustomListKeyConstructor(DefaultKeyConstructor):
    list_sql = ListSqlQueryKeyBit()
    pagination = PaginationKeyBit()
    updated_at = UpdatedAtKeyBit()


#Cache invalidation
from django.db.models.signals import post_save, post_delete

def change_api_updated_at(sender=None, instance=None, *args, **kwargs):
    value = datetime.datetime.utcnow()
    cache.set('%d_feed_api_updated_at_timestamp' % instance.id, value)
    cache.set('%d_feed_api_updated_at_timestamp' % 0, value)

post_save.connect(receiver=change_api_updated_at, sender=Feed)
post_delete.connect(receiver=change_api_updated_at, sender=Feed)


class InBBoxFilterBBox(InBBoxFilter):
    bbox_param = "bbox"


class FeedViewSet(ModelViewSet):
    serializer_class = FeedSerializer
    queryset = Feed.objects.all()


class FeedGeoViewSet(ModelViewSet):
    serializer_class = FeedInfoSerializer
    queryset = Feed.objects.all()


class FeedNestedViewSet(ModelViewSet):

    @cache_response(cache="filebased", key_func=CustomListKeyConstructor())
    def list(self, request, feed_pk=None):
        queryset= self.queryset.filter(feed=feed_pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @cache_response(cache="filebased", key_func=CustomObjectKeyConstructor())
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
