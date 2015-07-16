from django.conf.urls import include, url
#from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from .views import (
    FeedViewSet, FeedGeoViewSet, AgencyViewSet, ServiceViewSet, RouteViewSet,
    TripViewSet, StopViewSet, ServiceDateViewSet )
from .nested_views import (
    FeedAgencyViewSet, FeedRouteViewSet, FeedGeoRouteViewSet,
    FeedStopViewSet, FeedGeoStopViewSet,
    FeedServiceViewSet, FeedServiceDateViewSet, ServiceServiceDateViewSet,
    FeedRouteTripViewSet, RouteTripViewSet  )

from .list_views import (
    StopsNearView, FeedStopsNearView, GeoStopsNearView, FeedGeoStopsNearView,
    ServicesActiveView, FeedServiceActiveView,
    TripActiveView, FeedTripActiveView )

router = routers.SimpleRouter()
router.register(r'feeds', FeedViewSet)
router.register(r'feeds-info', FeedGeoViewSet)
router.register(r'agencies', AgencyViewSet)
router.register(r'routes', RouteViewSet)
router.register(r'stops', StopViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'service-dates', ServiceDateViewSet)
router.register(r'trips', TripViewSet)

feeds_router = routers.NestedSimpleRouter(router, r'feeds', lookup='feed')

feeds_router.register('agencies', FeedAgencyViewSet)
feeds_router.register('routes', FeedRouteViewSet)
feeds_router.register('routes.geojson', FeedGeoRouteViewSet)
feeds_router.register('stops', FeedStopViewSet)
feeds_router.register('stops.geojson', FeedGeoStopViewSet)
feeds_router.register('services', FeedServiceViewSet)
feeds_router.register('service-dates', FeedServiceDateViewSet)
feeds_router.register('trips', FeedRouteTripViewSet)


services_router = routers.NestedSimpleRouter(feeds_router, r'services', lookup='service')
services_router.register('service-dates', ServiceServiceDateViewSet)

routes_router = routers.NestedSimpleRouter(feeds_router, r'routes', lookup='route')
routes_router.register('trips', RouteTripViewSet)


urls = [
    url(u'^stops-near/(?P<x>\d+\.\d+)/(?P<y>\d+\.\d+)/$', StopsNearView.as_view(), name="stops-near"),
    url(u'^feeds/(?P<feed_pk>[^/]+)/stops-near/(?P<x>\d+\.\d+)/(?P<y>\d+\.\d+)/$', FeedStopsNearView.as_view(), name="feed-stops-near"),

    url(u'^stops-near.geojson/(?P<x>\d+\.\d+)/(?P<y>\d+\.\d+)/$', GeoStopsNearView.as_view(), name="stops-near.geojson"),
    url(u'^feeds/(?P<feed_pk>[^/]+)/stops-near.geojson/(?P<x>\d+\.\d+)/(?P<y>\d+\.\d+)/$', FeedGeoStopsNearView.as_view(), name="geo-feed-stops-near"),

    url(u'^services-active/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', ServicesActiveView.as_view(), name="services-active"),
    url(u'^feeds/(?P<feed_pk>[^/]+)/services-active/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', FeedServiceActiveView.as_view(), name="feed-services-active"),
    url(u'^trips-active/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', TripActiveView.as_view(), name="services-active"),
    url(u'^feeds/(?P<feed_pk>[^/]+)/trips-active/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', FeedTripActiveView.as_view(), name="feed-trips-active"),

]
urlpatterns = router.urls + feeds_router.urls + services_router.urls + routes_router.urls + urls
