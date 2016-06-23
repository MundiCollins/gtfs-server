// This is adapted from the implementation in Project-OSRM
// https://github.com/DennisOSRM/Project-OSRM-Web/blob/master/WebContent/routing/OSRM.RoutingGeometry.js
function decodePolyline(str, precision) {
    var index = 0,
        lat = 0,
        lng = 0,
        coordinates = [],
        shift = 0,
        result = 0,
        byte = null,
        latitude_change,
        longitude_change,
        factor = Math.pow(10, precision || 6);

    // Coordinates have variable length when encoded, so just keep
    // track of whether we've hit the end of the string. In each
    // loop iteration, a single coordinate is decoded.
    while (index < str.length) {

        // Reset shift, result, and byte
        byte = null;
        shift = 0;
        result = 0;

        do {
            byte = str.charCodeAt(index++) - 63;
            result |= (byte & 0x1f) << shift;
            shift += 5;
        } while (byte >= 0x20);

        latitude_change = ((result & 1) ? ~(result >> 1) : (result >> 1));

        shift = result = 0;

        do {
            byte = str.charCodeAt(index++) - 63;
            result |= (byte & 0x1f) << shift;
            shift += 5;
        } while (byte >= 0x20);

        longitude_change = ((result & 1) ? ~(result >> 1) : (result >> 1));

        lat += latitude_change;
        lng += longitude_change;

        coordinates.push([lat / factor, lng / factor]);
    }

    return coordinates;
}


function chunkArray(waypoints, groupSize) {
    return _.chunk(waypoints, groupSize);
}

function generateRoute(routing_server_url, waypoints) {
    var wps = $.map(waypoints, function (waypoint) {
        return {lat: waypoint.lat, lon: waypoint.lon, name: waypoint.name, type: waypoint.type}
    });
    var groups = chunkArray(wps, 50);
    var promises = $.map(groups, function (group) {
        var json = {
            locations: group,
            costing: 'bus',
        }

        var data = {
            json: JSON.stringify(json),
            api_key: 'valhalla-SdWQH9o'
        }
        return $.get(routing_server_url, data);
    });

    var route = [];
    $.when.apply($, promises).then(function () {
        //response format [data, textStatus, jqXHR]
        if (promises.length == 1) {
            arguments = [arguments]
        }

        for (var i = 0; i < arguments.length; i++) {
            var json = JSON.parse(arguments[i][0]);
            route = route.concat(decodePolyline(json.trip.legs[0].shape));
        }
        var polyline = L.polyline(route, {
            color: 'red',
            weight: 5,
            opacity: 0.5,
            smoothFactor: 1
        });
        $(document).trigger('routeGenerated', {route: polyline, waypoints: waypoints});

    }).fail(function (jqXHR, status, error) {
        $(document).trigger('error', {message: 'Failed due to: ' + status + " " + error})
    });
}


function getMarkersFromWaypoints(waypoints) {
    return $.map(waypoints, function (waypoint, index) {
        var markerLocation = new L.LatLng(waypoint.lat, waypoint.lon);
        var marker = new L.Marker(markerLocation, {title: waypoint.name, draggable: true, index: index, icon: waypoint.icon});
        marker.on('dragend', function (e) {
            $(document).trigger('markerDragEnd', {index: e.target.options.index, marker: e.target});
        });
        return marker;
    });
}

function plotMarkers(markers, map) {
    $.map(markers, function (marker) {
        marker.addTo(map);
    });
}

function updateStop(url, data) {
    var jqxhr = $.post(url, data, function (stop) {
        $(document).trigger('success', {message: "Successfully updated " + stop.name + " location"})
    }, 'json');

    jqxhr.fail(function (jqXHR, status, error) {
        $(document).trigger('error', {message: 'Failed due to: ' + status + " " + error})
    });
}

