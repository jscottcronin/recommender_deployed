from lightfm import LightFM


class FM(object):
    def __init__(self, preprocessor, fm_model):

        self.model = fm_model
        self.train_interactions = None

        if preprocessor is not None:
            self.uid_to_idx = preprocessor.uid_to_idx
            self.iid_to_idx = preprocessor.iid_to_idx


    def fit(self, interactions, lightfm_fit_kwargs):
        self.train_interactions = interactions
        self.model.fit(interactions, lightfm_fit_kwargs)


    def predict(self):
        return self.attr
