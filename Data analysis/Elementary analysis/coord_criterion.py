"""
Filter the suspect bot under coordinate criterion, which means that the user always
post tweets in the same location.
The judgement method will be:
1. Read the coordinates from the filtered data
2. Supposed that we have three pairs of coordinates for one user like
[144.97601509, -37.84839197], [144.99783, -37.90971] & [144.9639504, -37.8749242]
3. Use the maths function 'haversine' to calculate the actual distance for them (unit: metre)
e.g. distance of (coord1 - coord2) = 5 (m)
distance of (coord2 - coord3) = 3 (m)
Then we can say this user moved 5+3 = 8 (m) to post these three tweets.
4. Consider the GPS error for each devices, this user can be regarded as the bot
since the move distance is too short, even shorter than the length and width of a room.
5. We took the width of the EDS3 of old engineering as the example (5 m).
We assumed that the if a moving user posts two tweets, the distance of his two posts should
be more than 5 (m) to avoid be identified as a bot user the fixed computer in a building.
6. If this user posted many tweets, the total distance of them should be bigger than 5 * i
where i is the times, that is number of tweets minus 1.
7. Any total distance of all his posts with coordinates less than 100 * i will be considered as the bot.
* Post at least 10 tweets should be considered to filter the noobs.
"""


import json
from math import radians, cos, sin, asin, sqrt

coord_ratio = 5
tweet_number_criterion = 10


# Calculate the great circle distance between two points on the earth (specified in decimal degrees)
def haversine(lon1, lat1, lon2, lat2):  # Longitude 1, latitude 1, longitude 2, latitude 2 (decimal)
    # Convert decimal to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # The formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # The earth's average radius in kilometers
    return c * r * 1000


def coord_criterion(read_file, write_file_1, write_file_2):
    # Find the users with short move distance and saved in coord_criterion.json.
    # Find the users with 0 move distance and saved in coord_fixed.json.
    count_bot = 0
    count_key_bot = 0
    write_file_1.write('{"suspect_bot_coord_list":[\n')
    write_file_2.write('{"Key_suspect_bot_fixed_coord_list":[\n')
    # First, use the dict to store all the coordinates for each user
    # The format
    # {"user_id":{"tweet_id": "[lon1,lat1]","tweet_id": "[lon2,lat2]"}}
    user_dict = dict()
    for each_row in read_file:
        try:
            item = json.loads(each_row[:-2])
            coord_id = item["tweet_id"]
            if item["user_id"] not in user_dict.keys():
                user_dict[item["user_id"]] = dict()
            user_dict[item["user_id"]][coord_id] = item["coodinates"]["coordinates"]
            print("The coordinates for :\n" + item["tweet_id"] + " has been counted")
        except:
            continue
    for each_user in user_dict.keys():
        coord_pair = user_dict[each_user]
        list_a = list(coord_pair.values())
        total = 0
        # For a user, he/she posted at least 10 tweets with coordinates.
        if len(list_a) > tweet_number_criterion:
            for i in range(0, len(list_a) - 1):
                d = haversine(list_a[i][0], list_a[i][1], list_a[i+1][0], list_a[i+1][1])
                total += d
            if int(total) < coord_ratio*(len(list_a)-1):
                # Regard as a bot
                # Find the information for this user and store them in a new json file.
                read_file.seek(0, 0)
                for each_row in read_file:
                    try:
                        item = json.loads(each_row[:-2])
                        if each_user == item["user_id"]:
                            info = dict()
                            info["user_id"] = item["user_id"]
                            info["user_name"] = item["user_name"]
                            info["followers"] = item["followers"]
                            info["followees"] = item["followees"]
                            each = json.dumps(info)
                            write_file_1.write(each + ',' + '\n')
                            count_bot += 1
                            print("Suspect bot: " + info["user_name"] + "has been counted")
                            if int(total) == 0:
                                write_file_2.write(each + ',' + '\n')
                                count_key_bot += 1
                                print("Key suspect bot: " + info["user_name"] + "has been counted")
                            break
                    except:
                        continue
    if count_key_bot == 0:
        write_file_2.seek(write_file_2.tell() - 1)
    else:
        write_file_2.seek(write_file_2.tell() - 2)
    write_file_2.write('],\n')
    write_file_2.write('"total_users":' + str(count_key_bot) + '}')
    if count_bot == 0:
        write_file_1.seek(write_file_1.tell() - 1)
    else:
        write_file_1.seek(write_file_1.tell() - 2)
    write_file_1.write('],\n')
    write_file_1.write('"total_users":' + str(count_bot) + '}')
    print("Task Done!")
    print("Total suspect bots:" + str(count_bot))
    print("Total key suspect bots:" + str(count_key_bot))


if __name__ == "__main__":
    with open('/vol1/post_with_coordinate.json') as f1:
        with open('/vol1/coord_criterion.json', 'w+') as f2:
            with open('/vol1/coord_fixed.json', 'w+') as f3:
                coord_criterion(f1, f2, f3)
            f3.close()
        f2.close()
    f1.close()
