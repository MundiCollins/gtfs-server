import json
import random

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.filters import DjangoFilterBackend

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.views import APIView

from django.db import transaction
from django.contrib.gis import geos
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from stronghold.decorators import public

from multigtfs.models import Agency, Route, Stop, Feed, Service, ServiceDate, Trip, StopTime, Ride, NewStop, NewRoute, NewFare, Shape, ShapePoint
from .serializers import (
    AgencySerializer,
    GeoRouteSerializer, RouteSerializer, RouteWithTripsSerializer,
    GeoStopSerializer, StopSerializer, StopSerializerWithDistance,
    GeoStopSerializerWithDistance,
    FeedSerializer,
    FeedInfoSerializer, ServiceSerializer, ServiceWithDatesSerializer,
    ServiceDateSerializer,
    TripSerializer,
    StopTimeSerializer )



class FeedViewSet(ReadOnlyModelViewSet):
    """
    Viewset for Feed model
    """
    serializer_class = FeedSerializer
    queryset = Feed.objects.all()


class FeedGeoViewSet(FeedViewSet):
    """
    Viewset for Feed model - extended info (changes serializer)
    """
    serializer_class = FeedInfoSerializer


class AgencyViewSet(ReadOnlyModelViewSet):
    """
    Viewset for Agency (global)
    """
    serializer_class = AgencySerializer
    queryset = Agency.objects.all()


class ServiceViewSet(ReadOnlyModelViewSet):
    """
    Viewset for Service (global)
    """
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()


class RouteViewSet(ReadOnlyModelViewSet):
    """
    Viewset for Route (global)
    """
    serializer_class = RouteSerializer
    queryset = Route.objects.all()


class StopViewSet(ReadOnlyModelViewSet):
    """
    Viewset for Stop (global)
    """
    serializer_class = StopSerializer
    queryset = Stop.objects.all()


class TripViewSet(ReadOnlyModelViewSet):
    """
    Viewset for Trip (global)
    """
    serializer_class = TripSerializer
    queryset = Trip.objects.all()


class ServiceDateViewSet(ReadOnlyModelViewSet):
    """
    Viewset for ServiceDate (global)
    """
    serializer_class = ServiceDateSerializer
    queryset = ServiceDate.objects.all()


class StopTimeViewSet(ReadOnlyModelViewSet):
    """
    Viewset for StopTime (global)
    """
    serializer_class = StopTimeSerializer
    queryset = StopTime.objects.all()


class NewRouteView(APIView):
    @csrf_exempt
    @method_decorator(public)
    def post(self, request):
        try:
            json_data = json.loads(request.body)
            data = json_data['data']
            agency_id = Agency.objects.filter(agency_id='UON').first().id  # hard-coded for digital matatus
            feed_id = Feed.objects.filter(name='Digital Matatus').first().id  # hard-coded for digital matatus data

            # create a new route
            request_params = data['new_route_details']

            # prepend zeros to the route number
            request_params['route_number'] = request_params['route_number'].zfill(4)

            route_mask = "{corridor}{first_level_branch}{second_level_branch}{route_number}{gazetted}{inbound}"
            params = {
                'route_id': route_mask.format(**request_params),
                'short_name': request_params.get('route_number'),
                'desc': request_params.get('description'),
                'rtype': "3",  # hard-coded for bus type
                'agency_id': agency_id,
                'feed_id': feed_id
            }

            route = Route(**params)
            route.save()
            route.refresh_from_db()

            options = dict()
            for i in range(1, 10):
                options[i] = i

            # Create route + shape
            context = dict()
            context['route_id'] = route.id
            context['route_name'] = route.short_name
            context['headsign_options'] = route.desc.split('-')
            context['origins'] = options
            context['route_variations'] = options

            return Response({"success": True, "result": context})
        except Exception as e:
            return Response({"success": False, "result": e})


