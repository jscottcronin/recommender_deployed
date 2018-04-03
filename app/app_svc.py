from flask import Flask, render_template, request, jsonify, abort
import json
import numpy as np

with open('app/objects/user_profiles.json', 'r') as f:
    USER_PROFILES = json.load(f)

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/recommender')
def recommender():
    sample_user_size = 30
    users = np.random.choice(list(USER_PROFILES), size=36, replace=False)
    profiles = [(int(user), USER_PROFILES[user]) for user in users]
    return render_template('recommender.html', profiles=profiles)

@app.route('/rec_predict', methods=['POST'])
def rec_predict():
    payload = request.get_json()

    # recs = MODEL.predict(payload)
    recs = ['movie_1', 'movie_2', 'movie_3']
    output = {
        'user_id': payload['user_id'],
        'recs': recs,
        }

    return jsonify(output)
