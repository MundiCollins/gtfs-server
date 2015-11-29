from rest_framework.serializers import ModelSerializer,SerializerMethodField, FloatField
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from multigtfs.models import Feed, Agency, Route, Stop, Service, ServiceDate, Trip, StopTime
from rest_framework.serializers import CharField

from django.contrib.gis.db.models.aggregates import Extent

class FeedSerializer(ModelSerializer):
    class Meta:
        model = Feed

class FeedInfoSerializer(ModelSerializer):
    feed_extent = SerializerMethodField()

    def get_feed_extent(self, obj):
        p = Route.objects.in_feed(obj).aggregate(Extent('geometry'))
        return p['geometry__extent']

    class Meta:
        model = Feed


class AgencySerializer(ModelSerializer):
    class Meta:
        model = Agency


class TripSerializer(ModelSerializer):
    class Meta:
        model = Trip
        exclude = ['geometry']

class RouteSerializer(ModelSerializer):
    @classmethod
    def setup_eager_loading(cls, queryset):
        queryset = queryset.select_related('feed')
        return queryset

    class Meta:
        model = Route
        exclude = ['geometry']

class RouteWithTripsSerializer(RouteSerializer):
    trips = TripSerializer(many=True, read_only=True)

    @classmethod
    def setup_eager_loading(cls, queryset):
        queryset = super(RouteWithTripsSerializer, self).setup_eager_loading(queryset)
        queryset = queryset.prefetch_related('trips')
        return queryset


class GeoRouteSerializer(GeoFeatureModelSerializer):
    
    class Meta:
        model = Route
        geo_field = "geometry"
        #auto_bbox = True



class StopSerializer(ModelSerializer):
    
    @classmethod
    def setup_eager_loading(cls, queryset):
        queryset = queryset.select_related('feed')
        return queryset

    class Meta:
        model = Stop
        exclude = ['point']


class GeoStopSerializer(GeoFeatureModelSerializer):
    
    @classmethod
    def setup_eager_loading(cls, queryset):
        queryset = queryset.select_related('feed')
        return queryset

    class Meta:
        model = Stop
        geo_field = "point"
        #auto_bbox = True


class StopSerializerWithDistance(StopSerializer):
    distance = SerializerMethodField(required=False, read_only=True)
    def get_distance(self, obj):
        if not obj.distance:
            return None
        return float(obj.distance.km)

from rest_framework.serializers import ListField
class StopWithTripsAndRoutesSerializer(StopSerializer):
    pass
    #trips = ListField(source="tr")


class GeoStopSerializerWithDistance(GeoStopSerializer):
    distance = SerializerMethodField(required=False, read_only=True)
    def get_distance(self, obj):
        if not obj.distance:
            return None
        return float(obj.distance.km)

class ServiceDateSerializer(ModelSerializer):
    class Meta:
        model = ServiceDate


class ServiceSerializer(ModelSerializer):
    #service_dates = ServiceDateSerializer(many=True, read_only=True)

    @classmethod
    def setup_eager_loading(cls, queryset):
        queryset = queryset.select_related('feed')
        return queryset

    class Meta:
        model = Service

class ServiceWithDatesSerializer(ServiceSerializer):
    service_dates = ServiceDateSerializer(many=True, read_only=True)

class StopTimeSerializer(ModelSerializer):
    trip_id = SerializerMethodField(read_only=True)
    stop_id = SerializerMethodField(read_only=True)
    route_id = SerializerMethodField(read_only=True)
    route = SerializerMethodField(read_only=True)

    @classmethod
    def setup_eager_loading(cls, queryset):
        queryset = queryset.select_related('trip', 'stop', 'trip__route')
        return queryset

    def get_trip_id(self, obj):
        return obj.trip.trip_id

    def get_stop_id(self, obj):
        return obj.stop.stop_id

    def get_route(self, obj):
        return obj.trip.route.id

    def get_route_id(self, obj):
        return obj.trip.route.route_id

    class Meta:
        model = StopTime
