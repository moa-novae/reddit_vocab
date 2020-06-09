import praw
reddit = praw.Reddit('personal')
AskHistorians = reddit.subreddit('AskHistorians')
for index, submission in enumerate(AskHistorians.top('all', limit=1)):
    top_level_comments = list(submission.comments)
    for comment in top_level_comments:
        if isinstance(comment, praw.models.MoreComments):
            continue
        if (comment.body != '[removed]'):
            print(comment.body)
