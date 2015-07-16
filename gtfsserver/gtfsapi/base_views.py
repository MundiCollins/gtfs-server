import datetime
from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.utils.encoding import force_text
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework.filters import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor
from rest_framework_extensions.key_constructor.bits import (
    KeyBitBase, RetrieveSqlQueryKeyBit, ListSqlQueryKeyBit,
    PaginationKeyBit, QueryParamsKeyBit, UniqueMethodIdKeyBit,
    KwargsKeyBit
)
from multigtfs.models import Feed
from rest_framework import generics

class FeedNestedAPIView(object):
    def get_queryset(self):
        queryset = super(FeedNestedListAPIView, self).get_queryset()
        queryset = queryset.filter(feed=self.kwargs['feed_pk'])
        return queryset

class FeedNestedListAPIView(generics.ListAPIView, FeedNestedAPIView):
    pass

class FeedNestedRetrieveAPIView(generics.RetrieveAPIView, FeedNestedAPIView):
    pass

class FeedNestedViewSet(FeedNestedListAPIView, FeedNestedRetrieveAPIView, GenericViewSet):
    pass

class FeedNestedViewSet2(ReadOnlyModelViewSet):
    """
    Base class for viewset nested into feed.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(feed=kwargs['feed_pk'])
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



class FeedNestedCachedViewSet(FeedNestedViewSet):
    """
    Base class for viewset nested into feed.
    Filebased cached version
    """

    @cache_response(cache="filebased", key_func=CustomListKeyConstructor())
    def list(self, request, feed_pk=None):
        return super(FeedNestedCachedViewSet, self).list(request, feed_pk=feed_pk)

    @cache_response(cache="filebased", key_func=CustomObjectKeyConstructor())
    def retrieve(self, request, *args, **kwargs):
        return super(FeedNestedCachedViewSet, self).retrieve(request, *args, **kwargs)




#Cache invalidation
def change_api_updated_at(sender=None, instance=None, *args, **kwargs):
    value = datetime.datetime.utcnow()
    cache.set('%d_feed_api_updated_at_timestamp' % instance.id, value)
    cache.set('%d_feed_api_updated_at_timestamp' % 0, value)

post_save.connect(receiver=change_api_updated_at, sender=Feed, dispatch_uid="change_api_updated_at_post_save")
post_delete.connect(receiver=change_api_updated_at, sender=Feed, dispatch_uid="change_api_updated_at_post_delete")


class FeedThroughServiceNestedViewSet(ReadOnlyModelViewSet):
    """
    Base class for viewset nested into feed, but related to feed via Service.
    Lookup is done by service__feed__pk and "lookup_field" (default=pk)
    """

    def list(self, request, feed_pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(service__feed=feed_pk)
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
            "service__feed__pk" :  kwargs['feed_pk']
        }
        instance = self.queryset.get(**filter_params)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)



class FeedServiceNestedViewSet(ReadOnlyModelViewSet):
    """
    Base class for viewset nested into service nested into feed.
    Lookup is done by feed_pk, service_id and "lookup_field" (default=pk)
    """
    def list(self, request, feed_pk=None, service_service_id=None):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(service__feed__pk=feed_pk, service__service_id = service_service_id)
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



class FeedRouteNestedViewSet(ReadOnlyModelViewSet):
    """
    Base class for viewset nested into route nested into feed
    """

    def list(self, request, feed_pk=None, route_route_id=None):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(route__route_id=route_route_id)
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
            "route__feed__pk" :  kwargs['feed_pk'],
            "route__route_id" : kwargs['route_route_id']
        }
        instance = self.queryset.get(**filter_params)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)



class FeedThroughRouteNestedViewSet(ReadOnlyModelViewSet):

    def list(self, request, feed_pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(route__feed=feed_pk)
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
            "route__feed__pk" :  kwargs['feed_pk']
        }
        instance = self.queryset.get(**filter_params)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
