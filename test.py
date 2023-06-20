import praw

reddit = praw.Reddit(client_id='9vtPQwf5FxXRHAUMJT3Eiw',
                     client_secret='vbGauf8kKjTSCHVyL1BWzjdoxdyNGA',
                     username='ApprehensivePrize236 ',
                     password='1912010918',
                     user_agent='HiroBot1.0')

subreddit = reddit.subreddit('worldnews')
for submission in subreddit.search('paracetamol'):
    print(submission.title)
    print(submission.url)