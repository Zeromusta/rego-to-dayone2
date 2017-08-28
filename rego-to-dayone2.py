import codecs
import json
from pprint import pprint
from subprocess import call

def format_for_dayone(text, iso_date, photos, tag, coords):
    """Build the 2 arguments (text & everything else) to pass to dayone2 cli"""
    formatted_list = []
    formatted_list.append(text)
    formatted_list.append("--coordinate " + coords + " --isoDate " + iso_date + " --tags " + tag)
    if photos:
        if photos_debug_limit_to_one: photos = photos.split()[0] + " "
        formatted_list[1] += " --photos " + photos + "--"
    else:
        formatted_list[1] += " --"
    return formatted_list
#

def write_to_dayone(dayone_list):
    """Take a formatted list of text & everything else, run dayone2 cli"""
    print("SCRIPT IS: echo \"" + dayone_list[0] + "\" | dayone2 " + dayone_list[1] + " new")
    try:
        retcode = call("echo \"" + dayone_list[0] + "\" | dayone2 " + dayone_list[1] + " new",
                       shell=True)
        if retcode < 0:
            print("Child was terminated by signal", -retcode)
        else:
            print("Child returned", retcode)
    except OSError as e:
        print("Execution failed:", e)
#

def get_tag_name(number):
    """Convert a pinColor to a tag string"""
    if number == 0:
        return "Food"
    elif number == 1:
        return "Drink"
    elif number == 2:
        return "Coffee"
    elif number == 3:
        return r"Coffee\ Supplies" #dayone2 cli needs the space escaped
    elif number == 4:
        return "Tea"
#

def get_date_only(iso_date_string):
    """Return the date from the start of an isoDate string, eg, 2017-01-01"""
    short_date = iso_date_string[:10]
    return short_date
#

def get_date_only_list(iso_date_string_list):
    """Return a list of only dates from a list of iso_date strings"""
    def_date_only_list = []
    for iso_date_string in iso_date_string_list:
        def_date_only_list.append(get_date_only(iso_date_string))
    return def_date_only_list
#

def get_full_photo_path(filename):
    """Append the photo path, add .jpg"""
    return photo_path + filename + ".jpg"
#

def remove_dupe_notes(place_notes, post_list):
    """Unfinished function, do no use"""
    deduped_place_notes = place_notes
    for post in post_list:
        if deduped_place_notes.find(post["note"]) > 0:
            deduped_place_notes.replace(post["note"], "")
            deduped_place_notes.replace("\n\n", "", 1)
    return deduped_place_notes
#

def get_post_day_list(post_list):
    """Create a unique list of iso from a post list,
    keeping the first iso date if multiple are on the same date
    """
    def_posts_date_list = []
    for post in post_list:
        if get_date_only(post["date"]) not in get_date_only_list(def_posts_date_list):
            def_posts_date_list.append(post["date"])
    return def_posts_date_list
#

def count_posts(places_list):
    """Run some analysis on rego.json, used for planning"""
    total_place_count = 0
    posts_more_than_10_count = 0

    for place in places_list:
        total_place_count = total_place_count + 1
        posts_date_dict = {}
        
        for post in place["posts"]:
            post_date = get_date_only(post["date"])
            post_date_found = False

            for date in posts_date_dict:
                date_date = get_date_only(date)
                if post_date == date_date:
                    post_date_found = True
                    posts_date_dict[date] = posts_date_dict[date]+1

            if not post_date_found:
                    posts_date_dict[post["date"]] = 1

        if len(posts_date_dict) > 1:
            #print("{} has {} posts.".format(place["name"],len(posts_date_dict)))
            for post_date, post_count in posts_date_dict.items():
                #print("{} has {} photos on {}.".format(place["name"], post_count, post_date))
                if post_count > 9:
                    print("{} has {} posts.".format(place["name"],len(posts_date_dict)))
                    print("{} has {} photos on {}.".format(place["name"], post_count, post_date))

        if len(place["posts"]) > 10:
            posts_more_than_10_count = posts_more_than_10_count + 1
            #print(place["name"])
    print("total_count = {}".format(total_place_count))
    print("posts_more_than_10_count = {}".format(posts_more_than_10_count))
#


# IMPORTANT VARIABLES HOW DOES ONE PYTHON IDK
# Testing stuff
print_debug = True
single_record = True
record_index = 8
photos_debug_limit_to_one = True
dayone_write = False
# Options
photo_path = "/Users/mark/Dropbox/Apps/Rego/photos/"
rego_path = "../../rego.json"
#


# INT MAIN() LOL
data = json.load(codecs.open(rego_path, 'r', 'utf-8-sig'))
#if print_debug: pprint(data["places"][record_index])

#For testing
if single_record:
    tmp = []
    tmp.append(data["places"][record_index])
    data["places"].clear
    data["places"] = tmp
if print_debug: print("\n")
if print_debug: pprint(data["places"])

for place in data["places"]:
    #create a list of dayone entries needed per place, one per day based on number of posts,
    #first iso date kept. if no posts, just have 1 entry with the place created date.
    posts_date_list = get_post_day_list(place["posts"])
    if not posts_date_list:
        posts_date_list.append(place["createdAt"])

    if print_debug: print("FIXED Days in this place: {}".format(posts_date_list))

    #for each day, prepare a dayone cli command
    for day in posts_date_list:
        #date
        dayone_iso_date = day

        #tag
        dayone_tag = get_tag_name(place["pinColor"])

        #coords
        dayone_coords = str(place["latitude"]) + " " + str(place["longitude"])

        #start gathering info for text
        dayone_text = place["name"]
        if "venueID" in place:
            dayone_text += "\n" + "https://foursquare.com/v/" + place["venueID"]
        if place["notes"]:
            dayone_text += "\n" + place["notes"]

        #itterate through posts, set text & photo
        dayone_photos = ""
        for post in place["posts"]:
            if get_date_only(post["date"]) == get_date_only(day):
                if "note" in post:
                    dayone_text += "\n" + post["note"]
                if "filename" in post:
                    dayone_photos += get_full_photo_path(post["filename"]) + " "

        if print_debug: print("dayone_text = {}".format(dayone_text))
        if print_debug: print("dayone_iso_date = {}".format(dayone_iso_date))
        if print_debug: print("dayone_photos = {}".format(dayone_photos))
        if print_debug: print("dayone_tag = {}".format(dayone_tag))
        if print_debug: print("dayone_coords = {}".format(dayone_coords))

        #format this for the dayone2 cli
        dayone_formatted_list = format_for_dayone(dayone_text, dayone_iso_date, dayone_photos,
                                                  dayone_tag, dayone_coords)
        print(dayone_formatted_list)

        if print_debug: print("\n")

        if dayone_write: write_to_dayone(dayone_formatted_list)
