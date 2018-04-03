import numpy as np
import pandas as pd
import scipy.sparse as scs
from sklearn.base import TransformerMixin


class Preprocessor(TransformerMixin):
    def __init__(self, copy=True, min_rating=4.0):
        self.copy = copy
        self.min_rating = min_rating
        self.uid_to_idx = None
        self.iid_to_idx = None

    def fit(self, df, y=None, **kwargs):
        self._validate_df(df)
        if self.copy:
            df = df.copy()
        df = self._filter_interactions_to_min_rating(df)
        df = self._drop_duplicate_user_item_interactions(df)

        # create uid to indx mapping
        uniq_uids = df['uid'].unique()
        self.uid_to_idx = dict(zip(uniq_uids, np.arange(len(uniq_uids))))

        # create iid to indx mapping
        uniq_iids = df['iid'].unique()
        self.iid_to_idx = dict(zip(uniq_iids, np.arange(len(uniq_iids))))
        return self

    def transform(self, df, **kwargs):
        self._validate_df(df)
        if self.copy:
            df = df.copy()

        df = self._filter_interactions_to_min_rating(df)
        df = self._drop_duplicate_user_item_interactions(df)

        # generate sparse matrix
        row = df['uid'].map(self.uid_to_idx)
        col = df['iid'].map(self.iid_to_idx)
        assert len(row) == len(col)
        data = np.ones(len(row))
        shape = (len(self.uid_to_idx), len(self.iid_to_idx))
        csr = scs.coo_matrix((data, (row, col)), shape=shape).tocsr()
        return csr

    def _drop_duplicate_user_item_interactions(self, df):
        if df.duplicated().sum() != 0:
            df = df.drop_duplicated()
        return df

    def _filter_interactions_to_min_rating(self, df):
        df = df.loc[df['rating'] >= self.min_rating, ['uid', 'iid']]
        return df

    def _validate_df(self, df):
        assert 'uid' in df.columns
        assert 'iid' in df.columns
        assert 'rating' in df.columns
