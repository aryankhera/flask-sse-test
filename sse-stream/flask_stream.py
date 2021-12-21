from flask import Flask, render_template
from networkGraph import NetworkGraph

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://some-redis"

ng=NetworkGraph()

@app.route('/')
def index():
    return render_template('flask_stream.html')

@app.route('/flask_stream/<start_subreddit>')
def flask_stream(start_subreddit):
    print(f"Flask Stream called with: {start_subreddit}")
    subredditGenerator=ng.get_subreddit_node_generator(start_subreddit)
    return app.response_class(subredditGenerator, mimetype='text/event-stream')

if __name__=='__main__':
    app.run(threaded=True)