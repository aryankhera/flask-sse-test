from flask import Flask, render_template
from flask_sse import sse
from networkGraph import NetworkGraph
from config import START_SUBREDDIT

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://some-redis"
app.register_blueprint(sse, url_prefix='/stream')
    
ng=NetworkGraph()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello/<start_subreddit>')
def publish_hello(start_subreddit):
    print(f"hello called with: {start_subreddit}")
    subredditGenerator=ng.get_subreddit_node_generator(start_subreddit)
    while True:
        try:
            sse.publish({"message": next(subredditGenerator)}, type='greeting')
        except StopIteration:
            print('Generator Exhausted')
            break
    return "Message sent!"
