from django.conf.urls import include, url
#from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from django.views.decorators.csrf import csrf_exempt
from stronghold.decorators import public

from .views import (
    FeedViewSet, FeedGeoViewSet, AgencyViewSet, ServiceViewSet, RouteViewSet,
    TripViewSet, StopViewSet, ServiceDateViewSet, StopTimeViewSet, RideView)
from .nested_views import (
    FeedAgencyViewSet, FeedRouteViewSet, FeedGeoRouteViewSet,
    FeedStopViewSet, FeedGeoStopViewSet,
    FeedServiceViewSet, FeedServiceDateViewSet, ServiceServiceDateViewSet,
    FeedRouteTripViewSet, RouteTripViewSet,
    FeedStopTimeViewSet, FeedStopStopTimeViewSet, FeedTripStopTimeViewSet  )

from .list_views import (
    StopsNearView, FeedStopsNearView, GeoStopsNearView, FeedGeoStopsNearView,
    ServicesActiveView, FeedServiceActiveView,
    TripActiveView, FeedTripActiveView, StopsActiveView,
    FeedStopActiveView,
    FeedStopTimesActiveView, FeedStopStopTimesActiveView ,
    TrajectoriesView )

router = routers.SimpleRouter()
router.register(r'feeds', FeedViewSet)
router.register(r'feeds-info', FeedGeoViewSet)
router.register(r'agencies', AgencyViewSet)
router.register(r'routes', RouteViewSet)
router.register(r'stops', StopViewSet)
router.register(r'stop-times', StopTimeViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'service-dates', ServiceDateViewSet)
router.register(r'trips', TripViewSet)
router.register(r'ride', csrf_exempt(RideView), base_name='ride')

feeds_router = routers.NestedSimpleRouter(router, r'feeds', lookup='feed')

feeds_router.register('agencies', FeedAgencyViewSet)
feeds_router.register('routes', FeedRouteViewSet)
feeds_router.register('routes.geojson', FeedGeoRouteViewSet)
feeds_router.register('stops', FeedStopViewSet)
feeds_router.register('stops.geojson', FeedGeoStopViewSet)
feeds_router.register('stop-times', FeedStopTimeViewSet)
feeds_router.register('services', FeedServiceViewSet)
feeds_router.register('service-dates', FeedServiceDateViewSet)
feeds_router.register('trips', FeedRouteTripViewSet)


services_router = routers.NestedSimpleRouter(feeds_router, r'services', lookup='service')
services_router.register('service-dates', ServiceServiceDateViewSet)

routes_router = routers.NestedSimpleRouter(feeds_router, r'routes', lookup='route')
routes_router.register('trips', RouteTripViewSet)

stops_router = routers.NestedSimpleRouter(feeds_router, r'stops', lookup='stop')
stops_router.register('stop-times', FeedStopStopTimeViewSet)

trips_router = routers.NestedSimpleRouter(feeds_router, r'trips', lookup='trip')
trips_router.register('stop-times', FeedTripStopTimeViewSet)



urls = [
    url(u'^stops-near/(?P<x>\d+\.\d+)/(?P<y>\d+\.\d+)/$', StopsNearView.as_view(), name="stops-near"),
    url(u'^feeds/(?P<feed_pk>[^/]+)/stops-near/(?P<x>\d+\.\d+)/(?P<y>\d+\.\d+)/$', FeedStopsNearView.as_view(), name="feed-stops-near"),

    url(u'^stops-near.geojson/(?P<x>\d+\.\d+)/(?P<y>\d+\.\d+)/$', GeoStopsNearView.as_view(), name="stops-near.geojson"),
    url(u'^feeds/(?P<feed_pk>[^/]+)/stops-near.geojson/(?P<x>\d+\.\d+)/(?P<y>\d+\.\d+)/$', FeedGeoStopsNearView.as_view(), name="geo-feed-stops-near"),

    url(u'^services-active/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', ServicesActiveView.as_view(), name="services-active"),
    url(u'^services-active-today/$', ServicesActiveView.as_view(), name="services-active-today"),
    url(u'^feeds/(?P<feed_pk>[^/]+)/services-active/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', FeedServiceActiveView.as_view(), name="feed-services-active"),
    url(u'^feeds/(?P<feed_pk>[^/]+)/services-active-today/$', FeedServiceActiveView.as_view(), name="feed-services-active-today"),

    url(u'^trips-active/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', TripActiveView.as_view(), name="trips-active"),
    url(u'^trips-active-today/$', TripActiveView.as_view(), name="trips-active-today"),
    url(u'^feeds/(?P<feed_pk>[^/]+)/trips-active/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', FeedTripActiveView.as_view(), name="feed-trips-active"),
    url(u'^feeds/(?P<feed_pk>[^/]+)/trips-active-today/$', FeedTripActiveView.as_view(), name="feed-trips-active-today"),

    url(u'^stops-active/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', StopsActiveView.as_view(), name="stops-active"),
    url(u'^stops-active-today/$', StopsActiveView.as_view(), name="stops-active-today"),
    url(u'^feeds/(?P<feed_pk>[^/]+)/stops-active/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', FeedStopActiveView.as_view(), name="feed-stop-active"),
    url(u'^feeds/(?P<feed_pk>[^/]+)/stops-active-today/$', FeedStopActiveView.as_view(), name="feed-stop-active-today"),

    #url(u'^stop-times-active/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', StopTimesActiveView.as_view(), name="stop-times-active"),
    #url(u'^stop-times-active-today/$', StopTimesActiveView.as_view(), name="stop-times-active-today"),

    url(u'^feeds/(?P<feed_pk>[^/]+)/stops/(?P<stop_stop_id>[^/]+)/stop-times-active/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', FeedStopStopTimesActiveView.as_view(), name="feed-stop-stop-times-active"),
    url(u'^feeds/(?P<feed_pk>[^/]+)/stops/(?P<stop_stop_id>[^/]+)/stop-times-active-today/$', FeedStopStopTimesActiveView.as_view(), name="feed-stop-stop-times-active-today"),

    url(u'^feeds/(?P<feed_pk>[^/]+)/stop-times-active/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', FeedStopTimesActiveView.as_view(), name="feed-stop-times-active"),
    url(u'^feeds/(?P<feed_pk>[^/]+)/stop-times-active-today/$', FeedStopTimesActiveView.as_view(), name="feed-stop-times-active-today"),

    url(u'^feeds/(?P<feed_pk>[^/]+)/trajectories/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}):(?P<hour>\d+)/(?P<bbox>[^/]+)/$', TrajectoriesView.as_view(), name="trajectories"),
    url(u'^feeds/(?P<feed_pk>[^/]+)/trajectories-today/(?P<hour>\d+)/(?P<bbox>[^/]+)/$', TrajectoriesView.as_view(), name="trajectories"),
    url(u'^feeds/(?P<feed_pk>[^/]+)/trajectories-now/(?P<bbox>[^/]+)/$', TrajectoriesView.as_view(), name="trajectories"),

    url(u'^ride/', csrf_exempt(RideView.as_view()), name="ride"),

]
urlpatterns = router.urls + feeds_router.urls + services_router.urls + routes_router.urls + stops_router.urls +  trips_router.urls + urls
