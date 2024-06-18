# Imports ====================================================================================================
import pandas as pd
import numpy as np
import data_processing as dp
import pickle
import umap.umap_ as umap
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans

def clustering(df1):
    # Carregando os modelos pickle
    with open('source/rf_model.pkl', 'rb') as model_file:
        rf_model = pickle.load(model_file)

    with open('source/kmeans_model.pkl', 'rb') as kmeans_file:
        kmeans = pickle.load(kmeans_file)


    with open('source/gross_revenue_scaler.pkl', 'rb') as scaler_file:
        gross_revenue_scaler = pickle.load(scaler_file)

    with open('source/recency_days_scaler.pkl', 'rb') as scaler_file:
        recency_days_scaler = pickle.load(scaler_file)

    with open('source/qtde_products_scaler.pkl', 'rb') as scaler_file:
        qtde_products_scaler = pickle.load(scaler_file)

    with open('source/frequency_scaler.pkl', 'rb') as scaler_file:
        frequency_scaler = pickle.load(scaler_file)

    with open('source/qtde_returns_scaler.pkl', 'rb') as scaler_file:
        qtde_returns_scaler = pickle.load(scaler_file)

    # Selecionando as colunas
    df_space = df1.drop(columns=['customer_id'], axis=1).copy()
    cols_selected = ['customer_id', 'gross_revenue', 'recency_days', 'qtde_products', 'frequency', 'qtde_returns']
    df_space = df1[cols_selected].copy()

    # Aplicar os scalers carregados aos dados
    df_space['gross_revenue'] = gross_revenue_scaler.transform(df_space[['gross_revenue']])
    df_space['recency_days'] = recency_days_scaler.transform(df_space[['recency_days']])
    df_space['qtde_products'] = qtde_products_scaler.transform(df_space[['qtde_products']])
    df_space['frequency'] = frequency_scaler.transform(df_space[['frequency']])
    df_space['qtde_returns'] = qtde_returns_scaler.transform(df_space[['qtde_returns']])

    # Verificar e tratar valores ausentes
    if df_space.isnull().values.any():
        df_space = df_space.fillna(method='ffill')  # Preenchimento para frente como exemplo

    # Divisão dos dados
    x_train = df_space.drop(columns=['customer_id', 'gross_revenue'], axis=1)
    y_train = df_space['gross_revenue']

    # Aplicar o modelo aos dados de treinamento
    leaf = rf_model.apply(x_train)

    # DataFrame leaf
    df_leaf = pd.DataFrame(leaf)

    # Redução de dimensionalidade
    reducer = umap.UMAP(random_state=42)
    embedding = reducer.fit_transform(df_leaf)

    # DataFrame de embedding
    df_tree = pd.DataFrame()
    df_tree['embedding_x'] = embedding[:, 0]
    df_tree['embedding_y'] = embedding[:, 1]

    parameter_tuning = df_tree.copy()

    # Clustering com KMeans
    labels = kmeans.predict(parameter_tuning)

    df10 = parameter_tuning.copy()
    df10['cluster'] = labels

    df_profile = df1[cols_selected].copy()
    df_profile['cluster'] = labels

    # Número de clientes por cluster
    df_cluster = df_profile[['customer_id', 'cluster']].groupby('cluster').count().reset_index()
    df_cluster['percentual_customer'] = 100 * (df_cluster['customer_id'] / df_cluster['customer_id'].sum())

    # Média de receita bruta por cluster
    df_avg_gross_revenue = df_profile[['gross_revenue', 'cluster']].groupby('cluster').mean().reset_index()
    df_cluster = pd.merge(df_cluster, df_avg_gross_revenue, how='inner', on='cluster')

    # Média de dias desde a última compra por cluster
    df_avg_recency_days = df_profile[['recency_days', 'cluster']].groupby('cluster').mean().reset_index()
    df_cluster = pd.merge(df_cluster, df_avg_recency_days, how='inner', on='cluster')

    # Média de quantidade de produtos por cluster
    df_qtde_products = df_profile[['qtde_products', 'cluster']].groupby('cluster').mean().reset_index()
    df_cluster = pd.merge(df_cluster, df_qtde_products, how='inner', on='cluster')

    # Média de frequência de compra por cluster
    df_frequency = df_profile[['frequency', 'cluster']].groupby('cluster').mean().reset_index()
    df_cluster = pd.merge(df_cluster, df_frequency, how='inner', on='cluster')

    # Média de devoluções por cluster
    df_qtde_returns = df_profile[['qtde_returns', 'cluster']].groupby('cluster').mean().reset_index()
    df_cluster = pd.merge(df_cluster, df_qtde_returns, how='inner', on='cluster')
    df_cluster = df_cluster.sort_values('gross_revenue', ascending=False)

    # Ordenação das colunas
    new_order_comuns = ['customer_id', 'cluster', 'percentual_customer', 'frequency', 'recency_days', 'qtde_products', 'qtde_returns', 'gross_revenue']
    df_cluster = df_cluster[new_order_comuns]

    return df_cluster
