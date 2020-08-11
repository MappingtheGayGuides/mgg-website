---
author: Amanda Regan
date: "2020-02-11"
title: Methodology
description: "A description of the methodology behind Mapping the Gay Guides. On this page we discuss how we digitized the data and the decisions made during that process."
tag: digital history, dataset, methodology, damron gay guides, lgbtq history
lastmod: "2020-08-02"
images: ["/images/1976ExplanationofListings.png"]
---
### Creating a Dataset

Turning a historical document, such as the Damron Address Books, into data that can be used for mapping is a process fraught with methodological decisions that shape the resulting dataset. The goal of this page is to make visible the choices that were made and clarify our categorization of data.

<figure>
<img src="/images/methodology-typicallisting.png" class="image-right" style="width:350px;">
<figcaption class="caption-right alert-secondary" style="width:350px;"><small><p><b>Figure 1.</b> Example of typical listings in the <i>Damron Address Book</i>.</p></small></figcaption>
</figure>

Although the Damron Guides have been digitized up until 1980 they are only available via an academic subscription to the Alexander Street LGBT Thought and Culture database. In order to generate maps and visualizations based on the Damron Guides it is necessary to first transcribe the data included in the digitized images of the guide into text that is machine readable.

Listings in the Damron Guides are grouped by state and then by city. A typical entry in the guide (figure 1) includes the name of the establishment, an address, sometimes notes or warnings, and often an “Explanation of Listings” which were lettered designations describing Damron’s categorization of the location. For example, a location may contain a “(D)” next to it indicating that it is a popular location for Dancing. Our data mirrors the information included in each listing as closely as possible.

<figure>
<img src="/images/1976ExplanationofListings.png" class="image-left" style="width:350px;">
<figcaption class="caption-left alert-secondary" style="width:350px;"><small><p><b>Figure 2.</b> Explanation of Listings in the <i>Damron Address Book</i>. On this site we refer to these categories as "Amenity Features."</p></small></figcaption>
</figure>

