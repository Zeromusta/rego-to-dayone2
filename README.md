# rego-to-dayone2
Migrate a Rego (regoapp.com) dropbox backup (rego.json) to Day One (dayoneapp.com) via macOS dayone2 cli

I needed to do this as Rego could not handle my ~450 resturant "places" and ~2500 photo "posts". I couldn't find any resources or tools so decided to learn/play with Python and see what I could do.

Play with these options in the script before running:

### Testing stuff
* print_debug = if true, prints lots of debug info.
* single_record = if true, only runs against one rego entry, for testing.
* record_index = array index to run in. Only used if single_record is True.
* photos_debug_limit_to_one = if true, only sends the first photo to dayone2 per post. Do this if you haven't subscribed and want to test.
* dayone_write = will only send script output to dayone2 if true.
### Options
* photo_path = will be appended to photo file names, full path.
* rego_path = rego.json location.

## FYI
There are no tests, checks or balances in this script, given I only plan to ever run it once. Please review before use and use at your own peril. 

## More info
My [notes and ramblings](NOTES.md) about the rego.json spec.
