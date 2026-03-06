---
author: Amanda Regan
date: "2020-02-11"
title: Methodology
description: "A description of the methodology behind Mapping the Gay Guides. On this page we discuss how we digitized the data and the decisions made during that process."
tag: digital history, dataset, methodology, damron gay guides, lgbtq history
lastmod: "2022-10-07"
images: ["/images/1976ExplanationofListings.png"]
---

# Methodology

Turning a historical document, such as the Damron Address Books, into data that can be used for mapping is a process fraught with methodological decisions that shape the resulting dataset. The goal of this section is to make visible the choices that were made and clarify our categorization of the data. Additionally, we offer some general considerations for using this historical dataset both on our site and in your own research.

## Creating the Data

### Digitization and Access
The Damron Guides have historically been scarce and hard to access. Only one library in the United States has an entire run of these rare sources. Although the Damron Guides have been digitized through 1980, they are only available via an academic subscription to the Alexander Street LGBT Thought and Culture database. The MGG Team has worked in collaboration with the ONE Archives at the University of Southern California to digitize the guides from 1981 through 2005. However, digitization is only one step toward mapping this data. In order to generate maps and visualizations based on the Damron Guides it is necessary to first transcribe the data included in the digitized images of the guide into text that is machine readable.

### Transcription
When we launched the initial version of this site in 2020, it included data from 1965 to 1980. Thanks to generous support from the National Endowment for the Humanities, we have since expanded the dataset to include an additional 23 years of data, now spanning from 1965 to 2003. 

The transcription of this data was handled by graduate student collaborators at California State University, Fullerton and Clemson University. Over the course of 4 years they transcribed each entry by hand. Once transcription was complete it was handed off to Clemson Digital History Ph.D. students who cleaned, processed, and geolocated the data. This painstaking process involved thousands of hours of careful work to ensure accuracy and consistency across nearly four decades of guidebooks. Each location was manually entered into our database with its name, address, city, state, amenity features, and any descriptive notes from the original guides.

As with any type of data entry, whether automated or manual, errors have likely been introduced into our dataset. However, our intent throughout this process has been to mirror the primary sources as closely as possible, preserving the language, categorizations, and structure of the original Damron Address Books. As our data has grown more complex and extensive, it has also become infinitely more interesting, revealing patterns of LGBTQ space-making and community formation across the United States over nearly forty years.

If you discover any errors in our data, we welcome your feedback. Please submit corrections or concerns through this form so we can continue to improve the accuracy and reliability of this resource.

### Understanding the Listings

<figure class="right"> <img src="/static/images/methodology-typicallisting.png" style="width:350px;"> <figcaption><small><p><b>Figure 1.</b> Example of typical listings in the <i>Damron Address Book</i>.</p></small></figcaption> </figure> 

Listings in the Damron Guides are grouped by state and then by city. A typical entry in the guide (Figure 1) includes the name of the establishment, an address, sometimes notes or warnings, and often an "Explanation of Listings" which were lettered designations describing Damron's categorization of the location. For example, a location may contain a "(D)" next to it indicating that it is a popular location for Dancing. Our data mirrors the information included in each listing as closely as possible.

The amenities changed over time and Damron regularly added, removed, or changed the amenity for particular categories. One notable change is the amenity (G) for "Girls, but seldom exclusively" which appears in the 1960s guides but is later changed to (L) for "Ladies" and eventually (W) for "Women." This presents a unique challenge for displaying this data.

<figure class="left"> <img src="/static/images/1976ExplanationofListings.png" style="width:350px;"> <figcaption><small><p><b>Figure 2.</b> Explanation of Listings in the <i>Damron Address Book</i>. On this site we refer to these categories as "Amenity Features."</p></small></figcaption> </figure> 

We have chosen to maintain the categorization assigned by Damron and we use the term "Amenity Feature" to describe these categories. 

The previous iteration of _Mapping the Gay Guides_ also included a type categorization. While this still exists in the raw data, we have chosen not to display it here for now. We originally made type determinations during the transcription process, however beginning in the 1980s the guides begin separating entries not only by state and city but also by type. But these categories were inconsistent and changed over time. They also did not match the exisiting types that were added in the first phase of the project. While we have recorded Damron's type in the raw data, we have not yet been able to ensure they are standardized and clean. We hope to be able to release more data about type in the future. If you are using the raw data and have questions, don’t hesitate to reach out our team. 

### Geocoding
After transcribing the data contained in the guide, it was necessary to associate the location's address with spatial longitude and latitude coordinates so that they could be plotted onto a map. This process is known as geocoding.

