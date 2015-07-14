from django.conf.urls import include, url
#from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from .views import ( FeedViewSet, FeedGeoViewSet, AgencyViewSet, FeedAgencyViewSet,
                    RouteViewSet, GeoRouteViewSet, StopViewSet, GeoStopViewSet, ServiceViewSet,
                    FeedServiceDateViewSet, ServiceServiceDateViewSet,
                    FeedRouteTripViewSet, RouteTripViewSet  )

router = routers.SimpleRouter()
router.register(r'feeds', FeedViewSet)
router.register(r'feeds-info', FeedGeoViewSet)
router.register(r'agencies', AgencyViewSet)

feeds_router = routers.NestedSimpleRouter(router, r'feeds', lookup='feed')

feeds_router.register('agencies', AgencyViewSet)
feeds_router.register('routes.geojson', GeoRouteViewSet)
feeds_router.register('routes', RouteViewSet)
feeds_router.register('stops.geojson', GeoStopViewSet)
feeds_router.register('stops', StopViewSet)
feeds_router.register('services', ServiceViewSet)
feeds_router.register('service_dates', FeedServiceDateViewSet)
feeds_router.register('trips', FeedRouteTripViewSet)


services_router = routers.NestedSimpleRouter(feeds_router, r'services', lookup='service')
services_router.register('service_dates', ServiceServiceDateViewSet)

routes_router = routers.NestedSimpleRouter(feeds_router, r'routes', lookup='route')
routes_router.register('trips', RouteTripViewSet)

urlpatterns = router.urls + feeds_router.urls + services_router.urls + routes_router.urls
