from rest_framework.routers import SimpleRouter
from .views import AgencyViewSet, RouteViewSet, GeoRouteViewSet, StopViewSet, GeoStopViewSet

router = SimpleRouter()
router.register('agencies', AgencyViewSet)
router.register('routes.geo', GeoRouteViewSet)
router.register('routes', RouteViewSet)
router.register('stops.geo', GeoStopViewSet)
router.register('stops', StopViewSet)

urlpatterns = router.urls
