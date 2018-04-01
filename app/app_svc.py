from flask import Flask, render_template, request, jsonify, abort

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/rec_predict', methods=['POST'])
def rec_predict():
    payload = request.get_json()

    # recs = MODEL.predict(payload)
    recs = ['movie_1', 'movie2', 'movie3']
    output = {
        'user_id': 0,
        'recs': recs,
        }

    return jsonify(output)
