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




$.getJSON('http://localhost:8080/api/v1/person', function(mggdata) {

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



// 
//
// $.getJSON('http://localhost:1313/api/v1/person', function(mggdata) {
//
//     var text = `Date: ${mggdata.data.Year}<br>
//                 Time: ${mggdata.data.title}<br>
//                 Unix time: ${mggdata.data.id}`
//
//     for(var key in mggdata.data){
//     var latLng = L.latLng([mggdata.data[key].lat, mggdata.data[key].lon]);
//     console.log(latLng);
//     L.marker(latLng).bindPopup(mggdata.data[key].title).addTo(markerGroup);
//        //var latLng = L.latLng([mggdata.data[key].lat, mggdata.data[key].lon]);
//        //console.log(mggdata.data[0].lon);
//      }
//
//     //console.log(mggdata.data[0]);
//     //$(".mypanel").html(text);
// });
