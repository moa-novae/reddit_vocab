import praw
import mtld
import json
import time
import spacy
import os
import timeit
nlp = spacy.load('en_core_web_sm')
reddit = praw.Reddit('personal')
# Change subreddits to whatever ones you want to analyze
subreddits = ('askreddit', 'askhistorians', 'philosophy', 'news', 'funny',
              'animalcrossing', 'aww')


class subreddit_analysis(mtld.lexical_analysis):
    nlp = spacy.load('en_core_web_sm')
    reddit = praw.Reddit('personal')

    def __init__(self, subreddit):
        self.subreddit = subreddit
        self.comment_str = self.fetch_subreddit_comments()
        # generate spaCy Doc
        self.doc = subreddit_analysis.nlp(self.comment_str)

    # Concat top comments from top 10 posts of all time
    def fetch_subreddit_comments(self):
        subreddit_inst = reddit.subreddit(self.subreddit)
        comment_str = ''
        for i, submission in enumerate(subreddit_inst.top('year')):
            top_level_comments = list(submission.comments)
            for index, comment in enumerate(top_level_comments):
                # do not concat if comment says More Comments
                if isinstance(comment, praw.models.MoreComments):
                    continue
                # do not concat if comment removed
                if (comment.body != '[removed]'):
                    comment_str = comment_str + comment.body
                    # add period if comment does not end with one
                    if (comment.body[-1] != '.'):
                        comment_str = comment_str + '.'
                if (index % 20 == 0):
                    # check doc length every 20 comments
                    if (len(subreddit_analysis.nlp(comment_str)) > 20000):
                        print(len(subreddit_analysis.nlp(comment_str)))
                        return comment_str


def save_subreddit_analysis(subreddits):
    output_json = {}
    output_dir = 'data'
    timestr = time.strftime("%Y%m%d-%H%M%S")
    fileName = timestr + '-data.txt'
    file_path = os.path.join(output_dir, fileName)
    for subreddit in subreddits:
        start = timeit.default_timer()
        result = subreddit_analysis(subreddit)
        output_json[subreddit] = {
            "mtld": result.mtld,
            "avg_sentence_length": result.avg_sentence_length
            }
        stop = timeit.default_timer()
        print(subreddit, ' took ', stop - start)
    # Generate data subdirrector if it does not exist
    try:
        os.mkdir(output_dir)
    except Exception:
        pass
    # Save generated output JSON to ./data
    with open(file_path, 'w') as outfile:
        json.dump(output_json, outfile, indent=4)


save_subreddit_analysis(subreddits)