<figure class="right"> <img src="/static/images/methodology-unclearaddresses.png" style="width:350px;"> <figcaption><small><p><b>Figure 3.</b> Example of an unclear address in the <i>Damron Address Book</i>.</p></small></figcaption> </figure> 

Roughly 43% of the entries included in the Damron Address Books between 1965 and 2003 were addresses that we deemed "unclear." This meant that the addresses were either vague and un-mappable locations (i.e. "Inquire Locally" or "U.S. Hwy 67") or were locations that had descriptive street addresses that required us to identify them by hand (i.e. Rice Park or 'Primrose Path' – Senate St. near Capitol). Of these "unclear locations" we were able to identify correct locations for more than half. Addresses listed as "Verified Locations" denote the locations that were found by hand and make up about 26.5% of the dataset.

However, there were many locations that we were unable to associate a geographical location with. Often these were locations that simply stated "Inquire locally" or where the location was simply too vague to confidently identify. These locations make up 16.6% of the dataset and are marked by a note in the status column that reads: "Location could not be verified. General city or location coordinates used." Rather than ignoring these locations, we have opted to use general city coordinates for them. This means, however, that the default map shows all locations and there are frequently clusters of locations with general coordinates mixed with verified locations. We've opted to include these locations by default to demonstrate the growth of LGBTQ spaces over nearly forty years, however we recognize that these locations can be somewhat misleading. Therefore, we have included a checkbox on the map controls that will filter the map to show only verified locations.

#### Location Verification Categories:
* **Google Verified Location:** A location that was able to be verified using Google's Geocoding API.
* **Verified Location:** If a location was not a standard address that could be geocoded, we attempted to verify it manually. A "verified location" means that the location was verified manually by a member of the MGG team.
* **Location could not be verified. General city or location coordinates used:** For locations that our team was not able to verify manually, we've opted to include the general coordinates for the city. Because these generalized locations can skew the map and provide a false sense of the geographic landscape of a city, we've included a checkbox on our app that allows users to filter out these locations and look only at verified locations. However, we've opted to include them by default in the map in order to depict the scale of the growth in LGBTQ establishments between 1965 and 2003.
 
## How Should This Site and These Visualizations Be Used?

Mapping the Gay Guides offers three primary ways to explore the data from the Damron Address Books. Each visualization has been designed with specific research questions and exploratory needs in mind, but each also has limitations that users should understand.

### The Interactive Map

* The interactive map allows you to visualize the geographic distribution of LGBTQ spaces across the United States from 1965 to 2003. You can filter locations by year, state, amenity feature, and location type. The map uses Mapbox for rendering and allows you to zoom in on specific regions or cities to explore local LGBTQ geographies.
* By default the map shows all locations in a particular year to demonstrate the breadth and geographical diversity of LGTBQ spaces. However, that means that some locations with genearl coordinates appear skewing the depicting of where locations appear when zoomed in. To rectify this, we have added a "remove unclear addresses" checkbox in the filter options which removes any locations that had unclear addresses and use general rather than specific coordinates. This allows users to remove those locations to understand the spatial layout of a particular city or space. 
* **The map is best used for:**
    * Exploring the geographic distribution of LGBTQ spaces in a specific city, state, or region
    * Tracking how the number and types of locations changed over time in a particular area
    * Identifying patterns of LGBTQ community formation and spatial clustering
    * Finding specific establishments in a city and learning what Damron said about them
* **Limitations:**
    * The map shows the locations as they were listed in the Damron guides, not necessarily all LGBTQ spaces that existed at the time. Damron's coverage was incomplete and reflected the biases and limitations of his network.
    * Locations with unclear addresses appear using general city coordinates, which can create misleading clusters. Use the "Remove unclear addresses" filter to see only verified locations.
    * The map represents a snapshot of what was published each year. Typically Damron would have been putting together an edition of the guide the previous year. For example, data for the 1980 guide was likely collected and refined in 1979. Businesses may have opened or closed between editions, and Damron's information could be out of date.
    * These guides were primarily aimed at gay men and how they experienced the world. It reflects the spaces that were important to them. As a result, lesbian spaces and other queer venues are frequently underrepresented. We are working on adding new layers of data from other guidebooks.

