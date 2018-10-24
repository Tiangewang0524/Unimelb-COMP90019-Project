"""
Filter the suspect bot under RT&Tweet criterion, which means too many retweets from others
but few tweets posted forwardly by itself.
RT > 300
T < 100
To filter the normal users.
Then it can pick up the detailed RT content of suspect bots from the original tweet data.
"""

import json
import time


count_criterion_1 = 300
count_criterion_2 = 100
# Use a dictionary to count the number of retweets and tweets for each user
def tweet_num_count(read_file_1, read_file_2, write_file):
    # Store the user with RT numbers and T numbers in user_dict
    user_dict = dict()
    count_bot = 0
    write_file.write('{"user_list":\n')
    for each_row in read_file_1:
        try:
            item = json.loads(each_row[:-2])
            if item["user_id"] not in user_dict.keys():
                user_dict[item["user_id"]] = dict()
                user_dict[item["user_id"]]["RT_num"] = 0
                user_dict[item["user_id"]]["T_num"] = 0
                if item["post_text"][0] == 'R' and item["post_text"][1] == 'T' and item["post_text"][3] == '@':
                    user_dict[item["user_id"]]["RT_num"] = 1
                else:
                    user_dict[item["user_id"]]["T_num"] = 1
            else:
                if item["post_text"][0] == 'R' and item["post_text"][1] == 'T' and item["post_text"][3] == '@':
                    user_dict[item["user_id"]]["RT_num"] += 1
                else:
                    user_dict[item["user_id"]]["T_num"] += 1
            print("The RT&T numbers for user: " + str(item["user_id"]) + " " + "has been counted")
        except:
            continue
    json.dump(user_dict, write_file)
    write_file.write(',\n')
    write_file.write('"suspect_bot_list":\n')
    # find the users with RT number >> T number in (active/follow_criterion) user list.
    user_list = json.load(read_file_2)
    first_key = list(user_list.keys())[0]
    num_dict = dict()
    for each_record in user_list[first_key]:
        user_id = each_record["user_id"]
        if int(user_dict[user_id]["RT_num"]) > count_criterion_1 \
                and int(user_dict[user_id]["T_num"]) < count_criterion_2:
            if int(user_dict[user_id]["T_num"])/int(user_dict[user_id]["RT_num"]) < 0.1:
                num_dict[user_id] = user_dict[user_id]
                count_bot += 1
    json.dump(num_dict, write_file)
    write_file.write(',\n')
    write_file.write('"total_users":' + str(count_bot) + '}')
    print("Task Done!")
    print("Total suspect bots under RT criterion:" + str(count_bot))


# Pick up RT content
def RT(read_file_1, read_file_2, write_file):
    count_RT = 0
    write_file.write('{"suspect_bot_RT_list":\n')
    user_list = json.load(read_file_2)
    # second_key = "suspect_bot_list"
    second_key = list(user_list.keys())[1]
    num_list = dict()
    num_list = user_list[second_key]
    user_list = dict()
    # pick up the dict which stores all the RT content from the original data and save as 'item'
    for each_row in read_file_1:
        try:
            item = json.loads(each_row[:-2])
        except:
            continue
    for each_bot_id in num_list.keys():
        # format:
        # dict{dict}
        # {"bot_id":{"post_text": "RT @DDDDD:XXXXXX"},{"post_text": "RT @DFEFE:XXXXXX"}}
        for each_key in item.keys():
            if each_key == each_bot_id:
                user_list[each_bot_id] = dict()
                user_list[each_bot_id] = item[each_key]
                print("Suspect user:" + " " + str(each_key) + "'s all RT content has been counted")
                count_RT += len(item[each_key].items())
                # When sub_task finished, delete this pair key-value to decrease the time for traverse
                del item[each_key]
                break
    json.dump(user_list, write_file)
    write_file.write(',\n')
    write_file.write('"total_suspect_RT":' + str(count_RT) + '}')
    print("Task Done!")
    print("Total RT number of suspect bots :" + str(count_RT))


if __name__ == "__main__":
    with open('/vol1/o0Combine/o0ComData3.json') as f1:
        with open('/vol1/active_user.json') as f2:
            with open('/vol1/RT_count.json', 'w+') as f3:
                tweet_num_count(f1, f2, f3)
            f3.close()
        f2.close()
    f1.close()
    time.sleep(5)
    # Read the RT post file instead of the original data
    with open('/vol1/post_with_RT.json') as f1:
        with open('/vol1/RT_count.json') as f2:
            with open('/vol1/RT_content.json', 'w+') as f3:
                RT(f1, f2, f3)
            f3.close()
        f2.close()
    f1.close()

