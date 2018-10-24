"""
Find the active Twitter users in Melbourne in last 11 months and save the list to the json file.
The criterion is 300 tweets for active users in 11 months.
"""

import json

count_criterion = 300
count_active_user = 0
num_user = dict()
with open('/vol1/o0Combine/o0ComData3.json') as f1:
    with open('/vol1/active_user.json', 'w+') as f2:
        f2.write('{"active_user_list":[\n')
        for each_row in f1:
            # print(each_row)
            try:
                item = json.loads(each_row[:-2])
                if item["user_id"] not in num_user.keys():
                    num_user[item["user_id"]] = 1
                else:
                    num_user[item["user_id"]] += 1
                    # Only count once when the user is regarded as the 'active user' (reach the criterion)
                    if num_user[item["user_id"]] == count_criterion:
                        info = dict()
                        info["user_id"] = item["user_id"]
                        info["user_name"] = item["user_name"]
                        info["followers"] = item["followers"]
                        info["followees"] = item["followees"]
                        each = json.dumps(info)
                        f2.write(each + ',' + '\n')
                        count_active_user += 1
                        print("Active user: " + info["user_name"] + "has been counted")
            except:
                continue
        if count_active_user == 0:
            f2.seek(f2.tell() - 1)
        else:
            f2.seek(f2.tell()-2)
        f2.write('],\n')
        f2.write('"total_active_users":' + str(count_active_user) + ',\n')
        f2.write('"total_users":' + str(len(num_user)) + '}')
        print("Task Done!")
        print("Total active users:" + str(count_active_user))
        f2.close()
    f1.close()


