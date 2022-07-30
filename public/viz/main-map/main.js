
//ARC GIS JS
const apiKey = "AAPK913fd73cbefa48b5929c8df63e95db270yZCsUIDQf_nRatPI26GP3cKLfeGycrnILpoxgllDSZpmcM8MXFR1SZ9mHcIcprX";
var dataSet = [
    ['Tiger Nixon', 'System Architect', 'Edinburgh', '5421', '2011/04/25', '$320,800'],
    ['Garrett Winters', 'Accountant', 'Tokyo', '8422', '2011/07/25', '$170,750'],
  ]

const t = $('#example').DataTable({
  "pageLength": 25
});


const map = L.map('map', {
  maxZoom: 13,
  minZoom: 3
}).setView([37.45,-93.85], 3);

L.esri.Vector.vectorBasemapLayer("ArcGIS:DarkGray", {
      apikey: apiKey
    }).addTo(map);

const mggdata = L.esri.Cluster.featureLayer({
  url: "https://services1.arcgis.com/x5wCko8UnSi4h0CB/arcgis/rest/services/mapping_the_gay_guides_data_19651980/FeatureServer/0"
})
.addTo(map);
$( document ).ready(function() {
    console.log( "ready!" );
    mggdata.setWhere('Year=1965');
    gentable('Year=1965');
});


// Setup the Popup
      mggdata.bindPopup(function (layer) {
        return L.Util.template("<b>Location Name:</b> {title}</br><b>Description:</b> {description}<br><b>City/State:</b> {city}, {state}<br><b>Type:</b> {type}<br><b>Amenity Features:</b> {amenityfeatures}", layer.feature.properties);
      });
//form values
const year = document.getElementById("map-viewby-year");
const state = document.getElementById("map-viewby-state");
const type = document.getElementById("map-viewby-type");
const amenities = document.getElementById("map-viewby-amenities");
const runq = document.getElementById("runbutton");
const resetBtn = document.getElementById("reset-btn")

runq.addEventListener('click', query);
//this is the start of the code needed to count the entries. Need to figure out how to tie it to the update function. See https://developers.arcgis.com/esri-leaflet/api-reference/tasks/query/ as reference
var cquery = L.esri.query({
    url: "https://services1.arcgis.com/x5wCko8UnSi4h0CB/arcgis/rest/services/mapping_the_gay_guides_data_19651980/FeatureServer/0"
})
var tquery = L.esri.query({
    url: "https://services1.arcgis.com/x5wCko8UnSi4h0CB/arcgis/rest/services/mapping_the_gay_guides_data_19651980/FeatureServer/0"
})


function runcount (){
  cquery.count(function (error, count, response) {
    if (error) {
    console.log(error);
    return;
    }
    //console.log('Found ' + count + ' features');
    $( ".info-count").remove();
    $( ".viz-info" ).append( "<p class='info-count alert alert-info' role='alert'>In " + year.value + " there were " + count + " locations that match the query criteria.</p>");
  });
};

function runcounterror (){
  cquery.count(function (error, count, response) {
    if (error) {
    console.log(error);
    return;
    }
    console.log('Found ' + count + ' features');
    $( ".info-count").remove();
    $( ".viz-info" ).append( "<p class='info-count alert alert-danger' role='alert'>The Damron Company did not publish a guide in 1967 therefore we have chosen not to display any data for this year.");
  });
};



//var dataSet = [];
function gentable(querycriteria){
  tquery.where(querycriteria).run(function (error, tabledeets, response) {
    if (error) {
    console.log(error);
    return;
    }
    console.log(tabledeets.features.length);

    var mgg_table = "";

    //this clears any previous data in the table
    t.clear().draw();
    var i;
    for (i=0; i < tabledeets.features.length; i++){
      var counter = i + 1

      t.row.add([tabledeets.features[i].properties.title, tabledeets.features[i].properties.Year, tabledeets.features[i].properties.description, tabledeets.features[i].properties.city,tabledeets.features[i].properties.state,tabledeets.features[i].properties.amenityfeatures,tabledeets.features[i].properties.type,tabledeets.features[i].properties.status]).draw(false);

    }

  });

}
console.log(dataSet);






function query(){
  if (year.value == 1967){
    qvalue = "Year=" + year.value;
    mggdata.setWhere(qvalue);
    runcounterror();
  } else {
  var qvalue = "";
  if (state.value != "All") {
    console.log("query has a state value");
    qvalue = "Year=" + year.value + " AND state='" + state.value + "'";
    console.log(qvalue);
  } else {
    console.log("state is set at all");
    qvalue = "Year=" + year.value;

    runcount();
  } if (type.value != "All") {
    console.log("query has type value");
    qvalue = qvalue + " AND type='" + type.value + "'";
    console.log(qvalue);
  }
  if (amenities.value != "All") {
    console.log("query has amenities value");
    qvalue = qvalue + " AND amenityfeatures LIKE '%" + amenities.value + "%'";
    console.log(qvalue);
  }

  mggdata.setWhere(qvalue);
  cquery.where(qvalue);
  runcount();
  gentable(qvalue);
}};



console.log(cquery);


console.log('State is set at:' + state.value)
console.log('Year ' + year.value);

resetBtn.addEventListener("click", function(){
  document.getElementById("mggmapcontrols").reset();
  $( ".info-count").remove();
  //$('#example').dataTable().clear();
  query();
  console.log(year.value);
});
