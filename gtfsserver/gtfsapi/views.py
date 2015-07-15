from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.filters import DjangoFilterBackend
from rest_framework_gis.filters import InBBoxFilter
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework.decorators import detail_route, list_route
from rest_framework.views import APIView
from rest_framework import generics
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
    PaginationKeyBit,
    QueryParamsKeyBit,
    UniqueMethodIdKeyBit,
    KwargsKeyBit
)

from .helpers import active_services_from_date

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
    #retrieve_sql = RetrieveSqlQueryKeyBit()
    updated_at = UpdatedAtKeyBit()
    #query = QueryParamsKeyBit()
    meth = UniqueMethodIdKeyBit()
    #kwargs = KwargsKeyBit()

class CustomListKeyConstructor(DefaultKeyConstructor):
    #list_sql = ListSqlQueryKeyBit()
    #pagination = PaginationKeyBit()
    updated_at = UpdatedAtKeyBit()
    #query = QueryParamsKeyBit()
    meth = UniqueMethodIdKeyBit()
    #kwargs = KwargsKeyBit()


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


class FeedViewSet(ReadOnlyModelViewSet):
    serializer_class = FeedSerializer
    queryset = Feed.objects.all()


class FeedGeoViewSet(ReadOnlyModelViewSet):
    serializer_class = FeedInfoSerializer
    queryset = Feed.objects.all()


class FeedNestedCachedViewSet(ReadOnlyModelViewSet):

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



class FeedNestedViewSet(ReadOnlyModelViewSet):

    def list(self, request, *args, **kwargs):
        queryset= self.queryset.filter(feed=kwargs['feed_pk'])
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        lookup_field = self.lookup_field or 'pk'
        filter_params = { lookup_field : kwargs[lookup_field], "feed__pk" : kwargs['feed_pk'] }
        instance = self.queryset.get(**filter_params)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)



class AgencyViewSet(ReadOnlyModelViewSet):
    serializer_class = AgencySerializer
    queryset = Agency.objects.all()


class FeedAgencyViewSet(FeedNestedViewSet):
    lookup_field = "agency_id"
    serializer_class = AgencySerializer
    queryset = Agency.objects.all()


class GeoRouteViewSet(FeedNestedCachedViewSet):
    serializer_class = GeoRouteSerializer
    queryset = Route.objects.all()
    pagination_class = None
    filter_backends = (InBBoxFilterBBox, )
    bbox_filter_field = 'geometry'


class RouteViewSet(FeedNestedViewSet):
    lookup_field = "route_id"
    serializer_class = RouteSerializer
    queryset = Route.objects.all()

    @list_route()
    def _rtype(self, request, feed_pk=None):
        types = self.queryset.filter(feed__pk=feed_pk).values_list('rtype', flat=True).distinct()
        avail_types = dict(Route._meta.get_field('rtype').choices)
        out_types = {}
        for x in types:
            out_types[x] = avail_types[x]
        return Response(out_types)


class GeoStopViewSet(FeedNestedCachedViewSet):
    serializer_class = GeoStopSerializer
    queryset = Stop.objects.all()
    pagination_class = None
    filter_backends = (InBBoxFilterBBox, )
    bbox_filter_field = 'point'

class StopViewSet(FeedNestedViewSet):
    lookup_field = "stop_id"
    serializer_class = StopSerializer
    queryset = Stop.objects.all()


class ServiceViewSet(FeedNestedViewSet):
    lookup_field = "service_id"
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceSerializer
        if self.action == 'retrieve':
            return ServiceWithDatesSerializer
        return serializers.Default



class ServiceFeedNestedViewSet(ReadOnlyModelViewSet):

    def list(self, request, feed_pk=None):
        queryset= self.queryset.filter(service__feed=feed_pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, feed_pk=None):
        instance = self.queryset.get(pk=pk, service__feed__pk=feed_pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ServiceNestedViewSet(ReadOnlyModelViewSet):

    def list(self, request, feed_pk=None, service_service_id=None):
        queryset= self.queryset.filter(service__feed__pk=feed_pk, service__service_id = service_service_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        lookup_field = self.lookup_field or 'pk'
        filter_params = {
            lookup_field : kwargs[lookup_field],
            "service__feed__pk" :  kwargs['feed_pk'],
            "service__service_id" : kwargs['service_service_id']
        }
        instance = self.queryset.get(**filter_params)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class RouteNestedViewSet(ReadOnlyModelViewSet):


    def list(self, request, feed_pk=None, route_pk=None):
        queryset= self.queryset.filter(route=route_pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, feed_pk=None, route_pk=None):
        instance = self.queryset.get(pk=pk, route__pk=service_pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class RouteFeedNestedViewSet(ReadOnlyModelViewSet):

    def list(self, request, feed_pk=None):
        queryset= self.queryset.filter(route__feed=feed_pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, feed_pk=None):
        instance = self.queryset.get(pk=pk, route__feed__pk=feed_pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ServiceServiceDateViewSet(ServiceNestedViewSet):
    serializer_class = ServiceDateSerializer
    queryset = ServiceDate.objects.all()

class FeedServiceDateViewSet(ServiceFeedNestedViewSet):
    serializer_class = ServiceDateSerializer
    queryset = ServiceDate.objects.all()


class RouteTripViewSet(RouteNestedViewSet):
    serializer_class = TripSerializer
    queryset = Trip.objects.all()

class FeedRouteTripViewSet(RouteFeedNestedViewSet):
    serializer_class = TripSerializer
    queryset = Trip.objects.all()

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from rest_framework import filters

class StopsNearView(generics.ListAPIView):
    serializer_class = StopSerializerWithDistance
    queryset = Stop.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('feed', )


    def get_queryset(self):
        queryset = super(StopsNearView, self).get_queryset()
        queryset = self.filter_queryset(queryset)
        radius = self.request.query_params.get('radius', 1.0)
        radius = float(radius)
        x = self.kwargs['x']
        y = self.kwargs['y']
        point = Point(float(x), float(y))
        queryset = queryset.distance(point).filter(point__distance_lt=(point, D(km=radius)))
        return queryset


class GeoStopsNearView(StopsNearView):
    serializer_class = GeoStopSerializerWithDistance
    pagination_class = None



class ServicesActiveView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('feed', )

    def get_queryset(self):
        qset = super(ServicesActiveView, self).get_queryset()
        year, month, day = int(self.kwargs['year']), int(self.kwargs['month']), int(self.kwargs['day'])
        requested_date = datetime.date(year, month, day)
        qset = active_services_from_date(requested_date, qset)
        return qset



class TripsActiveView(generics.ListAPIView):
    serializer_class = TripSerializer
    queryset = Trip.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('service__feed', )

    def get_queryset(self):
        qset = super(TripsActiveView, self).get_queryset()
        year, month, day = int(self.kwargs['year']), int(self.kwargs['month']), int(self.kwargs['day'])
        requested_date = datetime.date(year, month, day)
        services = active_services_from_date(requested_date)
        active_trips = qset.filter(service__in=services)
        return active_trips
