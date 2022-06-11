---
author: Amanda Regan
date: "2019-12-14"
title: Mapping the Gay Guides
lastmod: "2021-04-14"
description: ""
script: "viz/main-map/main.js"
layout: map
---

Each year Bob Damron's Address Book expanded and added new locations, updated entries, and provided readers with a refreshed guide exploring LGTBQ America. The interactive map below displays each of the locations listed in the Damron Guides by year. The filter controls below the map allow users to look at different years using the slider and filter the data according to the type of location as well as by the amenity categorizations that Damron used each year. For more details on the variables below, see our methodology which explains each category in depth.


<div class="row">
  <div id="accordion" class="col-lg-12">
    <div class="card">
    <div class="card-header" id="headingTwo">
      <h5 class="mb-0">
        <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
        <i class="fa-solid fa-angle-down"></i> How to Use this Map
        </button>
      </h5>
    </div>
    <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordion">
      <div class="card-body">
        Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. 3 wolf moon officia aute, non cupidatat skateboard dolor brunch. Food truck quinoa nesciunt laborum eiusmod. Brunch 3 wolf moon tempor, sunt aliqua put a bird on it squid single-origin coffee nulla assumenda shoreditch et. Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident. Ad vegan excepteur butcher vice lomo. Leggings occaecat craft beer farm-to-table, raw denim aesthetic synth nesciunt you probably haven't heard of them accusamus labore sustainable VHS.
      </div>
    </div>
  </div>
  </div>
</div>

<div class="row visualization">
  <div class="col-lg-12">
    <div id="map" style="height: 400px;"></div>
  </div>
</div>
<div class="viz-info" style="margin-top: 15px;"></div>
<div class="container card" style ="margin-top: 30px;">
<h4 style="margin-top:15px">Filter the Data</h4>
<hr style="margin-top:0px;">
<form id="mggmapcontrols" class="card-body" style="padding-top: 0px;">
<div class="row">
  <div class="col-lg-9">
    <div class="form-floating">
      <p>Year:</p>
      <input type="range" class="form-range" min="1965" max="1980" step="1" value="1965" id="map-viewby-year" width="100%" oninput="Year='rangeInput.value'" style="width:100%;">
      <label for="map-viewby-year" class="float-left form-label">1965</label>
      <label for="map-viewby-year" class="float-right form-label">1980</label><br>
    </div>
  </div>
  <div class="col-lg-3">
    <div class="form-floating">
      <div class="custom-control custom-switch">
        <input type="checkbox" class="custom-control-input" id="verified-locations">
        <label class="custom-control-label" for="verified-locations">Show only Verified Locations</label>
      </div>
    </div>
  </div>
