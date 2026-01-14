#!/usr/bin/env python3
import pandas as pd
import numpy as np
import os


def normalize(df, criteria, benefit):
    norm = df.copy()
    for c in criteria:
        col = df[c].astype(float)
        mn = col.min()
        mx = col.max()
        if mx == mn:
            norm[c] = 1.0
        else:
            if benefit.get(c, True):
                norm[c] = (col - mn) / (mx - mn)
            else:
                norm[c] = (mx - col) / (mx - mn)
    return norm


def maut(df, criteria, weights, benefit):
    norm = normalize(df, criteria, benefit)
    w = np.array([weights[c] for c in criteria])
    scores = (norm[criteria].to_numpy(dtype=float) * w).sum(axis=1)
    df_result = df.copy()
    df_result['Score'] = scores
    df_result = df_result.sort_values('Score', ascending=False).reset_index(drop=True)
    return df_result


def print_ranking(df_result, display_cols=None):
    if display_cols is None:
        display_cols = list(df_result.columns)
    print('\nHasil perankingan (Score tertinggi ke terendah):\n')
    print(df_result[display_cols].to_string(index=False))


def demo():
    here = os.path.dirname(__file__)
    data_path = os.path.join(here, '..', 'data', 'alternatives.csv')
    df = pd.read_csv(data_path)

    criteria = ['Price', 'Duration', 'Facilities', 'Destination', 'Rating']

    # Bobot contoh (harus dijumlahkan = 1)
    weights = {
        'Price': 0.25,
        'Duration': 0.15,
        'Facilities': 0.2,
        'Destination': 0.2,
        'Rating': 0.2,
    }

    # Tipe kriteria: True = benefit (semakin besar semakin baik), False = cost (semakin kecil lebih baik)
    benefit = {
        'Price': False,
        'Duration': False,
        'Facilities': True,
        'Destination': True,
        'Rating': True,
    }

    result = maut(df, criteria, weights, benefit)
    print_ranking(result, display_cols=['Alternative'] + criteria + ['Score'])


if __name__ == '__main__':
    demo()
