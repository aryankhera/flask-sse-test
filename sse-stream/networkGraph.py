import praw
from config import CLIENT_SECRET,CLIENT_ID,LIMIT


class NetworkGraph:
    def __init__(self):
        self.reddit = praw.Reddit(
            user_agent="Comment Extraction (by u/USERNAME)",
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            username="",
            password="",
        )        
        self.subreddits=set()
        self.users_most_active_subreddits=set()

    def get_subreddit_node_generator(self,start_subreddit):
        top10redditors=[submission.author for submission in self.reddit.subreddit(start_subreddit).hot(limit=LIMIT)]
        for author in top10redditors:
            for comment in author.submissions.new(limit=LIMIT):
                subreddit_name=comment.subreddit.display_name
                if subreddit_name not in self.users_most_active_subreddits and subreddit_name.lower() != start_subreddit.lower() and subreddit_name not in self.subreddits:
                    print(subreddit_name)
                    yield subreddit_name
                self.users_most_active_subreddits.add(subreddit_name)
            self.subreddits.union(self.users_most_active_subreddits)
            self.users_most_active_subreddits.clear()
        yield 'finished'