# How to thoughts:

_(This whole file is rough and my scribbled while working out how to do this.)_

Looks like macOS term can handle emoji & em dashes, so works a treat just to run it directly.

I’m not checking for ["places"]["posts"] with > 10 photos, dayone2 cli will yell if you try it. I only have 1 so will fix it manually.

Not dealing with place “notes” that duplicate post “notes”. I think this was left over from a rego 1 --> rego 2 migration? Started to think about it but cbf.



# rego.json

## ROOT
>  "build": "500",

*Ignore*
rego internal build number I assume.

>  "collections": [

*Ignore*
Breakdown of continents, dont care, only set these up as a workaround to a rego problem when we broke the app with too many records, more than 200 or 400? don't remember. They fixed it, but it's super slow.

>  "date": "2017-08-26T15:10:06Z", 

*Ignore*
Date when the rego.json was sync'd? Not sure, doesn't matter

>  "device": "Hide", 

*Ignore*
iPhone name, ignore.

>  "pinColors": {

*CHECK*
Categories, map to dayone tags

    "Blue": "Tea", 				"pinColor": 4
    "Green": "Places to go", 			not used any more
    "Orange": "Drinking Establishment", 	"pinColor": 1
    "Purple": "Coffee Supplies", 		"pinColor": 3
    "Red": "Coffee", 				"pinColor": 2
    "Yellow": "Food House" --> 		"pinColor": 0


>  "places": [

*CHECK*
The goods. See below.

>  "version": "2.6"

*Ignore*
Rego app version

## PLACES
>      "addressDictionary": {
*Ignore*
cbf, dayone works it out when adding via coords.
Checked, each entry has coords.

>     "collections": [
*Ignore*
Don't want to keep geo categories, I added them because rego was buggy viewing all.

>      "createdAt": "2013-09-23T11:04:17Z", 
*Ignore*
Record creation, don't really care, get the date from the photos (posts)

>      "isFavorite": 0, 
*Ignore*
Never used by us

>      "latitude": 44.13384573792996, 
>      "longitude": 9.726998333584568, 
*CHECK*
need dis, map to dayone2 cords

>      "mapType": 0, 
*Ignore*
No idea what this is, it's 0 throughout the file.

>      "name": "Corneglio", 
*CHECK*
Need, first line into dayone2 to make it the header.

>      "notes": "September 23, 2013 \u2014 Tasty house wine!", 
*CHECK*
Full record notes, going to deal with dupes and import these first, then each post note.
There is always a key, sometimes it is empty.

>      "parseID": "tkMaz9Z2GK", 
*Ignore*
Only have one of these, no idea what it does.

>      "pinColor": 0, 
*CHECK*
map to pincolour tag above.

>      "posts": [
*CHECK*
photos and comments, this is the bulk of the data, details below.

>      "updatedAt": "2016-02-26T11:26:47Z"
*Ignore*
don't care

>      "venueID": "56d2eba7cd10603390fed4d2"
*CHECK*
Make this a foursquare link by appending 
https://foursquare.com/v/
eg
https://foursquare.com/v/56d2eba7cd10603390fed4d2

## POSTS
>          "createdAt": "2017-08-21T22:31:25Z", 
*Ignore*
Don't care, getting date from date field

>          "date": "2017-08-04T13:27:02Z", 
*CHECK*
most important field, gather posts with the same date (eg 2017-08-04) and make that a dayone2 post.
dayone2 will barf if you have more than 10 pics, I'm not handling that as only have 1 record out of 450

>          "filename": "7FF6F6B5-0A4E-4986-AE83-C87DED7AE4C4", 
*CHECK*
add filepath to dropbox folder, add .jpg, they're all .jpg's, think rego reencodes your photos, they're all low res :'(

>          "isKeyPhoto": 0, 
*Ignore*
Eh don't care.

>          "isShared": 1, 
*Ignore*
No idea, only on that strange parseid record. More rego 1 DM left overs?

>          "note": "I haven't washed!", 
*CHECK*
Maybe the rego 1 --> rego2 DM left these floating around after moving them to notes on the record? Then after the DM you could add more, which meant there is a mix of stuff that is DM'd no "notes" and some that isn't. Either way, just import each after record notes, better to have dupes than lost info. Can manually update if we're bothered in dayone. Could do something tricky and check but eh.

>          "position": 0, 
*Ignore*
left over from the old rego? Can you position/order photos now? Must have been able to before? Some data is >0 but eh don't care.

>          "type": 32767, 
*Ignore*
rego only uses 2 types, '1' or '32767'.
1 = photo, which we always care about. it could have a note, which I am now copying across regardless and making dupe data. 32767 is a note without a photo, and once again copying across. so ignore type

>          "updatedAt": "2014-07-13T13:53:47Z"
*Ignore*
deffo don't care.