### The Amenities Visualization
* One of the unique qualities of the Damron Guides compared to other travel guides was the extensive categorization of spaces. This adds a unique layer to the data that is ripe for historical investigation and digitizing this data has made these categorizations accessible.
* The amenities page provides a set of interactive charts that show how different amenity features changed over time. Users can compare up to three amenities simultaneously, view data as relative percentages of all locations in a year or as a raw count, and see geographic distributions on an integrated map. This visualization makes it possible to look at this data and Damron's view of the gay world in a way that would be extremely difficult using the physical guidebooks and traditional historical research methods. 
* **The amenity visualization is best used for:**
    * Tracking trends in how LGBTQ spaces were categorized over time. For example the rise of wheelchair-accessible venues after the Americans with Disabilities Act was passed in 1990 or the changes in venues Damron deemed friendly to women. 
    * Comparing multiple amenity features to understand relationships between different types of spaces.
    * Analyzing regional variations in how spaces were categorized.
    * Understanding broader patterns in LGBTQ commercial culture and community needs.
* **Limitations:**
    * This data is based on historical sources that reflect Bob Damron's own biases and must be read "against the grain." Understanding Bob Damron's perspective, business model, and the context in which these guides were created is essential. [Read more about Bob Damron and the history of the guides](/about-the-address-books).
    * Amenity features reflect Damron's categorization system, which changed over time and carried its own biases. For example, the use of "RT" for "Raunchy Types" conflated race, class, and morality. You can read more about all of the amenities that appeared in the Damron Guides between 1965 and 2003 on our [Amenity Guide](/amenity-guide).
    * The data shows what Damron reported and thought of spaces, not as accurate representations of the population that frequented that space. Some venues may have self reported to Damron using a form in the guide.
    * Some amenity features appear or disappear over the years as Damron added or removed categories, making some comparisons over time difficult. 
    * Percentage visualizations can be misleading when absolute numbers are small. The relative percentage on the amenity page represents the total number of locations for that amenity in a particular year divided by the total number of listings in that year. Be sure to compare the relative percentages with the raw numbers. 

### The Locations Database
* The database allows you to search, filter, and sort through all locations in our dataset. You can search by keywords, filter by year, state, or amenity, and sort by different fields. Each entry shows the location's name, description, address, and all associated amenity features.
* **The locations database is best used for:**
    * Finding specific establishments by name or location
    * Conducting keyword searches across descriptions (e.g., searching for "Latin" or "women" or "dancing")
    * Systematically reviewing all locations in a particular city or year
    * Exporting lists of locations that meet specific criteria for further research (feature coming soon)
* **Limitations:**
    * The database reflects our transcription of the original guides. While we strived for accuracy, transcription errors may exist.
    * Descriptions are exactly as they appeared in the guides, preserving historical language that may be outdated or offensive by contemporary standards.
    * Not all locations have complete information. Some entries in the original guides were minimal (just a name and address).

## General Considerations for All Visualizations
These visualizations represent historical documents created by Bob Damron and his network, not comprehensive surveys of LGBTQ life. As such, its important to recognize the nature of these sources and how they shape the data and conclusions on this site. 

First, Bob Damron’s Address Book primarily reflected commercial gay male culture, with less coverage of other queer spaces. Spaces for lesbians or other groups are underrepresented. 

Second, the data for each guidebook was typically created the year before the published cover data. For example, data for the 1980 edition was likely collected in 1979. Each guidebook represents a moment in time and may not have reflected closures and openings until the following year’s edition. 

 
## How Can I Use This Data in My Own Research?
We believe in open source data and making our work freely available to researchers, educators, students, and the public. Our complete dataset and code are available through our [GitHub repository.](https://github.com/MappingtheGayGuides/MGG-Data)

### Accessing the Data

All of our data is available on our [github repository.](https://github.com/MappingtheGayGuides/MGG-Data) Data in data.csv and data.rds contain full datasets. 

### Using the Data Responsibly

If you use this data in your research, presentations, publications, or creative work, we ask that you:

1. **Cite the project appropriately:**
_Mapping the Gay Guides_, Amanda Regan and Eric Gonzaba, (2019-): [http://www.mappingthegayguides.org](http://www.mappingthegayguides.org).

2. **Acknowledge the limitations and historical context:** This data represents what was published in the Damron guides, not a complete record of LGBTQ spaces. It reflects historical biases, commercial interests, and the limitations of Damron's information network. The language and categorizations in the guides reflect their time period. They include terms and classifications that may be considered outdated or offensive today but are preserved to maintain accuracy with the primary sources.

3. **Share your work with us:** We'd love to know how you're using the data! Please contact us at info@mappingthegayguides.org to share your research, creative projects, teaching materials, or other uses of the dataset.

We will be publishing the complete dataset formally. In the meantime, all data is available through GitHub under a Creative Commons Attribution-NonCommercial (CC BY-NC) license.

### Questions or Collaborations?

If you have questions about using the data, want to discuss potential collaborations, or need assistance with technical aspects of working with the dataset, please reach out to us at info@mappingthegayguides.org.

