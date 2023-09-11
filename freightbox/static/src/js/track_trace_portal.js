odoo.define('freightbox.track_trace_portal', function (require) {
    'use strict';
    var rpc = require('web.rpc');
    var map = false

    console.log("TRACK TRACE PORTAL JS CALL")

    mapboxgl.accessToken = 'pk.eyJ1IjoiYWpheS1wb3dlcnBib3giLCJhIjoiY2xjOG9reHk5M2s0ejN2cGp0dWxhYXJjZSJ9.3JGZaTYDaZlfOWcv1J-wbw';
    map = new mapboxgl.Map({
    container: 'tnt_map',
    style: 'mapbox://styles/mapbox/streets-v12',
    center: [76.9921, 18.8127],
    zoom: 3
    });


    $(document).on('click', '#track_map_btn', function(){

        map.remove();

        mapboxgl.accessToken = 'pk.eyJ1IjoiYWpheS1wb3dlcnBib3giLCJhIjoiY2xjOG9reHk5M2s0ejN2cGp0dWxhYXJjZSJ9.3JGZaTYDaZlfOWcv1J-wbw';
        map = new mapboxgl.Map({
            container: 'tnt_map',
            style: 'mapbox://styles/mapbox/streets-v12',
            center: [76.9921, 18.8127],
            zoom: 3
        });

        var tnt_divs = document.getElementsByClassName('si-track');

        for (var i=0; i<tnt_divs.length; i++) {
            if (tnt_divs[i].id == this.name+'_tnt') {
                tnt_divs[i].style.display = 'block';
            }
            else{
                tnt_divs[i].style.display = 'none';
            }
        }

        rpc.query({
            model: 'transport',
            method: 'get_container_track_details',
            args: [null, this.name],
        }).then(function (result) {
            console.log("METHOD CALL SUCCESSFUL !!");
            console.log(">> Route : ", result['route']);

            var map_markers_list = result['map_markers_list'];
            console.log(">> map_markers_list : ", map_markers_list);
            for (var i=0; i<map_markers_list.length; i++) {
                var marker_lat = 0;
                var marker_lon = 0;
                try {
                    marker_lat = map_markers_list[i]['lat'];
                }
                catch {
                    marker_lat = 0;
                }
                try {
                    marker_lon = map_markers_list[i]['lon'];
                }
                catch {
                    marker_lon = 0;
                }

                if (i == 0 ) {
                    if (marker_lat != 0 && marker_lon != 0) {
                        new mapboxgl.Marker()
                        .setLngLat([marker_lon, marker_lat])
                        .addTo(map);
                    }
                }
                else if (i == (map_markers_list.length-1)) {
                    if (marker_lat != 0 && marker_lon != 0) {
                        new mapboxgl.Marker({ color: 'black', rotation: 45 })
                        .setLngLat([marker_lon, marker_lat])
                        .addTo(map);
                    }
                }
                else {
                    if (marker_lat != 0 && marker_lon != 0) {
                        new mapboxgl.Marker({ color: 'grey', rotation: 25 })
                        .setLngLat([marker_lon, marker_lat])
                        .addTo(map);
                    }
                }

            }

//            if (por_lat != 0 && por_lon != 0) {
//                const marker1 = new mapboxgl.Marker()
//                .setLngLat([por_lon, por_lat])
//                .addTo(map);
//                }
//
//            if (pod_lat != 0 && pod_lon != 0) {
//                const marker2 = new mapboxgl.Marker({ color: 'black', rotation: 45 })
//                .setLngLat([pod_lon, pod_lat])
//                .addTo(map);
//                }
            console.log(">>> BEFORE LOAD ")
            var lines_created = false;
            map.on('load', () => {
                console.log(">>> inside load <<< ")
                if (result['route'].length > 0) {
                    for (var i=0; i<result['route'].length; i++) {
                        console.log(">>>>>>> INDEX : ", i)
                        var key = Object.keys(result['route'][i])[0];
                        var route_list = result['route'][i][key];

                        console.log(">>> KEY : ",key)
                        console.log(">>> VALUE : ",route_list)
                        var coordinates = [];
                        for (var j=0; j<route_list.length; j++) {
                            coordinates.push([Number(route_list[j]['lon']), Number(route_list[j]['lat'])])
                        }
                        console.log(">>> COORDINATES : ",coordinates)
                        var source_id = "src_"+i;
                        var layer_id = "lyr_"+i;
                        if (map.getLayer(layer_id)) {
                          map.removeLayer(layer_id);
                        }

                        if (map.getSource(source_id)) {
                          map.removeSource(source_id);
                        }
                        var line_color = 'grey';
                        if (key == 'road') {
                            line_color = 'blue';
                        }
                        if (key == 'rail') {
                            line_color = 'black';
                        }
                        if (key == 'ship') {
                            line_color = 'yellow';
                        }

                        var lines = [{
                            type: "Feature",
                            geometry: {
                                type: "LineString",
                                coordinates: coordinates
                            }
                        }];

                        map.addSource(source_id, {
                            type: "geojson",
                            data: {
                                type: "FeatureCollection",
                                features: lines
                            }
                        });
                        map.addLayer({
                            id: layer_id,
                            type: "line",
                            source: source_id,
                            layout: {
                                "line-join": "round",
                                "line-cap": "round"
                            },
                            paint: {
                                "line-color": line_color,
                                "line-width": 2,
                                "line-opacity": 1
                            }
                        });
                    }
                }
                lines_created = true;
            });
            if (lines_created == false) {
                if (result['route'].length > 0) {
                    for (var i=0; i<result['route'].length; i++) {
                        console.log(">>>>>>> INDEX : ", i)
                        var key = Object.keys(result['route'][i])[0];
                        var route_list = result['route'][i][key];

                        console.log(">>> KEY : ",key)
                        console.log(">>> VALUE : ",route_list)
                        var coordinates = [];
                        for (var j=0; j<route_list.length; j++) {
                            coordinates.push([Number(route_list[j]['lon']), Number(route_list[j]['lat'])])
                        }
                        console.log(">>> COORDINATES : ",coordinates)
                        var source_id = "src_"+i;
                        var layer_id = "lyr_"+i;
                        if (map.getLayer(layer_id)) {
                          map.removeLayer(layer_id);
                        }

                        if (map.getSource(source_id)) {
                          map.removeSource(source_id);
                        }
                        var line_color = 'grey';
                        if (key == 'road') {
                            line_color = 'blue';
                        }
                        if (key == 'rail') {
                            line_color = 'black';
                        }
                        if (key == 'ship') {
                            line_color = 'yellow';
                        }
                        var lines = [{
                            type: "Feature",
                            geometry: {
                                type: "LineString",
                                coordinates: coordinates
                            }
                        }];
                        map.addSource(source_id, {
                            type: "geojson",
                            data: {
                                type: "FeatureCollection",
                                features: lines
                            }
                        });
                        map.addLayer({
                            id: layer_id,
                            type: "line",
                            source: source_id,
                            layout: {
                                "line-join": "round",
                                "line-cap": "round"
                            },
                            paint: {
                                "line-color": line_color,
                                "line-width": 2,
                                "line-opacity": 1
                            }
                        });
                    }
                }
            }
            console.log(">>> AFTER LOAD ")
        });
    });
 });
