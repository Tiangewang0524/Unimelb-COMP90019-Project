"""
The analysis for the RT content of the suspect bots and active RT users.
Pick up top 10 popular words from the content.
"""

import json
# Common words in English which interfere the result
irrelevant_list = ["on", "in", "to", "till", "until", "at", "before", "past", "since", "for", "ago", "is", "the",
                   "are", "was", "were", "a", "next", "beside", "over", "under", "above", "across", "into", "towards",
                   "onto", "from", "of", "off", "about", "out", "outside", "inside", "I", "you", "he", "she", "they",
                   "me", "him", "her", "them", "been", "have", "do", "did", "done", "had", "not", "and", "this",
                   "that", "i", "it", "with", "be", "within", "as", "we", "our", "if", "so", "-", "has", "its",
                   "will", "an", "just", "my", "who", "your", "his", "their", "oh", "wow", "ah", "mine", "yours",
                   "ours", "what", "which", "where", "but", "no", "how", "when", "no", "all", "people", "more", "up",
                   "down", "can", "could", "should", "must", "may", "maybe", "one", "it's", "i'm", "like", "now",
                   "two", "three", "four", "five", "first", "second", "third", "very", "much", "get", "new", "or",
                   "why", "any", "by"]


def RT_analysis(read_file, write_file):
    frequency = dict()
    list_a = []
    count_a = 0
    dict_a = dict()
    write_file.write('{"top_10_words":\n')
    # Pick up the dict which stores all the RT content
    # of the suspect bots and active RT users and save as 'item'
    for each_row in read_file:
        try:
            item = json.loads(each_row[:-2])
        except:
            continue
    for sub_dict in item.values():
        for each_value in sub_dict.values():
            # Delete the 'RT' and '@'
            text = each_value[3:]
            for each_word in text.split():
                each_word = each_word.lower()
                if each_word not in frequency:
                    frequency[each_word] = 1
                else:
                    frequency[each_word] += 1
    list_a = sorted(frequency.items(), key=lambda item: item[1], reverse=True)
    for each in list_a:
        # each[0] is the word, each[1] is the frequency
        if each[0] not in irrelevant_list:
            dict_a[each[0]] = each[1]
            count_a += 1
            if count_a == 10:
                break
    json.dump(dict_a, write_file)
    write_file.write(',\n')
    # Store top 10 words with '@'
    write_file.write('"top_10_words with @":\n')
    dict_a = dict()
    count_a = 0
    for each in list_a:
        # each[0] is the word, each[1] is the frequency
        if "@" in each[0]:
            dict_a[each[0]] = each[1]
            count_a += 1
            if count_a == 10:
                break
    json.dump(dict_a, write_file)
    write_file.write(',\n')
    # Store top 10 words with '#'
    write_file.write('"top_10_words with #":\n')
    dict_a = dict()
    count_a = 0
    for each in list_a:
        # each[0] is the word, each[1] is the frequency
        if "#" in each[0]:
            dict_a[each[0]] = each[1]
            count_a += 1
            if count_a == 10:
                break
    json.dump(dict_a, write_file)
    write_file.write('}')
    print("Task Done!")


if __name__ == "__main__":
    with open('/vol1/RT_content.json') as f1:
        with open('/vol1/RT_analysis.json', 'w+') as f2:
            RT_analysis(f1, f2)
        f2.close()
    f1.close()