from django.conf.urls import include, url
#from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from .views import ( FeedViewSet, FeedGeoViewSet, AgencyViewSet, FeedAgencyViewSet,
                    RouteViewSet, GeoRouteViewSet, StopViewSet, GeoStopViewSet, ServiceViewSet )

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


urlpatterns = router.urls + feeds_router.urls
