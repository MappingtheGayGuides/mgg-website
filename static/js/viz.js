
//ARC GIS JS
const apiKey = "AAPK913fd73cbefa48b5929c8df63e95db270yZCsUIDQf_nRatPI26GP3cKLfeGycrnILpoxgllDSZpmcM8MXFR1SZ9mHcIcprX";



const map = L.map('map', {
  maxZoom: 18
}).setView([0,0], 2);

L.esri.Vector.vectorBasemapLayer("ArcGIS:DarkGray", {
      apikey: apiKey
    }).addTo(map);

const mggdata = L.esri.Cluster.featureLayer({
  url: "https://services1.arcgis.com/x5wCko8UnSi4h0CB/arcgis/rest/services/mapping_the_gay_guides_data_19651980/FeatureServer/0"
})
.addTo(map);

mggdata.setWhere('Year=1965');

// Setup the Popup
      mggdata.bindPopup(function (layer) {
        return L.Util.template("<b>Location Name:</b> {title}</br><b>Description:</b> {description}<br><b>City/State:</b> {city}, {state}<br><b>Type:</b> {type}<br><b>Amenity Features:</b> {amenityfeatures}", layer.feature.properties);
      });

const year = document.getElementById("map-viewby-year");
const state = document.getElementById("map-viewby-state");
const runq = document.getElementById("runbutton");
const resetBtn = document.getElementById("reset-btn")

year.addEventListener("change", function(){
  mggdata.setWhere('Year=' + year.value);
});
state.addEventListener("change", function(){
  mggdata.setWhere("state='" + state.value + "'");
});

function query(){
  console.log('query running test');
};

runq.addEventListener('click', query);


console.log('State is set at:' + state.value)
console.log('Year ' + year.value);

resetBtn.addEventListener("click", function(){
  document.getElementById("mgg-map-filters").reset();
  console.log(year.value);
});
