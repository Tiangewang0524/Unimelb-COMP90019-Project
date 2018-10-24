"""
Filter the suspect bot under follower criterion, which means too many followers but few followees.
"""

import json


def follow(read_file, write_file):
    count_bot = 0
    write_file.write('{"suspect_bot_list":[\n')
    for each_row in read_file:
        try:
            info = json.loads(each_row[:-2])
            # Not only the rate but also the number of followers and followees
            # Some users do follow huge number of other Twitter users
            # and have a normal number of followers although the rate less than 0.1
            # Some users are just Twitter noobs and they don't have too many followees
            # so filter them
            if int(info["followers"]) / int(info["followees"]) < 0.1:
                if int(info["followers"]) < 300 and int(info["followees"]) > 100:
                    each = json.dumps(info)
                    write_file.write(each + ',' + '\n')
                    count_bot += 1
                    print("Suspect user: " + info["user_name"] + "has been counted")
        except:
            continue
    if count_bot == 0:
        write_file.seek(write_file.tell() - 1)
    else:
        write_file.seek(write_file.tell() - 2)
    write_file.write('],\n')
    write_file.write('"total_users":' + str(count_bot) + '}')
    print("Task Done!")
    print("Total suspect bots under follower criterion:" + str(count_bot))


if __name__ == "__main__":
    with open('/vol1/active_user.json') as f1:
        with open('/vol1/follow_criterion.json', 'w+') as f2:
            follow(f1, f2)
        f2.close()
    f1.close()
