import pickle
import pandas as pd
import numpy as np
from pathlib import Path


def make_prediction(input: dict) -> float:
    model_path = './main_app/static/models/finalized_model.pkl'
    model = pickle.load(open(model_path, 'rb'))

    try:
        pred = np.exp(float(model.predict(pd.DataFrame(input, index=[0]))))
    except TypeError:
        pred = 0
    except ValueError:
        pred = 0
    return pred


def get_neighborhood_categorie() -> list:

    NEIGHBORHOOD_MAPPING = {
        'Blmngtn': 'Bloomington Heights',
        'Blueste': 'Bluestem',
        'BrDale': 'Briardale',
        'BrkSide': 'Brookside',
        'ClearCr': 'Clear Creek',
        'CollgCr': 'College Creek',
        'Crawfor': 'Crawford',
        'Edwards': 'Edwards',
        'Gilbert': 'Gilbert',
        'IDOTRR': 'Iowa DOT and Rail Road',
        'MeadowV': 'Meadow Village',
        'Mitchel': 'Mitchell',
        'Names': 'North Ames',
        'NoRidge': 'Northridge',
        'NPkVill': 'Northpark Villa',
        'NridgHt': 'Northridge Heights',
        'NWAmes': 'Northwest Ames',
        'OldTown': 'Old Town',
        'SWISU': 'South & West of Iowa State University',
        'Sawyer': 'Sawyer',
        'SawyerW': 'Sawyer West',
        'Somerst': 'Somerset',
        'StoneBr': 'Stone Brook',
        'Timber': 'Timberland',
        'Veenker': 'Veenker',
    }

    model_path = './main_app/static/models/finalized_model.pkl'
    model = pickle.load(open(model_path, 'rb'))
    categories = []
    for elt in model[:-1].get_feature_names_out():
        if "Neighborhood" in elt:
            code = elt.replace("cat__Neighborhood_", "")
            # Use the neighborhood name if it's in the mapping, or use the code
            name = NEIGHBORHOOD_MAPPING.get(code, code)
            categories.append((code, name))

    return categories


def get_foundation_categorie() -> list:

    FOUNDATION_MAPPING = {
        'BrkTil': 'Brick & Tile',
        'CBlock': 'Cinder Block',
        'PConc': 'Poured Concrete',
        'Slab': 'Slab',
        'Stone': 'Stone',
        'Wood': 'Wood',
    }

    model_path = './main_app/static/models/finalized_model.pkl'
    model = pickle.load(open(model_path, 'rb'))
    categories = []
    for elt in model[:-1].get_feature_names_out():
        if "Foundation" in elt:
            code = elt.replace("cat__Foundation_", "")
            # Use the neighborhood name if it's in the mapping, or use the code
            name = FOUNDATION_MAPPING.get(code, code)
            categories.append((code, name))

    return categories
