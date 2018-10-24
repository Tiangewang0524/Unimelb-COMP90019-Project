"""
Apply these two criteria on the original data without coordinates.
2. Follow criterion
3. RT criterion with content analysis
Based on the active_user.json which is the file to store all the active users,
filter the suspect bot under follower criterion, which means too many followers but few followees.
Then filter the users with too many RT based on the user list under above criteria.
Lastly, analyse the RT content and find top 10 popular words.

* If there is no bots under two criteria, it turns to do other tasks.
"""


import RT_criterion as RT_cr
import RT_content_analysis as RT_ana
import time


if __name__ == "__main__":
    # Third criterion: RT/tweet
    # First count the number of RT and tweet for each user in the follow_criterion suspect bot list
    # and find suspect bot under RT criterion.
    with open('/vol1/o0Combine/o0ComData3.json') as f1:
        with open('/vol1/follow_criterion.json') as f2:
            with open('/vol1/follow_RT_count.json', 'w+') as f3:
                RT_cr.tweet_num_count(f1, f2, f3)
            f3.close()
        f2.close()
    f1.close()
    print("RT criterion for follow_criterion suspect bot list done!")
    time.sleep(10)
    # Then filter all RT content for suspect bot above for RT content analysis.
    # Read the RT post file instead of the original data
    with open('/vol1/post_with_RT.json') as f1:
        with open('/vol1/follow_RT_count.json') as f2:
            with open('/vol1/follow_RT_content.json', 'w+') as f3:
                RT_cr.RT(f1, f2, f3)
            f3.close()
        f2.close()
    f1.close()
    print("RT content for follow_criterion suspect bot list done!")
    time.sleep(10)
    # Count the top 10 popular words for the RT content
    with open('/vol1/follow_RT_content.json') as f1:
        with open('/vol1/follow_RT_analysis.json', 'w+') as f2:
            RT_ana.RT_analysis(f1, f2)
        f2.close()
    f1.close()
    print("RT content analysis for follow_criterion suspect bot list done!")
    print("All tasks in Follow criterion + RT criterion done!")
