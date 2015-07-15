from django.conf.urls import include, url
#from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from .views import ( FeedViewSet, FeedGeoViewSet,
                    AgencyViewSet, FeedAgencyViewSet,
                    FeedRouteViewSet, FeedGeoRouteViewSet,
                    FeedStopViewSet, FeedGeoStopViewSet,
                    FeedServiceViewSet,
                    FeedServiceDateViewSet, ServiceServiceDateViewSet,
                    FeedRouteTripViewSet, RouteTripViewSet  )

from .views import StopsNearView, GeoStopsNearView, ServicesActiveView, TripsActiveView

router = routers.SimpleRouter()
router.register(r'feeds', FeedViewSet)
router.register(r'feeds-info', FeedGeoViewSet)
router.register(r'agencies', AgencyViewSet)

feeds_router = routers.NestedSimpleRouter(router, r'feeds', lookup='feed')

feeds_router.register('agencies', FeedAgencyViewSet)
feeds_router.register('routes.geojson', FeedGeoRouteViewSet)
feeds_router.register('routes', FeedRouteViewSet)
feeds_router.register('stops.geojson', FeedGeoStopViewSet)
feeds_router.register('stops', FeedStopViewSet)
feeds_router.register('services', FeedServiceViewSet)
feeds_router.register('service_dates', FeedServiceDateViewSet)
feeds_router.register('trips', FeedRouteTripViewSet)


services_router = routers.NestedSimpleRouter(feeds_router, r'services', lookup='service')
services_router.register('service_dates', ServiceServiceDateViewSet)

routes_router = routers.NestedSimpleRouter(feeds_router, r'routes', lookup='route')
routes_router.register('trips', RouteTripViewSet)


urls = [
    url(u'stops-near/(?P<x>\d+\.\d+)/(?P<y>\d+\.\d+)/$', StopsNearView.as_view(), name="stops-near"),
    url(u'stops-near.geojson/(?P<x>\d+\.\d+)/(?P<y>\d+\.\d+)/$', GeoStopsNearView.as_view(), name="stops-near.geojson"),

    url(u'services-active/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', ServicesActiveView.as_view(), name="services-active"),
    url(u'trips-active/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', TripsActiveView.as_view(), name="services-active"),

]
urlpatterns = router.urls + feeds_router.urls + services_router.urls + routes_router.urls + urls
