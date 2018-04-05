from flask import Flask, render_template, request, jsonify, abort
import json
import numpy as np
from sklearn.externals import joblib

with open('app/objects/user_profiles.json', 'r') as f:
    USER_PROFILES = json.load(f)
POSTERS = joblib.load('app/objects/posters.pkl.gz')
MODEL = joblib.load('app/objects/fm.pkl.gz')
BASE_URL = 'https://image.tmdb.org/t/p/w200'

app = Flask(__name__)

@app.route('/recommender')
def recommender():
    users = np.random.choice(list(USER_PROFILES), size=36, replace=False)
    profiles = [(int(user), USER_PROFILES[user]) for user in users]
    return render_template('recommender.html', profiles=profiles)
#
@app.route('/rec_predict', methods=['POST'])
def rec_predict():
    payload = request.get_json()
    user_id = payload['user_id']
    n_rec = payload['n_rec']

    if payload['execute_popularity'] == True:
        recs =  MODEL.predict_popularity(n_rec)
        model_name = 'popularity'

    elif payload['execute_popularity'] == False:
        recs =  MODEL.predict_personalized(user_id, n_rec)
        model_name = 'personalized'
    else:
        raise KeyError('execute_popularity is a required key in POST payload')

    poster_urls = [BASE_URL + POSTERS[iid] for iid in recs]

    output = {
        'user_id': user_id,
        'recs': recs,
        'posters': poster_urls,
        'model_name': model_name
    }
    return jsonify(output)



@app.route('/get_historical_likes', methods=['POST'])
def get_historical_likes():
    payload = request.get_json()
    user_id = payload['user_id']
    n = payload['n']

    user_likes =  MODEL.get_historical_likes(user_id, n)
    poster_urls = [BASE_URL + POSTERS[iid] for iid in user_likes]

    output = {
        'user_id': user_id,
        'user_likes': user_likes,
        'posters': poster_urls
    }
    return jsonify(output)
