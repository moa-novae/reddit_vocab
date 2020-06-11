import praw
import mtld
import json
import time
import spacy
import os
nlp = spacy.load('en_core_web_sm')
reddit = praw.Reddit('personal')
subreddits = ('askreddit', 'askhistorians', 'philosophy', 'news', 'funny',
              'animalcrossing', 'aww')


class subreddit_analysis:
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
        for i, submission in enumerate(subreddit_inst.top('all', limit=10)):
            top_level_comments = list(submission.comments)
            for comment in top_level_comments:
                # do not concat if comment says More Comments
                if isinstance(comment, praw.models.MoreComments):
                    continue
                # do not concat if comment removed
                if (comment.body != '[removed]'):
                    comment_str = comment_str + comment.body
        return comment_str

    @property
    def avg_sentence_length(self):
        output = mtld.avg_sentence_length(self.doc)
        return output

    @property
    def mtld(self):
        # lemmatize each token for mtld calculation
        lemmatize = [token.lemma_ for token in self.doc]
        output = mtld.mtld(lemmatize)
        return output


output_json = {}
output_dir = 'data'
timestr = time.strftime("%Y%m%d-%H%M%S")
fileName = timestr + '-data.txt'
file_path = os.path.join(output_dir, fileName)
for subreddit in subreddits:
    result = subreddit_analysis(subreddit)
    output_json[subreddit] = {
        "mtld": result.mtld,
        "avg_sentence_length": result.avg_sentence_length
        }
# Generate data subdirrector if it does not exist
try:
    os.mkdir(output_dir)
except Exception:
    pass
# Save generated output JSON to ./data
with open(file_path, 'w') as outfile:
    json.dump(output_json, outfile, indent=4)
