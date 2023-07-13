# flask --app api.py run --debug --port 10451
# or just python3 api.py
from flask import Flask

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'You want path: %s' % path

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=10451)
