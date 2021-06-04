document.addEventListener('DOMContentLoaded', function () {
    var mymap = L.map('mapid').setView([3.993717, -73.765649], 14);//lat long zoom

    // estetica del mapa
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox/streets-v11',
        // id: 'mapbox/satellite-v9',//tipo de mapa
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'your.mapbox.access.token'
    }).addTo(mymap);

    // adicion de marcador
    var marker = L.marker([3.993717, -73.765649]).addTo(mymap);

    //adicion de circulo
    var circle = L.circle([3.987, -73.775], {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: 500
    }).addTo(mymap);

    // adicion de poligono
    var polygon = L.polygon([
        [3.994, -73.754],
        [3.990, -73.754],
        [3.993, -73.747]
    ], {
        color: 'green'
    }).addTo(mymap);

    //adicion de leyendas popup a los elementos agregados
    marker.bindPopup("<b>Hello world!</b><br>I am a popup.").openPopup();
    circle.bindPopup("I am a circle.");
    polygon.bindPopup("I am a polygon.");

    //eventos
    mymap.on('click', onMapClick);
    
    function onMapClick(e) {
        // alert("You clicked the map at " + e.latlng);
        //poner popup sin nesecidad de ningun elemento quita el ope  popupa anterior y si hago click ene otra parte se borra
        var popup = L.popup();
        popup
            .setLatLng(e.latlng)
            .setContent("You clicked the map at " + e.latlng.toString())
            .openOn(mymap);
        // .setLatLng([51.5, -0.15])
        // .setContent("I am a standalone popup.")
    }

});

