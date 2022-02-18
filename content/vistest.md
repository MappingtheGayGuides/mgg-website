---
author: Amanda Regan
date: "2019-12-14"
title: Map Vis Test
lastmod: "2021-04-14"
description: ""
slug: "maptest"
---
{{< rawhtml >}}
    <!-- Load Leaflet, use newest version at http://leafletjs.com -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.6.0/leaflet.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.6.0/leaflet.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>

    <!-- load jQuery, use newest version at https://code.jquery.com   -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>

    <!-- Load Esri Leaflet, use newest version at http://esri.github.io/esri-leaflet -->
    <script src="https://unpkg.com/esri-leaflet/dist/esri-leaflet.js"></script>

    <!-- style the map -->
    <style>

      #map {
        position: absolute;
        height: 100vh;
        width: 100vw;
        top: 0;
        left: 0;
      }
    </style>
  </head>


  <div class="row">
  <div class="col-lg-10">
  <!-- Create div element to house the map -->
  <div id="map"></div>
  <div class="mypanel"></div>
  </div>
  </div>




  <script>
  //  Initialize the map with specified center coordinates and zoom level
    //for target area (North Dakota)
    var map = L.map('map', {
      center: [47.55, -100.34],
      zoom: 2,
    })
    //var map = L.map('map').setView([51.505, -0.09], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'your.mapbox.access.token'
    }).addTo(map);

    //var marker = L.marker([51.5, -0.09]).addTo(map);
    //marker.bindPopup("<b>Hello world!</b><br>I am a popup.");

    var markerGroup = L.featureGroup([]).addTo(map);

    // $.getJSON('http://localhost:', function(data) {
    //   for(var key in data.Sheet1){
    //     var latLng = L.latLng([data.Sheet1[key].Latitude, data.Sheet1[key].Longitude]);
    //     L.marker(latLng).bindPopup(data.Sheet1[key].Status).addTo(markerGroup);
    //   }
    // });




  $.getJSON('http://localhost:1313/api/v1/person', function(mggdata) {

      var text = `Date: ${mggdata.data.Year}<br>
                  Time: ${mggdata.data.title}<br>
                  Unix time: ${mggdata.data.id}`

      for(var key in mggdata.data){
      var latLng = L.latLng([mggdata.data[key].lat, mggdata.data[key].lon]);
      console.log(latLng);
      L.marker(latLng).bindPopup(mggdata.data[key].title).addTo(markerGroup);
         //var latLng = L.latLng([mggdata.data[key].lat, mggdata.data[key].lon]);
         //console.log(mggdata.data[0].lon);
       }

      //console.log(mggdata.data[0]);
      //$(".mypanel").html(text);
  });



    </script>
{{< /rawhtml >}}
