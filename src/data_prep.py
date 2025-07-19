import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def create_fraud_features(df):
    """
    Création des toutes les features pour détecter la fraude
    """
    df_new = df.copy()
    df_new['total_items'] = df_new['Nb_of_items'].fillna(0)
    price_cols = [f'cash_price{i}' for i in range(1, 25)]
    price_data = df_new[price_cols]
    df_new['total_price'] = price_data.sum(axis=1, skipna=True)
    df_new['avg_price'] = price_data.mean(axis=1, skipna=True)
    df_new['median_price'] = price_data.median(axis=1, skipna=True)
    df_new['std_price'] = price_data.std(axis=1, skipna=True).fillna(0)
    df_new['min_price'] = price_data.min(axis=1, skipna=True)
    df_new['max_price'] = price_data.max(axis=1, skipna=True)
    df_new['price_range'] = df_new['max_price'] - df_new['min_price']
    qty_cols = [f'Nbr_of_prod_purchas{i}' for i in range(1, 25)]
    qty_data = df_new[qty_cols]
    df_new['total_quantity'] = qty_data.sum(axis=1, skipna=True)
    df_new['avg_quantity'] = qty_data.mean(axis=1, skipna=True)
    df_new['max_quantity'] = qty_data.max(axis=1, skipna=True)
    item_cols = [f'item{i}' for i in range(1, 25)]
    make_cols = [f'make{i}' for i in range(1, 25)]
    df_new['unique_items'] = df_new[item_cols].nunique(axis=1, dropna=True)
    df_new['unique_makes'] = df_new[make_cols].nunique(axis=1, dropna=True)
    df_new['item_diversity_ratio'] = df_new['unique_items'] / (df_new['total_items'] + 1)
    df_new['make_diversity_ratio'] = df_new['unique_makes'] / (df_new['total_items'] + 1)
    df_new['price_per_item'] = df_new['total_price'] / (df_new['total_items'] + 1)
    df_new['price_per_quantity'] = df_new['total_price'] / (df_new['total_quantity'] + 1)
    round_prices = price_data.apply(lambda x: (x % 100 == 0).sum(), axis=1)
    df_new['round_prices_count'] = round_prices
    df_new['round_prices_ratio'] = round_prices / (df_new['total_items'] + 1)
    df_new['has_high_value_item'] = (price_data.max(axis=1) > price_data.quantile(0.95, axis=1)).astype(int)
    df_new['high_quantity_items'] = (qty_data > 10).sum(axis=1)
    df_new['max_quantity_ratio'] = df_new['max_quantity'] / (df_new['avg_quantity'] + 1)
    df_new['all_prices_round'] = (price_data % 100 == 0).all(axis=1).astype(int)
    df_new['all_prices_same'] = (price_data.nunique(axis=1, dropna=True) <= 1).astype(int)
    df_new['total_very_high'] = (df_new['total_price'] > 10000).astype(int)
    df_new['avg_very_high'] = (df_new['avg_price'] > 2000).astype(int)
    df_new['price_concentration'] = df_new['max_price'] / (df_new['total_price'] + 1)
    df_new['diversity_too_low'] = (df_new['unique_items'] == 1).astype(int)
    return df_new

def encode_categorical_features(df, target, target_smooth=5, encoders=None):
    """
    Encodages des variables catégorielles avec 3 méthodes
    """
    df_processed = df.copy()
    if encoders is None:
        encoders = {
            'target_encoders': {},
            'count_encoders': {},
            'label_encoders': {},
            'global_means': {},
            'fraud_rate': target.mean() if target is not None else 0.0
        }
        is_training = True
    else:
        is_training = False
    categorical_cols = [col for col in df_processed.columns if df_processed[col].dtype == 'object']
    if is_training and target is not None:
        global_mean = target.mean()
        for col in categorical_cols:
            df_processed[col] = df_processed[col].fillna('UNKNOWN').astype(str)
            target_stats = pd.DataFrame({
                'category': df_processed[col],
                'target': target
            }).groupby('category')['target'].agg(['mean', 'count']).reset_index()
            target_stats['smoothed_mean'] = (
                (target_stats['mean'] * target_stats['count'] + global_mean * target_smooth) / 
                (target_stats['count'] + target_smooth)
            )
            encoders['target_encoders'][col] = dict(zip(target_stats['category'], target_stats['smoothed_mean']))
            encoders['global_means'][col] = global_mean
            df_processed[f'TE_{col}'] = df_processed[col].map(encoders['target_encoders'][col]).fillna(global_mean)
            count_map = df_processed[col].value_counts().to_dict()
            encoders['count_encoders'][col] = count_map
            df_processed[f'CE_{col}'] = df_processed[col].map(count_map)
            le = LabelEncoder()
            df_processed[col] = le.fit_transform(df_processed[col])
            encoders['label_encoders'][col] = le
    else:
        for col in categorical_cols:
            if col in encoders['target_encoders']:
                df_processed[col] = df_processed[col].fillna('UNKNOWN').astype(str)
                df_processed[f'TE_{col}'] = df_processed[col].map(encoders['target_encoders'][col]).fillna(encoders['global_means'][col])
                df_processed[f'CE_{col}'] = df_processed[col].map(encoders['count_encoders'][col]).fillna(0)
                le = encoders['label_encoders'][col]
                mask = df_processed[col].isin(le.classes_)
                df_processed.loc[mask, col] = le.transform(df_processed.loc[mask, col])
                df_processed.loc[~mask, col] = -1
    return df_processed, encoders

if __name__ == "__main__":
    # Exemple d'utilisation pour tester le module
    import os

    # Chemins des fichiers (à adapter selon ton arborescence)
    TRAIN_FILE = '../data/X_train.csv'
    TARGET_FILE = '../data/y_train.csv'

    if os.path.exists(TRAIN_FILE) and os.path.exists(TARGET_FILE):
        print("Chargement des données...")
        df = pd.read_csv(TRAIN_FILE)
        y = pd.read_csv(TARGET_FILE)['fraud_flag']

        print("Création des features...")
        features = create_fraud_features(df)

        print("Encodage des variables catégorielles...")
        processed, encoders = encode_categorical_features(features, y)

        print("Shape finale :", processed.shape)
        print("Colonnes générées :", processed.columns.tolist()[-10:])  # Affiche les 10 dernières colonnes
    else:
        print("Fichiers de données non trouvés. Merci de vérifier les chemins.")