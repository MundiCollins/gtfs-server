from rest_framework.serializers import ModelSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from multigtfs.models import Agency, Route, Stop

class AgencySerializer(ModelSerializer):
    class Meta:
        model = Agency


class RouteSerializer(ModelSerializer):
    class Meta:
        model = Route


class GeoRouteSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Route
        geo_field = "geometry"
        auto_bbox = True


class StopSerializer(ModelSerializer):
    class Meta:
        model = Stop


class GeoStopSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Stop
        geo_field = "geometry"
        auto_bbox = True
