---
author: Amanda Regan
date: "2020-01-16"
title: Methodology
description: ""
tag: digital history, spatial history, mapping, damron gay guides, lgbtq history
---
Turning a historical document, such as the Damron Address Books, into data that can be used for mapping is a process fraught with methodological decisions that shape the resulting dataset. The goal of this page is to make visible the choices that were made and clarify our categorization of data.

Although the Damron Guides have been digitized up until 1980 they are only available via a subscription to an academic database. (which db?) In order to generate maps and visualizations based on the Damron Guides it is necessary to first transcribe the data included in the digitized images of the guide into text that is machine readable.

**figure 1 typical listing in damron guide**

Listings in the Damron Guides are grouped by state and then by city. A typical entry in the guide (figure 1) includes the name of the establishment, an address, sometimes notes or warnings, and often an "Explanation of Listings" which were lettered designations describing Damron's categorization of the location. For example, a location may contain a "(D)" next to it indicating that it is a popular location for Dancing. Our data mirrors the information included in each listing as closely as possible.

**Figure 2 Explanation of Listings**

We have chosen to maintain the categorization assigned by Damron and we use the term "Amenity Feature" to describe these categories. However, we have also added our own classification in the "Type" field. The type field goes beyond Damron's categorization by describing locations as one or more of the following types: Bars/Clubs, Hotels, Church, Theatre, Restaurant, Business, Baths, Book Stores or Cruising Area. While some of our type designations overlap with Damron's categorization, we note that locations can often function and multiple types. For example, many bars were located inside hotels and in order to track this unique kind of space we've made these locations both bars and hotels. Likewise, in the cases where a straight establishment (like a mall) is noted for being "Cruisy" but is not listed under Cruising Areas in the guide, we've assigned the type of location as Cruising Area. As the guides grow in length the diversity of business types increases but Damron’s own classification system doesn’t account for the rise in book stores, theatres, or escort services listed in the guides. We’ve added categories to account for such locations making the type classification more robust and nuanced than Damron's.
After transcribing and categorizing the data contained in the guide, it was necessary to associate the location's address with spatial longitude and latitude coordinates so that they could be plotted onto a map. This process is known as geocoding [link to wikipedia entry on geocoding here].

**Figure 3 - Unclear Address example from Guide**

Roughly 32% of the entries included in the Damron Address Books between 1965 and 1980 were addresses that we deemed "unclear." This meant that the addresses were either vague and unmappable locations (i.e. "Inquire Locally" or "U.S. Hwy 67") or were locations that had descriptive street addresses that required us to identify them by hand (i.e. Rice Park or ‘Primrose Path’ – Senate St. near Capitol). Of these "unclear locations" we were able to identify correct locations for more than half. Addresses listed as "Verified Locations" denote the locations that were found by hand and make up about 21% of the dataset.

However, there were many locations that we were unable to associate a geographical location with. Often these were locations that simply stated "Inquire locally" or where the location was simply too vague to confidently identify. These locations make up about 11% of the dataset and are marked by a note in the status column that reads: "Location could not be verified. General city or location coordinates used." Rather than ignoring these locations, we have opted to use general city coordinates for them. This means, however, that the default map shows all locations and there are frequently clusters of locations with general coordinates mixed with verified locations. We've opted to include these locations by default to demonstrate the growth of LGBTQ spaces in the South over time however were recognize that these locations can be somewhat misleading. Therefore we have included a checkbox on the map controls that will filter the map to show only verified locations.
Google Verified Location: A location that was able to be verified using Google's Geocoding API.

Verified Location: If a location was not a standard address that could be geocoded, we attempted to verify it manually. A "verified location" means that the location was verified manually by a member of the MGG team.

Location could not be verified. General city or location coordinates used: For locations that our team was not able to verify manually, we've opted to include the general coordinates for the city. Because these generalized locations can skew the map and provide a false sense of the geographic landscape of a city, we've included a checkbox on our app that allows users to filter out these locations and look only at verified locations. However we've opted to include them by default in the map in order to depict the scale of the growth in LGBTQ establishments between 1965 and 1980.