We have chosen to maintain the categorization assigned by Damron and we use the term "Amenity Feature" to describe these categories. [(Read more about each of Damron's categories at the bottom of this page)](/methodology/#damron-s-establishment-features) However, we have also added our own classification in the "Type" field. The type field goes beyond Damron's categorization by describing locations as one or more of the following types: Bars/Clubs, Hotels, Church, Theatre, Restaurant, Business, Baths, Book Stores or Cruising Area. While some of our type designations overlap with Damron's categorization, we note that locations can often function as multiple types. For example, many bars were located inside hotels and in order to track this unique kind of space we've made these locations both bars and hotels. Likewise, in the cases where a straight establishment (like a mall) is noted for being "Cruisy" but is not listed under Cruising Areas in the guide, we've assigned the type of location as Cruising Area. As the guides grow in length the diversity of business types increases but Damron’s own classification system doesn’t account for the rise in bookstores, theaters, or escort services listed in the guides. We’ve added categories to account for such locations making the type classification more robust and nuanced than Damron's.
After transcribing and categorizing the data contained in the guide, it was necessary to associate the location's address with spatial longitude and latitude coordinates so that they could be plotted onto a map. This process is known as geocoding [link to wikipedia entry on geocoding here].

<figure>
<img src="/images/methodology-unclearaddresses.png" class="image-right" style="width:350px;">
<figcaption class="caption-right alert-secondary" style="width:350px;"><small><p><b>Figure 3.</b> Example of an unclear address in the <i>Damron Address Book</i>.</p></small></figcaption>
</figure>

Roughly 30% of the entries included in the Damron Address Books between 1965 and 1980 were addresses that we deemed "unclear." This meant that the addresses were either vague and un-mappable locations (i.e. "Inquire Locally" or "U.S. Hwy 67") or were locations that had descriptive street addresses that required us to identify them by hand (i.e. Rice Park or ‘Primrose Path’ – Senate St. near Capitol). Of these "unclear locations" we were able to identify correct locations for more than half. Addresses listed as "Verified Locations" denote the locations that were found by hand and make up about 21% of the dataset.


<figure>
<img src="/images/methodology-status-plot-08-02-2020.png" class="image-left" style="width:450px;">
<figcaption class="caption-left alert-secondary" style="width:450px;"><small><p><b>Figure 4.</b> Chart showing the breakdown between verified (21%), google verified (70%), and locations that could not be verified (9%).</p></small></figcaption>
</figure>

However, there were many locations that we were unable to associate a geographical location with. Often these were locations that simply stated "Inquire locally" or where the location was simply too vague to confidently identify. These locations make up 9% of the dataset and are marked by a note in the status column that reads: "Location could not be verified. General city or location coordinates used." Rather than ignoring these locations, we have opted to use general city coordinates for them. This means, however, that the default map shows all locations and there are frequently clusters of locations with general coordinates mixed with verified locations. We've opted to include these locations by default to demonstrate the growth of LGBTQ spaces in the South over time however were recognize that these locations can be somewhat misleading. Therefore we have included a checkbox on the map controls that will filter the map to show only verified locations.

<br>

* **Google Verified Location:** A location that was able to be verified using Google's Geocoding API.

* **Verified Location:** If a location was not a standard address that could be geocoded, we attempted to verify it manually. A "verified location" means that the location was verified manually by a member of the MGG team.

* **Location could not be verified. General city or location coordinates used:** For locations that our team was not able to verify manually, we've opted to include the general coordinates for the city. Because these generalized locations can skew the map and provide a false sense of the geographic landscape of a city, we've included a checkbox on our app that allows users to filter out these locations and look only at verified locations. However we've opted to include them by default in the map in order to depict the scale of the growth in LGBTQ establishments between 1965 and 1980.

### Damron's Amenity Features
How did Damron organize the gay world?

While you browse any of the maps on _Mapping the Gay Guides_, you’ll quickly notice the ability to search through the listings via “amenity features.” These categories are not our team’s creation; rather, these classifications were actually a part of the original listings during publication. The Damron publishers used a series of mostly letters to denote that certain establishments included particular features. The _Mapping the Gay Guides_ team cannot verify whether all of these amenity features are necessarily accurate, nor do we know Damron’s methodology in adding these letters to particular listings. However, the addition of these amenities features allows users to more thoroughly investigate the gay world the way thousands, perhaps millions of gay men understood it via these travel guides.

Damron’s “explanation of listings” remained remarkably consistent over the 15 years of data we currently have available. Subtle changes do occasionally appear, including sometimes changing a letter designation or including a whole new category. Below is a list of Damron’s amenity features in the year 1980. You’ll note that the Damron publishers offered their own explanations for each feature.

  * **`*` - Very Popular**
    * Damron used a small black star next to listings to denote that a location was popular. You’ll notice that in our data we’ve opted for an asterisk (`*`).
  * **`(AH)` – After Hours**
    * Bars and clubs made up a large, if not majority, of many cities’ listings in the guidebook. The nocturnal nature of the gay world meant gay men continued to look for places of enjoyment even after bar closing times. Establishment closing times differed greatly by city and state.
  * **`(AYOR)` –  At Your Own Risk – Dangerous – Usually Fuzz**
    * The AYOR designation was added in the 1977 Damron Address Book. Noting dangerous locations, AYOR later included the “usually fuzz” description. “Fuzz” likely refers to the appearance of police or law enforcement.
  * **`(B)` – Blacks Frequent**
    * This designation is Damron’s only amenity feature that specifically mentions race. The use of (B) first began in the 1970 guidebook, then referring to establishments that “blacks predominate.”
  * **`(BA)` – Bare-Ass (Usually nude beach)**
  * **`(BYOB)` – Bring Your Own Bottle**
    * The complications with restaurants securing liquor licenses meant that many locations allowed for outside alcohol to be brought into their premises.
  * **`(C)` – Coffee, Soft Drinks, Juices, Snacks**
  * **`(D)` – Dancing**
    * While it might seem obvious that many bars and clubs offered dancing, not all gay bars had the space for any dance floors. Upon Damron’s first publication in 1964, same-sex dancing in public was widely seen as taboo and, in many places including New York City, was outright illegal.
  * **`(E)` – Entertainment**
  * **`(FFA)` – Final Faith of America, or ask your friendly SM Serviceman**
    * This category is Damron’s attempt at subtlety. FFA actually has another acronym (which a quick Google search can reveal). The designation is reserved for bars or clubs where patrons can partake in a certain sexual act.
  * **`(H)` – Hotel, Motel, Resort, or other overnight accommodations**
  * **`(HIP)` – Heads Frequent**
    * This designation likely refers to the popularity of marijuana at a certain establishment.
  * **`(L)` or `(G)` – Ladies/Ms, but seldom exclusively unless noted OR Girls/Ms but seldom exclusively**
    * Damron used the (G) designation to denote “girls” until 1980 when he dropped the (G) in favor of (L). While many of the listings with the (L) or (G) might have been popular with lesbians, Damron also used the designation to describe places frequented by gay men that women (lesbian or straight) would also feel comfortable. Therefore, not all places listed with designation should be understood as “lesbian spaces.”
  * **`(M)` – Mixed – Some Straights**
    * This designation largely marked establishments that had a significant, if not a majority number of straight identified patrons, or persons who did not identify as gay. Damron likely used this designation to mark sites where gays and lesbians faced less hostility than at otherwise straight venues.
  * **`M.C.C.` – Metropolitan Community Church**
    * The first Metropolitan Community Church was founded in 1968 and gained popularity specifically by reaching out to members of LGBT communities. As mainstream Christian denominations have long denounced homosexuality as sinful, the M.C.C. allowed gay and lesbian Christians an accepting place for fellowship and worship.
  * **`(OC)` – Older/More Mature Crowd**
    * Modern American society largely prizes youth, and this includes gay male culture. Damron’s (OC) classification likely aided older men looking for spaces where they could find acceptance despite a culture of youth fetishization.
  * **`(P)` – Private – Inquire locally as to admission**
    * Many establishments often used the “private” designation to get around the possibility of police raids. Police raids against gay bars were common in the 1960s through 1980. It was harder to raid “private” clubs, however.
  * **`(PE)` – Pretty Elegant – often coat or tie**
  * **`(PT)` - Pool Table**
  * **`(R)` –  Restaurant**
  * **`(RT)` – Raunchy Types – Hustlers, Drags, and other ‘Downtown’ Types**
    * Damron began using the (RT) classification in 1972. It’s presence on the explanation of listings suggest Damron’s early attempts to highlight establishments that the guides deemed as less than reputable. The Damron guides link sex workers (hustlers) and “downtown types” (likely people who lived in the inner city) to places of vice, crime, and deviancy.
  * **`(S)` – Shows—Impersonators or Pantomime Acts—Often Touristy**
    * It’s likely that “impersonators” here is Damron’s designation of drag shows.
  * **`(SM)` - Some Motorcycle & Leather**
    * American motorcycle culture began in the 1940s and 1950s, and gay motorcycle clubs gained in popularity around the same time. Some participants in the culture found refuge in these roaming motorcycle communities as replacement meeting spots for the bars (which could be unsafe, especially with constant police raids).  Gay leather culture also allowed some gay men to embrace a masculine gay identity, one in opposition to the stereotyped femininity of “fairy” gay men.
  * **`(W)` - Western or Cowboy Types**
    * Somewhat similar to the (SM) classification above, Damron used the (W) designation to identify places with rodeo and/or western vibes. These establishments were particularly popular in the American West and South and projected a more masculine image of gay life.
  * **`(WE)` - Weekends**
    * Damron used (WE) to note places open on the weekends. This label was sometimes joined with the star symbol (or asterisk in our data), suggesting an establishment was popular on the weekends.
  * **`(YC)` - Young/Collegiate Types**
    * In opposition to the (OC) label, Damron utilized (YC) to note places popular with a younger in age crowd.

### Open Datasets

In line with reproducible research practices, all of our data and code is available on [GitHub.](https://github.com/MappingtheGayGuides) If you're interested in our raw data it can be found in the MGG-Data repository. This repository includes basic csv files with the raw data digitized from the Damron Guides. If you're interested in the code used to build the visualizations on this site you can find that code in the [MGG-App repository.](https://github.com/MappingtheGayGuides/MGG-App) All of the code used to generate this website is in the [MGG-Website](https://github.com/MappingtheGayGuides/mgg-website) repository.
