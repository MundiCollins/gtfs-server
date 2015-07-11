from rest_framework.serializers import ModelSerializer,SerializerMethodField
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from multigtfs.models import Feed, Agency, Route, Stop


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


class RouteSerializer(ModelSerializer):
    class Meta:
        model = Route
        exclude = ['geometry']


class GeoRouteSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Route
        geo_field = "geometry"
        #auto_bbox = True


class StopSerializer(ModelSerializer):
    class Meta:
        model = Stop
        exclude = ['point']


class GeoStopSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Stop
        geo_field = "point"
        #auto_bbox = True
