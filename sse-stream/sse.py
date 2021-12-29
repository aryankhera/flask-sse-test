from flask import Flask, render_template, request
from flask_sse import sse
from networkGraph import NetworkGraph
from config import START_SUBREDDIT
from flask_cors import CORS
# from gevent import monkey; monkey.patch_all()

app = Flask(__name__)
CORS(app)
app.config["REDIS_URL"] = "redis://some-redis"
app.register_blueprint(sse, url_prefix='/stream')
    
ng=NetworkGraph()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello/<start_subreddit>')
def publish_hello(start_subreddit):
    print(f"hello called with: {start_subreddit}")
    # subredditGenerator=ng.get_subreddit_node_generator(start_subreddit)
    subredditGenerator=ng.get_next_subrredit_node(ng,start_subreddit,0,set())
    while True:
        try:
            sse.publish({"message": next(subredditGenerator)}, type='greeting',channel=request.args["channel"])
            # print(f"{start_subreddit}---{request.args['channel']}")
        except StopIteration:
            print('Generator Exhausted')
            break
    return "Message sent!"
