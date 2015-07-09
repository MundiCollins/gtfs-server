from rest_framework.routers import SimpleRouter
from .views import AgencyViewSet, RouteViewSet, GeoRouteViewSet, StopViewSet, GeoStopViewSet

router = SimpleRouter()
router.register('agencies', AgencyViewSet)
router.register('routes.geojson', GeoRouteViewSet)
router.register('routes', RouteViewSet)
router.register('stops.geojson', GeoStopViewSet)
router.register('stops', StopViewSet)

urlpatterns = router.urls
