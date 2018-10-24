"""
Filter all the RT text in the original data and group by the user_id through dictionary
to decrease the time for traverse.
"""


import json


def RT_filter (read_file, write_file):
    write_file.write('{"Rows":\n')
    # Use the dict to store all the RT content for each user
    # The format
    # {"user_id":{"tweet_id": "RT @DDDDD:XXXXXX","tweet_id": "RT @DFEFE:XXXXXX"}}
    user_dict = dict()
    count_RT = 0
    for each_row in read_file:
        try:
            item = json.loads(each_row[:-2])
            RT_id = item["tweet_id"]
            if item["user_id"] not in user_dict.keys():
                user_dict[item["user_id"]] = dict()
            if item["post_text"][0] == 'R' and item["post_text"][1] == 'T' and item["post_text"][3] == '@':
                user_dict[item["user_id"]][RT_id] = item["post_text"]
                count_RT += 1
                print("The RT content:\n" + item["post_text"] + "\nhas been counted")
        except:
            continue
    json.dump(user_dict, write_file)
    write_file.write(',\n')
    write_file.write('"total_RT":' + str(count_RT) + '}')
    print("Task Done!")


if __name__ == "__main__":
    with open('/vol1/o0Combine/o0ComData3.json') as f1:
        with open('/vol1/post_with_RT.json', 'w+') as f2:
            RT_filter(f1, f2)
        f2.close()
    f1.close()