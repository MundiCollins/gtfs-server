from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import (AgencyListView, RouteListView, RouteDetailView, FeedListView, StopListJSONView, ParentStopListJSONView,
                    trip_detail_view, add_stop_ajax, get_route_ajax, update_stop_ajax, delete_stop_ajax,
                    new_route, new_trip, export_feed, update_agency_ajax, update_feed_ajax, update_route_ajax, update_trip_ajax, update_shape_ajax,
                    delete_route_ajax, delete_trip_ajax, delete_feed_ajax, new_feed, confirm_stop_ajax)

urlpatterns = patterns(
    '',
    url(r'gtfs/$', login_required(FeedListView.as_view()), name='feed_list'),
    url(r'gtfs/(?P<feed_id>\d+)/agency/$', login_required(AgencyListView.as_view()), name='agency_list'),
    url(r'gtfs/(?P<feed_id>\d+)/agency/(?P<agency_id>\d+)/route/$', login_required(RouteListView.as_view()), name='route_list'),
    url(r'gtfs/(?P<feed_id>\d+)/agency/(?P<agency_id>\d+)/route/(?P<pk>\d+)/$', login_required(RouteDetailView.as_view()), name='route_detail'),
    url(r'gtfs/(?P<feed_id>\d+)/agency/(?P<agency_id>\d+)/new-route$', login_required(new_route), name='new_route'),

    url(r'gtfs/(?P<feed_id>\d+)/export/$', login_required(export_feed), name='export_feed'),

    url(r'gtfs/(?P<feed_id>\d+)/agency/(?P<agency_id>\d+)/route/(?P<route_id>\d+)/trip/(?P<pk>\d+)/$', login_required(trip_detail_view), name='trip_detail'),
    url(r'gtfs/(?P<feed_id>\d+)/agency/(?P<agency_id>\d+)/route/(?P<route_id>\d+)/new-trip/$', login_required(new_trip), name='new_trip'),

    url(r'gtfs/(?P<feed_id>\d+)/stops.json/', login_required(StopListJSONView.as_view()), name='get_stop_list_ajax'),
    url(r'gtfs/(?P<feed_id>\d+)/parentstops.json/', login_required(ParentStopListJSONView.as_view()), name='get_parent_stop_list_ajax'),

    url(r'gtfs/stop.json/', login_required(add_stop_ajax), name='add_stop_ajax'),
    url(r'gtfs/route.json/', login_required(get_route_ajax), name='get_route_ajax'),

    url(r'gtfs/updatestop.json/', login_required(update_stop_ajax), name='update_stop_ajax'),
    url(r'gtfs/updateroute.json/', login_required(update_route_ajax), name='update_route_ajax'),
    url(r'gtfs/updatetrip.json/', login_required(update_trip_ajax), name='update_trip_ajax'),
    url(r'gtfs/updateshape.json/', login_required(update_shape_ajax), name='update_shape_ajax'),
    url(r'gtfs/updatefeed.json/', login_required(update_feed_ajax), name='update_feed_ajax'),
    url(r'gtfs/updateagency.json/', login_required(update_agency_ajax), name='update_agency_ajax'),

    url(r'gtfs/deletestop.json/', login_required(delete_stop_ajax), name='delete_stop_ajax'),
    url(r'gtfs/deleteroute.json/', login_required(delete_route_ajax), name='delete_route_ajax'),
    url(r'gtfs/deletetrip.json/', login_required(delete_trip_ajax), name='delete_trip_ajax'),
    url(r'gtfs/deletefeed.json/', login_required(delete_feed_ajax), name='delete_feed_ajax'),

    url(r'gtfs/new-feed/$', login_required(new_feed), name='new_feed'),

    url(r'gtfs/confirmstop.json/', login_required(confirm_stop_ajax), name='confirm_stop_ajax'),
)
