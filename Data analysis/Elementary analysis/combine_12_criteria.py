"""
Apply all three criteria on the original data.
1. Coordinates criterion
2. Follow criterion
3. RT criterion with content analysis
Based on the coord_fixed.json which is the file to store all the users satisfy the coordinate criterion,
filter the suspect bot under follower criterion, which means too many followers but few followees.
Then filter the users with too many RT based on the user list under above criteria.
Lastly, analyse the RT content and find top 10 popular words.

* If there is no bots under two criteria/three criteria, it turns to do other tasks.
* Unfortunately, all tweets with coordinates do not contain 'RT' or 'RT @XXXXXXX'.
So they cannot be applied RT criterion and RT content analysis.
"""


import follow_criterion as follow_cr


if __name__ == "__main__":
    # Second criterion: followers/followees
    with open('/vol1/coord_fixed.json') as f1:
        with open('/vol1/coord_follow_criterion.json', 'w+') as f2:
            follow_cr.follow(f1, f2)
        f2.close()
    f1.close()
    print("Follow criterion task done!")

