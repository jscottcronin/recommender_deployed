import sys
sys.path[0] = sys.path[0].rsplit('/', 1)[0]
from lightfm import LightFM
import numpy as np
import pandas as pd
from sklearn.externals import joblib
from app.preprocess import Preprocessor
from app.models import FM

if __name__ == '__main__':
    # Load data (this was downloaded from )
    interactions = pd.read_csv('data/ratings.dat',
                           sep='::', engine='python',
                           header=None,
                           names=['uid', 'iid', 'rating', 'timestamp'],
                           usecols=['uid', 'iid', 'rating'],
                          )
    # convert from datarame to scipy sparse matrix
    preprocessor = Preprocessor(min_rating=4.0)
    csr = preprocessor.fit_transform(interactions)

    # build personalized recommender
    lfm = LightFM(no_components=30, loss='warp', learning_rate=0.05)
    fm = FM(fm_model=lfm, preprocessor=preprocessor)
    fm.fit(csr, epochs=3)

    # Store serialized version of model
    joblib.dump(fm, 'app/objects/fm.pkl.gz')
