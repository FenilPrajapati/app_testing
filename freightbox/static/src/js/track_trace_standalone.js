odoo.define('freightbox.track_trace_standalone', function (require) {
'use strict';
    var rpc = require('web.rpc');
    var map = false;

    console.log("TRACK TRACE STANDALONE CONTAINER LIST JS ")

    mapboxgl.accessToken = 'pk.eyJ1IjoiYWpheS1wb3dlcnBib3giLCJhIjoiY2xjOG9reHk5M2s0ejN2cGp0dWxhYXJjZSJ9.3JGZaTYDaZlfOWcv1J-wbw';
    map = new mapboxgl.Map({
        container: 'tnt_standalone_map',
        style: 'mapbox://styles/mapbox/streets-v12',
        center: [76.9921, 18.8127],
        zoom: 3
    });

    $(document).on('click', '#tnt_sa_btn', function(){
        console.log("TRACK TRACE STANDALONE BUTTON CLICK..")
        map.remove();

        mapboxgl.accessToken = 'pk.eyJ1IjoiYWpheS1wb3dlcnBib3giLCJhIjoiY2xjOG9reHk5M2s0ejN2cGp0dWxhYXJjZSJ9.3JGZaTYDaZlfOWcv1J-wbw';
        map = new mapboxgl.Map({
            container: 'tnt_standalone_map',
            style: 'mapbox://styles/mapbox/streets-v12',
            center: [76.9921, 18.8127],
            zoom: 3
        });

//        var location_labels = document.getElementsByClassName('location_label');
        var tnt_divs = document.getElementsByClassName('si-track');
//        var por_lat = false;
//        var por_lon = false;
//        var pod_lat = false;
//        var pod_lon = false;
//        var cur_lat = false;
//        var cur_lon = false;
//
        for (var i=0; i<tnt_divs.length; i++) {
            if (tnt_divs[i].id == this.name+'_tnt') {
                tnt_divs[i].style.display = 'block';
            }
            else{
                tnt_divs[i].style.display = 'none';
            }
        }
//
//         for (var i=0; i<location_labels.length; i++) {
//                if (location_labels[i].name == this.name+'_por_lat') {
//                    por_lat = location_labels[i].value;
//                }
//                if (location_labels[i].name == this.name+'_por_lon') {
//                    por_lon = location_labels[i].value;
//                }
//                if (location_labels[i].name == this.name+'_pod_lat') {
//                    pod_lat = location_labels[i].value;
//                }
//                if (location_labels[i].name == this.name+'_pod_lon') {
//                    pod_lon = location_labels[i].value;
//                }
//                if (location_labels[i].name == this.name+'_cur_lat') {
//                    cur_lat = location_labels[i].value;
//                }
//                if (location_labels[i].name == this.name+'_cur_lon') {
//                    cur_lon = location_labels[i].value;
//                }
//            }
//
//            console.log('>> por_lon : ', por_lon)
//            console.log('>> por_lat : ', por_lat)
//            console.log('>> pod_lon : ', pod_lon)
//            console.log('>> pod_lat : ', pod_lat)
//            console.log('>> cur_lon : ', cur_lon)
//            console.log('>> cur_lat : ', cur_lat)
//
//            if (por_lat != false && por_lon != false) {
//                const marker1 = new mapboxgl.Marker()
//                .setLngLat([por_lon, por_lat])
//                .addTo(map);
//                }
//
//            if (pod_lat != false && pod_lon != false) {
//                const marker2 = new mapboxgl.Marker({ color: 'black', rotation: 45 })
//                .setLngLat([pod_lon, pod_lat])
//                .addTo(map);
//                }
//
//        var route_labels = document.getElementsByClassName('route_label');
//        var cur_route = '';
//        for (var i=0; i<route_labels.length; i++) {
//            if (route_labels[i].name == this.name+'_route'){
//                cur_route = route_labels[i].value;
//            }
//        }
//        var coordinates = []
//        var route_sub = cur_route.split('/')
//        for (var i=0; i<route_sub.length; i++) {
//            coordinates.push([route_sub[i].split(',')[0],route_sub[i].split(',')[1]])
//            }
//        console.log('>> Coordinates : ', coordinates)
        rpc.query({
            model: 'track.trace.event',
            method: 'get_event_track_details',
            args: [null, this.name],
        }).then(function (result) {
            console.log("METHOD CALL SUCCESSFUL !!");
            console.log(">> por_lat : ", result['por_lat']);
            console.log(">> por_lon : ", result['por_lon']);
            console.log(">> pod_lat : ", result['pod_lat']);
            console.log(">> pod_lon : ", result['pod_lon']);
            console.log(">> por_lat : ", result['por_lat']);
            console.log(">> Route : ", result['route']);

            var por_lat = result['por_lat'];
            var por_lon = result['por_lon'];
            var pod_lat = result['pod_lat'];
            var pod_lon = result['por_lat'];

            if (por_lat != 0 && por_lon != 0) {
                const marker1 = new mapboxgl.Marker()
                .setLngLat([por_lon, por_lat])
                .addTo(map);
                }

            if (pod_lat != 0 && pod_lon != 0) {
                const marker2 = new mapboxgl.Marker({ color: 'black', rotation: 45 })
                .setLngLat([pod_lon, pod_lat])
                .addTo(map);
                }
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
