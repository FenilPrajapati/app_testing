odoo.define('freightbox.vessel_tracking', function (require) {
    'use strict';
    var rpc = require('web.rpc');

    mapboxgl.accessToken = 'pk.eyJ1IjoiYWpheS1wb3dlcnBib3giLCJhIjoiY2xjOG9reHk5M2s0ejN2cGp0dWxhYXJjZSJ9.3JGZaTYDaZlfOWcv1J-wbw';
    var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v12',
    center: [76.9921, 18.8127],
    zoom: 3
    });

    $(document).on('click', '#vessel_checkbox', function(){
        if (map != null){
            map.remove();
            mapboxgl.accessToken = 'pk.eyJ1IjoiYWpheS1wb3dlcnBib3giLCJhIjoiY2xjOG9reHk5M2s0ejN2cGp0dWxhYXJjZSJ9.3JGZaTYDaZlfOWcv1J-wbw';
            map = new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/mapbox/streets-v12',
            center: [76.9921, 18.8127],
            zoom: 3
            });
        }
        var input_vars = document.querySelectorAll('input');
        const selected_routes = []
        var selected_index = []
        for (var k=0; k<input_vars.length; k++) {
            if (input_vars[k].id == 'vessel_checkbox' && input_vars[k].checked == true) {
                selected_routes.push(input_vars[k].name+'_route')
                selected_index.push(input_vars[k].name)
            }
        }
        var route_labels = document.getElementsByClassName('route_label');
        var location_labels = document.getElementsByClassName('location_label');
        var tnt_divs = document.getElementsByClassName('vessel-track');
        var route_labels = document.getElementsByClassName('route_label');
        var lines = []
        console.log(">>> selected_routes : ", selected_routes)
        for (var i=0; i<route_labels.length; i++) {
            console.log(">>> selected_routes : ", selected_routes)
            console.log(">>> route_labels[i].name : ", route_labels[i].name)
            console.log(">>> selected_routes.includes(route_labels[i].name) : ", selected_routes.includes(route_labels[i].name))
            if (selected_routes.includes(route_labels[i].name)){
                console.log(">>> INSIDE IF")
                var cur_route = route_labels[i].value
                var new_coordinates = []
                var route_sub = cur_route.split('/')
                for (var j=0; j<route_sub.length; j++) {
                    new_coordinates.push([route_sub[j].split(',')[0],route_sub[j].split(',')[1]])
                }
                var layer_id = "layer_"+i
                var source_id = "source_"+i

                lines.push({
                    "type": "Feature",
                    "geometry": {
                      "type": "LineString",
                      "coordinates": new_coordinates
                    }
                });
            }
        }
        console.log(">>> LINES : ",lines)
        if (lines.length > 0) {
            map.on('load', function() {
                console.log(">>> CHECKPOINT 1")

              map.addSource('lines', {
                  "type": "geojson",
                  "data": {
                    "type": "FeatureCollection",
                    "features": lines
                  }
                });
                console.log(">>> CHECKPOINT 2")
                map.addLayer({
                  "id": "lines",
                  "type": "line",
                  "source": "lines",
                  "layout": {
                    "line-cap": "round",
                    "line-join": "round"
                  },
                  "paint": {
                    "line-color": "#888",
                    "line-width": 2
                  }
                });

            });
            console.log(">>> CHECKPOINT 3")
        }
        console.log(">>>> selected_index : ", selected_index)
        var pulsing_dot_created = false;
        var live_loc_data = [];
        for (var i=0; i<selected_index.length; i++) {
            var por_lat = false;
            var por_lon = false;
            var pod_lat = false;
            var pod_lon = false;
            var por_text = false;
            var pod_text = false;
            var cur_lat = false;
            var cur_lon = false;

            for (var l=0; l<location_labels.length; l++) {
                if (location_labels[l].name == selected_index[i]+'_por_lat') {
                    por_lat = location_labels[l].value;
                }
                if (location_labels[l].name == selected_index[i]+'_por_lon') {
                    por_lon = location_labels[l].value;
                }
                if (location_labels[l].name == selected_index[i]+'_pod_lat') {
                    pod_lat = location_labels[l].value;
                }
                if (location_labels[l].name == selected_index[i]+'_pod_lon') {
                    pod_lon = location_labels[l].value;
                }
                if (location_labels[l].name == selected_index[i]+'_por_text') {
                    por_text = location_labels[l].value;
                }
                if (location_labels[l].name == selected_index[i]+'_pod_text') {
                    pod_text = location_labels[l].value;
                }
                if (location_labels[l].name == selected_index[i]+'_cur_lat') {
                    cur_lat = location_labels[l].value;
                }
                if (location_labels[l].name == selected_index[i]+'_cur_lon') {
                    cur_lon = location_labels[l].value;
                }
            }

            console.log('>> por_lon : ', por_lon)
            console.log('>> por_lat : ', por_lat)
            console.log('>> pod_lon : ', pod_lon)
            console.log('>> pod_lat : ', pod_lat)
            console.log('>> por_text : ', por_text)
            console.log('>> pod_text : ', pod_text)
            console.log('>> cur_lon : ', cur_lon)
            console.log('>> cur_lat : ', cur_lat)

            if (por_lat != false && por_lon != false) {
                var marker1 = new mapboxgl.Marker()
                .setLngLat([por_lon, por_lat])
                .addTo(map);

                console.log(">>>> por_text : ", por_text)

                if (por_text != false) {
                    var popup1 = new mapboxgl.Popup({ offset: 25, closeOnClick: true})
                    .setHTML(por_text);
                    marker1.setPopup(popup1);
                }
            }



            if (pod_lat != false && pod_lon != false) {
                var marker2 = new mapboxgl.Marker({ color: 'black', rotation: 45 })
                .setLngLat([pod_lon, pod_lat])
                .addTo(map);

                console.log(">>>> pod_text : ", pod_text)

                if (pod_text != false) {
                    var popup2 = new mapboxgl.Popup({ offset: 25, closeOnClick: true})
                    .setHTML(pod_text);

                    marker2.setPopup(popup2);
                }
            }

            if (cur_lat != false && cur_lon != false) {
                live_loc_data.push([cur_lon, cur_lat])
            }
        }

        if (live_loc_data.length > 0) {
            const size = 200;
            const pulsingDot = {
                    width: size,
                    height: size,
                    data: new Uint8Array(size * size * 4),

                    // When the layer is added to the map,
                    // get the rendering context for the map canvas.
                    onAdd: function () {
                    const canvas = document.createElement('canvas');
                    canvas.width = this.width;
                    canvas.height = this.height;
                    this.context = canvas.getContext('2d');
                },

                // Call once before every frame where the icon will be used.
                render: function () {
                    const duration = 1000;
                    const t = (performance.now() % duration) / duration;

                    const radius = (size / 2) * 0.3;
                    const outerRadius = (size / 2) * 0.7 * t + radius;
                    const context = this.context;

                    // Draw the outer circle.
                    context.clearRect(0, 0, this.width, this.height);
                    context.beginPath();
                    context.arc(
                    this.width / 2,
                    this.height / 2,
                    outerRadius,
                    0,
                    Math.PI * 2
                );
                context.fillStyle = `rgba(255, 200, 200, ${1 - t})`;
                context.fill();

                // Draw the inner circle.
                context.beginPath();
                context.arc(
                    this.width / 2,
                    this.height / 2,
                    radius,
                    0,
                    Math.PI * 2
                );
                context.fillStyle = 'rgba(255, 100, 100, 1)';
                context.strokeStyle = 'white';
                context.lineWidth = 2 + 4 * (1 - t);
                context.fill();
                context.stroke();

                // Update this image's data with data from the canvas.
                this.data = context.getImageData(
                    0,
                    0,
                    this.width,
                    this.height
                ).data;

                // Continuously repaint the map, resulting
                // in the smooth animation of the dot.
                map.triggerRepaint();

                // Return `true` to let the map know that the image was updated.
                return true;
                }
                };
                map.on('load', () => {
                map.addImage('pulsing-dot', pulsingDot, { pixelRatio: 2 });

                for (var i=0; i<live_loc_data.length; i++) {
                    var pulsing_dot_source = "pulsing-dot-source-"+i;
                    var pulsing_dot_layer = "pulsing-dot-layer-"+i;
                    var cur_lon = live_loc_data[i][0];
                    var cur_lat = live_loc_data[i][1];
                    map.addSource(pulsing_dot_source, {
                        'type': 'geojson',
                        'data': {
                            'type': 'FeatureCollection',
                            'features': [
                                {
                                    'type': 'Feature',
                                    'geometry': {
                                        'type': 'Point',
                                        'coordinates': [cur_lon, cur_lat] // icon position [lng, lat]
                                    }
                                }
                            ]
                        }
                    });
                    map.addLayer({
                        'id': pulsing_dot_layer,
                        'type': 'symbol',
                        'source': pulsing_dot_source,
                        'layout': {
                        'icon-image': 'pulsing-dot'
                        }
                    });
                }
            });
        }
    });
});