class RideView(APIView):
    authentication_classes = []
    permission_classes = []

    @csrf_exempt
    @method_decorator(public)
    def post(self, request):
        json_data = json.loads(request.body)

        for data in json_data['data']:
            if data['new_route'] == 'true':
                # create a new trip

                feed_id = Feed.objects.filter(name='Digital Matatus').first().id  # hard-coded for digital matatus data
                request_params = data['new_trip_details']

                # Trip variables
                headsign = request_params['headsign']
                service_id = "1"  # hard-coded:
                origin = request_params['origin']
                route_variation = request_params['route_variation']
                direction = int(data['inbound']),
                route_id = int(data['route_id'])
                route = Route.objects.get(id=route_id)

                # corridor + 4 characters for the route number
                corridor = route.route_id[0]
                route_number = route.route_id[5:9]

                shape_id = "{}{}{}{}{}".format(corridor, route_number, origin, route_variation, direction)

                trip_id = shape_id
                with transaction.atomic():
                    # Create new shape
                    shape = Shape(
                        feed_id=feed_id,
                        shape_id=shape_id)
                    shape.save()

                    trip = Trip(
                        trip_id=trip_id,
                        headsign=headsign,
                        service_id=service_id,
                        direction=direction,
                        route_id=route_id,
                        shape_id=shape.id
                    )
                    trip.save()

                    # Create shape points from the uploaded shape files
                    # shape_file = shapefile.Reader(shp=request.FILES['shape-file'], dbf=request.FILES['shape-file-dbf'])
                    # shapes = shape_file.shapes()

                    sequence_start = 2001
                    shape_key = 0

                    for i in data['route']:
                        shape_point = ShapePoint(
                            point='POINT ({} {})'.format(i['longitude'], i['latitude']),
                            shape_id=shape.id,
                            sequence=sequence_start + shape_key
                        )
                        shape_point.save()
                        shape_key += 1

                    shape.update_geometry()

                    start_seconds = 6 * 3600  # First trip is at 6am
                    delta = 5 * 60  # % minutes
                    stop_sequence = 0

                    for row in data['stops']:
                        tmp = list(row['stop_name'].upper().replace(' ', ''))
                        random.shuffle(tmp)
                        stop_suffix = "".join(tmp[:3])  # pick 3 characters from the shuffled stop name

                        stop, created = Stop.objects.get_or_create(
                            point=geos.fromstr('POINT({} {})'.format(row['longitude'], row['latitude'])),
                            feed_id=feed_id,
                            defaults={
                                'stop_id': '{}{}{}{}'.format(corridor.zfill(2), row['designation'] or 0, direction,
                                                             stop_suffix),
                                'name': row['stop_name']
                            }
                        )

                        trip.stoptime_set.add(StopTime(
                            stop_id=stop.id,
                            trip_id=trip.id,
                            stop_sequence=stop_sequence + 1,
                            arrival_time=start_seconds,
                            departure_time=start_seconds
                        ))
                        start_seconds += delta

                    trip.save()
                    trip.update_geometry()
                    trip.refresh_from_db()

            else:
                route_id = int(data['route_id'])
                route_name = data['route_name']
                routes = data['route']
                stops = data['stops']

                ride = Ride(route=Route.objects.get(id=route_id),
                            new_route=data['new_route'],
                            route_name=route_name,
                            direction='inbound' if data['inbound'] == '1' else 'outbound',
                            route_description=data['description'],
                            notes=data['notes'],
                            vehicle_capacity=data['vehicle_capacity'],
                            vehicle_type=data['vehicle_type'],
                            vehicle_full=data['vehicle_full'],
                            start_time=data['start_time'],
                            duration=data['trip_duration'],
                            surveyor_name=data['surveyor_name'])
                ride.save()
                ride_id = ride.id

                for i in routes:
                    route = NewRoute(ride=Ride.objects.get(id=ride_id), latitude=i['latitude'], longitude=i['longitude'],
                                     time=i['time'])
                    route.save()

                for i in stops:
                    latitude = i['latitude']
                    longitude = i['longitude']
                    arrival_time = i['arrival_time']
                    departure_time = i['departure_time']
                    stop_name = i['stop_name']
                    stop_designation = i['stop_designation']
                    new_stop = NewStop(ride=Ride.objects.get(id=ride_id), latitude=latitude, longitude=longitude,
                                       arrival_time=arrival_time, departure_time=departure_time, stop_name=stop_name,
                                       stop_designation=stop_designation)
                    new_stop.save()

        return Response({"success": True})


class FareView(APIView):
    authentication_classes = []
    permission_classes = []

    @csrf_exempt
    @method_decorator(public)
    def post(self, request):
        json_data = json.loads(request.body)

        fare = NewFare()
        fare.stop_to = json_data['stop_to']
        fare.stop_from = json_data['stop_from']
        fare.amount = json_data['amount']
        fare.stop_from_id = json_data['stop_from_id']
        fare.route_id = json_data['route_id']
        fare.stop_to_id = json_data['stop_to_id']
        fare.weather = json_data['weather']
        fare.traffic_jam = json_data['traffic_jam']
        fare.demand = json_data['demand']
        fare.air_quality = json_data['air_quality']
        fare.peak = json_data['peak']
        fare.travel_time = json_data['travel_time']
        fare.crowd = json_data['crowd']
        fare.safety = json_data['safety']
        fare.drive_safety = json_data['drive_safety']
        fare.music = json_data['music']
        fare.internet = json_data['internet']
        fare.save()

        return Response({"success": True})
