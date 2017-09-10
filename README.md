# rego-to-dayone2
Migrate a Rego (regoapp.com) dropbox backup (rego.json) to Day One (dayoneapp.com) via macOS dayone2 cli

I needed to do this as Rego could not handle my ~450 resturant "places" and ~2500 photo "posts". I couldn't find any resources or tools so decided to learn/play with Python and see what I could do.

Play with these options in the script before running:

### Testing stuff
* print_debug = if true, prints lots of debug info.
* restrict_records = if true, only runs select records, not all, for testing.
* record_min & record_max = list indexes of records to run in. Set to 0 and 49 to run in the first 50. In my testing, dayone2 did strange things if you ran more than 100 records in at once. I opened dayone, ran in 100 records, quit dayone, rince, repeat.
* photos_debug_limit_to_one = if true, only sends the first photo to dayone2 per post. Do this if you haven't subscribed and want to test, as dayone2 cli doesn't let you have more than 1 photo.
* dayone_write = will only send script output to dayone2 if true.
### Options
* photo_path = will be appended to photo file names, full path.
* rego_path = rego.json location.

## FYI
There are no tests, checks or balances in this script, given I only plan to ever run it once. Please review before use and use at your own peril. 

## More info
My [notes and ramblings](NOTES.md) about the rego.json spec.
