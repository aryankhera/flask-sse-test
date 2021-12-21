from networkGraph import NetworkGraph

ng=NetworkGraph()
subredditGenerator=ng.get_subreddit_node_generator('TeamFightTactics')
print(next(subredditGenerator))
print(next(subredditGenerator))
print(next(subredditGenerator))
