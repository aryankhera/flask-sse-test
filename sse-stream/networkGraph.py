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
                    print(f"{start_subreddit} -> {subreddit_name}")
                    yield f"{start_subreddit} -> {subreddit_name}"
                self.users_most_active_subreddits.add(subreddit_name)
            self.subreddits=self.subreddits.union(self.users_most_active_subreddits)
            self.users_most_active_subreddits.clear()
        yield 'finished'

    @classmethod
    def get_next_subrredit_node(cls,self,start,level,visited_subreddit):
        print(f'{start} {level}')
        if level!=LIMIT:
            subreddits=set()
            most_active_sr=set()
            top10redditors=[submission.author for submission in self.reddit.subreddit(start).hot(limit=LIMIT)]
            for author in top10redditors:
                try:
                    if author is not None:
                        for comment in author.submissions.new(limit=LIMIT):
                            subreddit_name=comment.subreddit.display_name
                            if subreddit_name.lower() != start.lower():
                                print(f"{start} -> {subreddit_name}")
                                yield f"{start} -> {subreddit_name}"
                            most_active_sr.add(subreddit_name)
                        subreddits=subreddits.union(most_active_sr)
                        most_active_sr.clear()
                        visited_subreddit.add(start)
                except:
                    continue
            for sr in subreddits:
                if sr not in visited_subreddit:
                    yield from NetworkGraph.get_next_subrredit_node(NetworkGraph(),sr,level+1,visited_subreddit)
            

