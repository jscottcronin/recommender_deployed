import numpy as np
from lightfm import LightFM
from sklearn.metrics.pairwise import cosine_similarity


class FM:
    def __init__(self, fm_model, preprocessor=None):
        self.model = fm_model
        self.pop_model = None
        self.movie_likes = None
        self.similar_items = None

        self.train_interactions = None
        self.no_customers = None
        self.no_items = None

        if preprocessor is not None:
            # user id <==> user index
            self.uid_to_idx = preprocessor.uid_to_idx
            self.idx_to_uid = {v: int(k) for k,v in self.uid_to_idx.items()}

            # item id <==> item index
            self.iid_to_idx = preprocessor.iid_to_idx
            self.idx_to_iid = {v: int(k) for k,v in self.iid_to_idx.items()}

    def fit(self, interactions, **kwargs):
        self.train_interactions = interactions
        self.no_customers = interactions.shape[0]
        self.no_items = interactions.shape[1]

        # Fit Personalized Model
        self.model.fit(interactions, **kwargs)
        self.similar_items = self._calculate_similar_items()

        # Fit Popularity Model
        self.movie_likes = np.array(interactions.sum(axis=0)).ravel()
        self.pop_model = np.argsort(-self.movie_likes)

    def predict_personalized(self, user_id, n_rec=10):
        assert user_id in self.uid_to_idx

        user_idx = self.uid_to_idx[user_id]
        movies_liked = self.train_interactions.getrow(user_idx).nonzero()[1]
        all_movies = np.arange(self.no_items)
        mask = np.isin(all_movies, movies_liked)
        unseen_movies = all_movies[~mask]

        scores = self.model.predict(
            user_ids=[user_idx],
            item_ids=unseen_movies,
            item_features=None,
            user_features=None,
            num_threads=1
            )
        idx_recs = np.argsort(-scores)[:n_rec]
        recs = [self.idx_to_iid[idx] for idx in idx_recs]
        return recs

    def predict_popularity(self, n_rec=10):
        idx_recs = self.pop_model[:n_rec]
        recs = [self.idx_to_iid[idx] for idx in idx_recs]
        return recs

    def get_historical_likes(self, user_id, n):
        user_idx = self.uid_to_idx[user_id]
        movies_liked = self.train_interactions.getrow(user_idx).nonzero()[1]
        freq = self.movie_likes[movies_liked]
        freq = freq / freq.sum()
        np.random.seed(seed=40)
        sampled_likes = np.random.choice(movies_liked,
                                        size=len(movies_liked),
                                        replace=False,
                                        p=freq)[:n]
        movie_ids = [self.idx_to_iid[idx] for idx in sampled_likes]
        return movie_ids

    def get_most_similar_items(self, item_id, n):
        item_idx = self.iid_to_idx[item_id]
        sim_idxs = self.similar_items[item_idx, :n]
        sim_iids = [self.idx_to_iid[idx] for idx in sim_idxs]
        return sim_iids


    def _calculate_similar_items(self):
        cs = cosine_similarity(self.model.item_embeddings)
        sims = np.argsort(-cs)[:, :100]
        return sims
