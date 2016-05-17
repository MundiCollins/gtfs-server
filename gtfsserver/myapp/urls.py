from django.conf.urls import patterns, url

from .views import (AgencyListView, RouteListView, RouteDetailView, FeedListView, StopListJSONView,
                    trip_detail_view, add_stop_ajax, get_route_ajax, update_stop_ajax, delete_stop_ajax,
                    new_route, new_trip, export_feed, update_route_ajax)

urlpatterns = patterns(
    '',
    url(r'gtfs/$', FeedListView.as_view(), name='feed_list'),
    url(r'gtfs/(?P<feed_id>\d+)/agency/$', AgencyListView.as_view(), name='agency_list'),
    url(r'gtfs/(?P<feed_id>\d+)/agency/(?P<agency_id>\d+)/route/$', RouteListView.as_view(), name='route_list'),
    url(r'gtfs/(?P<feed_id>\d+)/agency/(?P<agency_id>\d+)/route/(?P<pk>\d+)/$', RouteDetailView.as_view(), name='route_detail'),
    url(r'gtfs/(?P<feed_id>\d+)/agency/(?P<agency_id>\d+)/new-route$', new_route, name='new_route'),

    url(r'gtfs/(?P<feed_id>\d+)/export/$', export_feed, name='export_feed'),

    url(r'gtfs/(?P<feed_id>\d+)/agency/(?P<agency_id>\d+)/route/(?P<route_id>\d+)/trip/(?P<pk>\d+)/$', trip_detail_view, name='trip_detail'),
    url(r'gtfs/(?P<feed_id>\d+)/agency/(?P<agency_id>\d+)/route/(?P<route_id>\d+)/new-trip/$', new_trip, name='new_trip'),

    url(r'gtfs/stops.json/', StopListJSONView.as_view(), name='get_stop_list_ajax'),
    url(r'gtfs/stop.json/', add_stop_ajax, name='add_stop_ajax'),
    url(r'gtfs/route.json/', get_route_ajax, name='get_route_ajax'),
    url(r'gtfs/updatestop.json/', update_stop_ajax, name='update_stop_ajax'),
    url(r'gtfs/deletestop.json/', delete_stop_ajax, name='delete_stop_ajax'),

    url(r'gtfs/updateroute.json/', update_route_ajax, name='update_route_ajax'),

)