function fetch_and_populate_stops(url, params, list_element) {
    var wkt = new Wkt.Wkt();
    var request = $.ajax({
        url: url,
        method: 'GET',
        data: params,
        dataType: 'json'
    });

    request.done(function (result) {
        var stops_list = $(list_element);
        stops_list.html('');
        var source = $("#add-stop-item-template").html();
        var template = Handlebars.compile(source);
        var option = $('<option>');

        option.html('--');
        option.attr('value', '');

        stops_list.append(option);
        $.each(result, function (idx, item) {
            var point = wkt.read(item.fields.point.replace(/SRID=4326;/g, ''));
            var context = {
                text: item.fields.name,
                value: item.pk,
                lat: point.components[0].y,
                lon: point.components[0].x
            }
            stops_list.append(template(context));
        });
        $(document).trigger('success', {message: 'Successfully fethed stops'})

    });

    request.fail(function (jqXHR, textStatus, error) {
        $(document).trigger('error', {message: 'Failed due to: ' + status + " " + error})
    });
}

function add_stop(url, params) {
    var request = $.ajax({
        url: url,
        method: 'POST',
        data: params,
        dataType: 'json'
    });

    request.done(function (result) {
        $(document).trigger('addStop', {stop: result});
        $('#stop-modal').modal('hide');
        $(document).trigger('success', {message: "Successfully added " + result.name})
    });

    request.fail(function (jqXHR, textStatus, error) {
        $(document).trigger('error', {message: 'Failed due to: ' + status + " " + error})
    });
}

function delete_stop(url, params){
    var request = $.ajax({
        url: url,
        method: 'POST',
        data: params,
    });

    request.done(function (result) {
        $(document).trigger('success', {message: result});
    });

    request.fail(function (jqXHR, textStatus, error) {
        $(document).trigger('error', {message: jqXHR.responseText});
    });
}

function delete_route(url, params){
    var request = $.ajax({
        url: url,
        method: 'POST',
        data: params,
    });

    request.done(function (result) {
        $(document).trigger('success', {message: result});
    });

    request.fail(function (jqXHR, textStatus, error) {
        $(document).trigger('error', {message: jqXHR.responseText});
    });
}

function delete_trip(url, params){
    var request = $.ajax({
        url: url,
        method: 'POST',
        data: params,
    });

    request.done(function (result) {
        console.log(result);
        $(document).trigger('success', {message: result});
    });

    request.fail(function (jqXHR, textStatus, error) {
        $(document).trigger('error', {message: jqXHR.responseText});
    });
}


function refreshWaypoints(waypoints) {
    return $.map(waypoints, function (waypoint, index) {
        if (index == 0 || index == waypoint.length) {
            waypoint.type = 'break';
        } else {
            waypoint.type = 'through';
        }
        return waypoint;
    });
}

function insertWaypoint(map, newWaypoint, waypoints) {
    var points = $.map(waypoints, function (waypoint) {
        return L.latLng(waypoint.lat, waypoint.lon);
    });

    var new_point = L.latLng(newWaypoint.lat,newWaypoint.lon);
    var closest = L.GeometryUtil.closest(map, points, new_point, true);
    var insert_after = false;

    for (var index = 0; index < points.length; index++) {
        var cur = L.latLng(points[index].lat, points[index].lng);
        if ((cur.lat == closest.lat) && (cur.lng == closest.lng)) {
            var angle = L.GeometryUtil.computeAngle(map.latLngToLayerPoint(closest), map.latLngToLayerPoint(new_point));
            if (angle >= 90 && angle <= 270) {
                insert_after = true;
            }
            break;
        }
    }

    // Get the corresponding stop on the list
    var anchorElement = $('#current-stops form > ul').children().eq(index);

    // Insert stop at correct location in the current stops list
    var source = $("#add-current-stop-item-template").html();
    var template = Handlebars.compile(source);
    var context = {
        name: newWaypoint.name,
        id: newWaypoint.id,
    }

    if (insert_after) {
        waypoints.splice(index + 1, 0, newWaypoint);
        anchorElement.after(template(context))
    } else {
        waypoints.splice(index, 0, newWaypoint);
        anchorElement.before(template(context))
    }

    // Refresh editable binding???
    //HACK

    $('.editable').editable({
        params: function (params) {
            //originally params contain pk, name and value
            params.csrfmiddlewaretoken = '{{ csrf_token }}';
            return params;
        }
    });
    return refreshWaypoints(waypoints);
}
