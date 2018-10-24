"""
Filter all the tweets with coordinates in the original data
and store all the infomation.
"""


import json


def coord_filter(read_file, write_file):
    write_file.write('"Rows":[\n')
    count_coord = 0
    for each_row in read_file:
        try:
            item = json.loads(each_row[:-2])
            # There is a type issue when save the original data. That is we have 'item["coodinates"]'
            # rather than 'item["coordinates"]'
            if item["coodinates"]["type"] == "Point" and item["coodinates"]["coordinates"]:
                json.dump(item, write_file)
                write_file.write(',' + '\n')
                count_coord += 1
                print("The tweet with coordinate:\n"
                      + item["post_text"] +
                      "\nhas been counted")
        except:
            continue
    write_file.seek(write_file.tell() - 2)
    write_file.write(']}')
    write_file.seek(0, 0)
    content = write_file.read()
    write_file.seek(0, 0)
    write_file.write('{"total_tweets_with_coordinates":' + str(count_coord) + ',' + content)
    print("Task Done!")


if __name__ == "__main__":
    with open('/vol1/o0Combine/o0ComData3.json') as f1:
        with open('/vol1/post_with_coordinate.json', 'w+') as f2:
            coord_filter(f1, f2)
        f2.close()
    f1.close()
