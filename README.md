# Reddit Vocab

## Description

A python project that aims to analyze lexical diversity of Reddit comment sections. Measure of lexical textual diversity (MTLD) as described by McCarthy and Jarvis (2010) is used. The average sentence length of each comment is also calculated. Currently, the script analyzes top comments of top yearly posts in the following subreddits:

- askreddit
- askhistorians
- philosophy
- news
- funny
- animalcrossing
- aww

The analysis of each subreddit's comments is stopped once 20,000 tokens is reached.

The resulting data is formated as JSON, and stored in the ./data subdirectory as a .txt file.
Feel Free to modify the subreddits you want to analyze.

## How to run

Run vocab.py after downloading the repo.

## Visualization

To see a graphical representation of the resulting data, visit this [link](https://friendly-meitner-bad372.netlify.app/).
GitHub repo for the linked static site can be found [here](https://github.com/moa-novae/reddit_vocab_static).
