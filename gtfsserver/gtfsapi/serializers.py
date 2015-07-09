from rest_framework.serializers import ModelSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from multigtfs.models import Feed, Agency, Route, Stop


class FeedSerializer(ModelSerializer):
    class Meta:
        model = Feed

class AgencySerializer(ModelSerializer):
    class Meta:
        model = Agency


class RouteSerializer(ModelSerializer):
    class Meta:
        model = Route
        excluded_fields = ['geometry']


class GeoRouteSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Route
        geo_field = "geometry"
        #auto_bbox = True


class StopSerializer(ModelSerializer):
    class Meta:
        model = Stop
        excluded_fields = ['point']


class GeoStopSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Stop
        geo_field = "point"
        #auto_bbox = True
