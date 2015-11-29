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

from multigtfs.models import Feed, Trip
from rest_framework import generics

from .cache_helpers import CustomObjectKeyConstructor, CustomListKeyConstructor

class FeedNestedMixin(object):
    def get_queryset(self):
        queryset = super(FeedNestedMixin, self).get_queryset()
        queryset = queryset.filter(feed=self.kwargs['feed_pk'])
        # Set up eager loading to avoid N+1 selects
        ser_class = self.get_serializer_class()
        if hasattr(ser_class, "setup_eager_loading"):
            queryset = ser_class.setup_eager_loading(queryset)  
        return queryset

class FeedNestedListAPIView( FeedNestedMixin, generics.ListAPIView ):
    pass

class FeedNestedRetrieveAPIView(FeedNestedMixin, generics.RetrieveAPIView):
    pass

class FeedNestedViewSet(FeedNestedListAPIView, FeedNestedRetrieveAPIView, GenericViewSet):
    pass




class FeedNestedCachedViewSet(FeedNestedViewSet):
    """
    Base class for viewset nested into feed.
    Filebased cached version
    """

    @cache_response(cache="filebased", key_func=CustomListKeyConstructor())
    def list(self, request, feed_pk=None):
        return super(FeedNestedCachedViewSet, self).list(request, feed_pk=feed_pk)

    #@cache_response(cache="filebased", key_func=CustomObjectKeyConstructor())
    def retrieve(self, request, *args, **kwargs):
        return super(FeedNestedCachedViewSet, self).retrieve(request, *args, **kwargs)




#Cache invalidation
def change_api_updated_at(sender=None, instance=None, *args, **kwargs):
    value = datetime.datetime.utcnow()
    cache.set('%d_feed_api_updated_at_timestamp' % instance.id, value)
    #cache.set('%d_feed_api_updated_at_timestamp' % 0, value)

post_save.connect(receiver=change_api_updated_at, sender=Feed, dispatch_uid="change_api_updated_at_post_save")
post_delete.connect(receiver=change_api_updated_at, sender=Feed, dispatch_uid="change_api_updated_at_post_delete")


class FeedThroughServiceNestedMixin(object):
    def get_queryset(self):
        queryset = super(FeedThroughServiceNestedMixin, self).get_queryset()
        queryset = queryset.filter(service__feed__pk=self.kwargs['feed_pk'])
        return queryset

class FeedThroughServiceNestedListAPIView( FeedThroughServiceNestedMixin, generics.ListAPIView ):
    pass

class FeedThroughServiceNestesRetrieveAPIView(FeedThroughServiceNestedMixin, generics.RetrieveAPIView):
    pass

class FeedThroughServiceNestedViewSet(FeedThroughServiceNestedListAPIView, FeedThroughServiceNestesRetrieveAPIView, GenericViewSet):
    pass


class FeedServiceNestedMixin(object):
    def get_queryset(self):
        queryset = super(FeedServiceNestedMixin, self).get_queryset()
        queryset = queryset.filter(
            service__feed__pk=self.kwargs['feed_pk'],
            service__service_id = self.kwargs['service_service_id']
        )
        return queryset

class FeedServiceNestedListAPIView( FeedServiceNestedMixin, generics.ListAPIView ):
    pass

class FeedServiceNestedNestesRetrieveAPIView(FeedServiceNestedMixin, generics.RetrieveAPIView):
    pass

class FeedServiceNestedViewSet(FeedServiceNestedListAPIView, FeedServiceNestedNestesRetrieveAPIView, GenericViewSet):
    pass



class FeedRouteNestedMixin(object):
    def get_queryset(self):
        queryset = super(FeedRouteNestedMixin, self).get_queryset()
        queryset = queryset.filter(
            route__feed__pk=self.kwargs['feed_pk'],
            route__route_id = self.kwargs['route_route_id']
        )
        return queryset

class FeedRouteNestedListAPIView( FeedRouteNestedMixin, generics.ListAPIView ):
    pass

class FeedRouteNestedNestesRetrieveAPIView(FeedRouteNestedMixin, generics.RetrieveAPIView):
    pass

class FeedRouteNestedViewSet(FeedRouteNestedListAPIView, FeedRouteNestedNestesRetrieveAPIView, GenericViewSet):
    """
    Base class for viewset nested into route nested into feed
    """
    pass



class FeedThroughRouteNestedMixin(object):
    def get_queryset(self):
        queryset = super(FeedThroughRouteNestedMixin, self).get_queryset()
        queryset = queryset.filter(route__feed__pk=self.kwargs['feed_pk'])
        return queryset

class FeedThroughRouteNestedListAPIView( FeedThroughRouteNestedMixin, generics.ListAPIView ):
    pass

class FeedThroughRouteNestesRetrieveAPIView(FeedThroughRouteNestedMixin, generics.RetrieveAPIView):
    pass

class FeedThroughRouteNestedViewSet(FeedThroughRouteNestedListAPIView, FeedThroughRouteNestesRetrieveAPIView, GenericViewSet):
    pass


class FeedStopNestedMixin(object):
    def get_queryset(self):
        queryset = super(FeedStopNestedMixin, self).get_queryset()
        queryset = queryset.filter(
            stop__feed__pk=self.kwargs['feed_pk'],
            stop__stop_id = self.kwargs['stop_stop_id']
        )
        return queryset

class FeedStopNestedListAPIView( FeedStopNestedMixin, generics.ListAPIView ):
    pass

class FeedStopNestedNestesRetrieveAPIView(FeedStopNestedMixin, generics.RetrieveAPIView):
    pass

class FeedStopNestedViewSet(FeedStopNestedListAPIView, FeedStopNestedNestesRetrieveAPIView, GenericViewSet):
    """
    Base class for viewset nested into stop nested into feed
    """
    pass





class FeedThroughStopNestedMixin(object):
    def get_queryset(self):
        queryset = super(FeedThroughStopNestedMixin, self).get_queryset()
        queryset = queryset.filter(stop__feed__pk=self.kwargs['feed_pk'])
        return queryset

class FeedThroughStopNestedListAPIView( FeedThroughStopNestedMixin, generics.ListAPIView ):
    pass

class FeedThroughStopNestedRetrieveAPIView(FeedThroughStopNestedMixin, generics.RetrieveAPIView):
    pass

class FeedThroughStopNestedViewSet(FeedThroughStopNestedListAPIView, FeedThroughStopNestedRetrieveAPIView, GenericViewSet):
    pass



class FeedTripNestedMixin(object):
    def get_queryset(self):
        queryset = super(FeedTripNestedMixin, self).get_queryset()
        related_trips = Trip.objects.filter(
            route__feed__pk=self.kwargs['feed_pk'],
            trip_id = self.kwargs['trip_trip_id']
        )
        queryset = queryset.filter(
            trip__in = related_trips
        )
        return queryset

class FeedTripNestedListAPIView( FeedTripNestedMixin, generics.ListAPIView ):
    pass

class FeedTripNestedNestesRetrieveAPIView(FeedTripNestedMixin, generics.RetrieveAPIView):
    pass

class FeedTripNestedViewSet(FeedTripNestedListAPIView, FeedTripNestedNestesRetrieveAPIView, GenericViewSet):
    """
    Base class for viewset nested into stop nested into feed
    """
    pass
