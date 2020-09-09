import my_tweet_flow

test = 'PierreTermier2'
print(my_tweet_flow.get_total_tweet_flow(test))
contributors = my_tweet_flow.get_tweet_flow_contributors(test)
for user_id, screen_name, tph, percent, rt_ratio in contributors:
    print(screen_name + '\t\t\t\t', str(tph) + '\t\t', str(percent) + '\t\t', str(rt_ratio) + '\t\t')