</div> <!-- end row -->
<hr>
<div class="row">
  <!-- State dropdown -->
  <div class="col-lg-4">
    <div class="form-floating">
      <label for="map-viewby-state">State:</label>
      <select class="form-control form-control" id="map-viewby-state">
        <option selected>All</option>
        <option value="AK">Alaska</option>
        <option value="AL">Alabama</option>
        <option value="AR">Arkansas</option>
        <option value="AZ">Arizona</option>
        <option value="CA">California</option>
        <option value="CO">Colorado</option>
        <option value="CT">Conneticut</option>
        <option value="DE">Delaware</option>
        <option value="FL">Florida</option>
        <option value="GA">Georgia</option>
        <option value="HI">Hawaii</option>
        <option value="IA">Iowa</option>
        <option value="ID">Idaho</option>
        <option value="IL">Illinois</option>
        <option value="IN">Indiana</option>
        <option value="KS">Kansas</option>
        <option value="KY">Kentucky</option>
        <option value="LA">Louisiana</option>
        <option value="MA">Massachusetts</option>
        <option value="MD">Maryland</option>
        <option value="ME">Maine</option>
        <option value="Mexico">Mexico</option>
        <option value="MI">Michigan</option>
        <option value="MS">Mississippi</option>
        <option value="MN">Minnesota</option>
        <option value="MO">Missouri</option>
        <option value="MT">Montana</option>
        <option value="NE">Nebraska</option>
        <option value="NH">New Hampshire</option>
        <option value="NJ">New Jersey</option>
        <option value="NC">North Carolina</option>
        <option value="NV">Nevada</option>
        <option value="NM">New Mexico</option>
        <option value="NY">New York</option>
        <option value="ND">North Dakota</option>
        <option value="OH">Ohio</option>
        <option value="OK">Oklahoma</option>
        <option value="OR">Oregon</option>
        <option value="PA">Pennsylvania</option>
        <option value="RI">Rhode Island</option>
        <option value="SC">South Carolina</option>
        <option value="SD">South Dakota</option>
        <option value="TN">Tennessee</option>
        <option value="TX">Texas</option>
        <option value="UT">Utah</option>
        <option value="VA">Virginia</option>
        <option value="WA">Washington</option>
        <option value="District of Columbia">Washington, D.C.</option>
        <option value="WV">West Virginia</option>
        <option value="WI">Wisconsin</option>
        <option value="WY">Wyoming</option>
      </select>
    </div>
  </div>

  <!-- Type dropdown -->
  <div class="col-lg-4">
    <div class="form-floating">
      <label for="map-viewby-type">Location Type:</label>
      <select class="form-control form-control" id="map-viewby-type">
        <option selected value="All">All</option>
        <option value="Bars/Clubs">Bars or Clubs</option>
        <option value="Baths">Baths</option>
        <option value="Hotel">Hotels</option>
        <option value="Cruising Areas">Crusing Areas</option>
        <option value="Restaurant">Restaurants</option>
        <option value="Book Store">Book Stores</option>
        <option value="Theatre">Theatres</option>
        <option value="Business">Businesses</option>
        <option value="Church">Religious Institutions or Groups</option>
      </select>
    </div>
  </div>

  <!-- Amenities dropdown -->
  <div class="col-lg-4">
    <div class="form-floating">
      <label for="map-viewby-amenities">Location Amenities:</label>
      <select class="form-control form-control" id="map-viewby-amenities">
        <option selected>All</option>
        <option value="(*)">(*) - Very Popular</option>
        <option value="(AH)">(AH) - After Hours</option>
        <option value="(AYOR)">(AYOR) - At Your Own Risk - Dangerous - Usually Fuzz</option>
        <option value="(B)">(B) - Blacks Frequent</option>
        <option value="(BA)">(BA) - Bare-Ass (Usually nude beach)</option>
        <option value="(BYOB)">(BYOB) - Bring Your Own Bottle</option>
        <option value="(C)">(C) - Coffee, Soft Drinks, and Sometimes Snacks</option>
        <option value="(D)">(D) - Dancing</option>
        <option value="(HOT)">(HOT) - Dangerous - Usually Fuzz</option>
        <option value="(E)">(E) - Entertainment</option>
        <option value="(FFA)">(FFA) - Final Faith of America, or ask your friendly SM Serviceman</option>
        <option value="(H)">(H) - Hotel, Motel, Resort, or other Overnight Accomodation</option>
        <option value="(M)">(M) - Mixed - Some Straights</option>
        <option value="(MCC)">(MCC) - Metropolitan Community Church</option>
        <option value="(OC)">(OC) - Older/More Mature Crowd</option>
        <option value="(P)">(P) - Private - Inquire Locally as to Admission</option>
        <option value="(PE)">(PE) - Pretty Elegant - Often Coat or Tie</option>
        <option value="(PT)">(PT) - Pool Table</option>
        <option value="(R)">(R) - Restaurant</option>
        <option value="(RT)">(RT) - Raunchy Types - Hustlers, Drags, and other 'Downtown Types'</option>
        <option value="(S)">(S) - Shows - Impersonators or Pantomime Acts - Often Touristy</option>
        <option value="(SM)">(SM) - Some Motorcycle & Leather</option>
        <option value="(W)">(W) - Western or Cowboy Types</option>
        <option value="(WE)">(WE) - Weekends</option>
        <option value="(YC)">(YC) - Young/Collegiate Types</option>
        <option value="Cruisy Area">Cruisy Areas</option>
      </select>

    </div>
  </div>
</div> <!-- end row -->
<button style="margin-top:10px;" type="button" id="runbutton" class="btn btn-primary">Submit</button>
<button style="margin-top:10px;" type="button" id="reset-btn" class="btn btn-primary">Reset</button>
</form>
</div>

<div class="row">
  <div class="col-lg-12" id="mggdata_table">
    <table id="example" class="table table-striped table-bordered" width="100%">
      <thead>
              <tr>
                  <th>Title</th>
                  <th>Description</th>
                  <th>City</th>
                  <th>State</th>
                  <th>Amenities</th>
                  <th>Type</th>
              </tr>
          </thead>
          <tbody>
              </tbody>
</table>

  </div>
</div>
