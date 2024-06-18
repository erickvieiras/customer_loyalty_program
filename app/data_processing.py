import pandas                   as pd
import numpy                    as np
import matplotlib.pyplot        as plt
import plotly.express           as px
import seaborn                  as sns
import inflection
import re

def cleaning_data(data):

    df2 = data
    old_columns = data.columns
    snakecase = lambda x: inflection.underscore(x)
    new_columns = list(map(snakecase, old_columns))
    df2.columns = new_columns

    df_missing = df2.loc[df2['customer_id'].isna(),:]
    df_full = df2.loc[~df2['customer_id'].isna(),:]

    # create reference
    df_backup = pd.DataFrame( df_missing['invoice_no'].drop_duplicates() )
    df_backup['customer_id'] = np.arange( 19000, 19000+len( df_backup ), 1)

    # merge original with reference dataframe
    df2 = pd.merge( df2, df_backup, on='invoice_no', how='left' )

    # coalesce 
    df2['customer_id'] = df2['customer_id_x'].combine_first( df2['customer_id_y'] )

    # drop extra columns
    df2 = df2.drop( columns=['customer_id_x', 'customer_id_y'], axis=1 )

    df2['invoice_date'] = pd.to_datetime(df2['invoice_date'])
    df2['customer_id'] = df2['customer_id'].astype(int)

    stock_code_letters = df2.loc[df2['stock_code'].apply(lambda x: bool(re.search('^[a-zA-Z]+$', x))), 'stock_code'].unique()

    df4 = df2.copy()
    # === Numerical attributes ====
    df4 = df4.loc[df4['unit_price'] >= 0.04, :]

    # === Categorical attributes ====
    df4 = df4[~df4['stock_code'].isin( stock_code_letters) ]

    # description
    df4 = df4.drop( columns='description', axis=1 )

    # map -  
    df4 = df4[~df4['country'].isin( ['European Community', 'Unspecified' ] ) ]

    # bad users
    df4 = df4[~df4['customer_id'].isin( [16446] )]

    # quantity
    df_returns = df4.loc[df2['quantity'] < 0, :]
    df_purchases = df4.loc[df2['quantity'] >= 0, :]

    df_reference = df4.drop(['invoice_no', 'stock_code', 'quantity', 'invoice_date', 'unit_price'], axis = 1).drop_duplicates(ignore_index = True)

    #gross Revenue (quantity * price)
    df_purchase = df_purchases.copy()
    df_purchase.loc[:, 'gross_revenue'] = df_purchase.loc[:, 'quantity'] * df_purchase.loc[:, 'unit_price']


    #monetary
    df_monetary = df_purchase.loc[:,['customer_id','gross_revenue']].groupby('customer_id').sum().reset_index()
    df_reference = pd.merge(df_reference, df_monetary, on = 'customer_id', how = 'left')


    #recency (Last Day Purchase)
    df_recency = df_purchase.loc[:, ['customer_id', 'invoice_date']].groupby( 'customer_id' ).max().reset_index()
    df_recency['recency_days'] = ( df4['invoice_date'].max() - df_recency['invoice_date'] ).dt.days
    df_recency = df_recency[['customer_id', 'recency_days']].copy()
    df_reference = pd.merge( df_reference, df_recency, on='customer_id', how='left' )
 
    #frequency (Quantity of Purchase)
    df_freq = (df_purchase.loc[:, ['customer_id', 'invoice_no']].drop_duplicates()
                                                                .groupby( 'customer_id' )
                                                                .count()
                                                                .reset_index()
                                                                .rename( columns={'invoice_no': 'qtde_invoices'}) )
    df_reference = pd.merge( df_reference, df_freq, on='customer_id', how='left' )

    #frequency (Quantity of Purchase)
    df_freq = (df_purchase.loc[:, ['customer_id', 'quantity']].groupby( 'customer_id' ).sum()
                                                            .reset_index()
                                                            .rename( columns={'quantity': 'qtde_items'} ) )
    df_reference = pd.merge( df_reference, df_freq, on='customer_id', how='left' )

    df_freq = (df_purchase.loc[:, ['customer_id', 'stock_code']].groupby( 'customer_id' ).count()
                                                            .reset_index()
                                                            .rename( columns={'stock_code': 'qtde_products'} ) )
    df_reference = pd.merge( df_reference, df_freq, on='customer_id', how='left' )

    #average ticket
    df_avg_ticket = df_purchase.loc[:, ['customer_id', 'gross_revenue']].groupby( 'customer_id' ).mean().reset_index().rename( columns={'gross_revenue':'avg_ticket'} )
    df_reference = pd.merge( df_reference, df_avg_ticket, on='customer_id', how='left')

    df_aux = df4[['customer_id', 'invoice_date']].drop_duplicates().sort_values( ['customer_id', 'invoice_date'], ascending=False )
    df_aux['next_customer_id'] = df_aux['customer_id'].shift() # next customer
    df_aux['previous_date'] = df_aux['invoice_date'].shift() # next invoince date

    df_aux['avg_recency_days'] = df_aux.apply( lambda x: ( x['invoice_date'] - x['previous_date'] ).days if x['customer_id'] == x['next_customer_id'] else np.nan, axis=1 )

    df_aux = df_aux.drop( ['invoice_date', 'next_customer_id', 'previous_date'], axis=1 ).dropna()

    # average recency 
    df_avg_recency_days = df_aux.groupby( 'customer_id' ).mean().reset_index()

    # merge
    df_reference = pd.merge( df_reference, df_avg_recency_days, on='customer_id', how='left' )

    df_aux = ( df_purchases[['customer_id', 'invoice_no', 'invoice_date']].drop_duplicates()
                                                                .groupby( 'customer_id')
                                                                .agg( max_ = ( 'invoice_date', 'max' ), 
                                                                    min_ = ( 'invoice_date', 'min' ),
                                                                    days_= ( 'invoice_date', lambda x: ( ( x.max() - x.min() ).days ) + 1 ),
                                                                    buy_ = ( 'invoice_no', 'count' ) ) ).reset_index()
    # Frequency
    df_aux['frequency'] = df_aux[['buy_', 'days_']].apply( lambda x: x['buy_'] / x['days_'] if  x['days_'] != 0 else 0, axis=1 )

    # Merge
    df_reference = pd.merge( df_reference, df_aux[['customer_id', 'frequency']], on='customer_id', how='left' )



    df_returns = df_returns[['customer_id', 'quantity']].groupby( 'customer_id' ).sum().reset_index().rename( columns={'quantity':'qtde_returns'} )
    df_returns['qtde_returns'] = df_returns['qtde_returns'] * -1

    df_reference = pd.merge( df_reference, df_returns, how='left', on='customer_id' )
    df_reference.loc[df_reference['qtde_returns'].isna(), 'qtde_returns'] = 0

    df_aux = ( df_purchases.loc[:, ['customer_id', 'invoice_no', 'quantity']].groupby( 'customer_id' )
                                                                                .agg( n_purchase=( 'invoice_no', 'nunique'),
                                                                                    n_products=( 'quantity', 'sum' ) )
                                                                                .reset_index() )

    # calculation
    df_aux['avg_basket_size'] = df_aux['n_products'] / df_aux['n_purchase']

    # merge
    df_reference = pd.merge( df_reference, df_aux[['customer_id', 'avg_basket_size']], how='left', on='customer_id' )


    df_aux = ( df_purchases.loc[:, ['customer_id', 'invoice_no', 'stock_code']].groupby( 'customer_id' )
                                                                                .agg( n_purchase=( 'invoice_no', 'nunique'),
                                                                                    n_products=( 'stock_code', 'nunique' ) )
                                                                                .reset_index() )

    # calculation
    df_aux['avg_unique_basket_size'] = df_aux['n_products'] / df_aux['n_purchase']

    # merge
    df_reference = pd.merge( df_reference, df_aux[['customer_id', 'avg_unique_basket_size']], how='left', on='customer_id' )

    df_reference = df_reference.dropna()

    return df_reference


def merge_data(data):
    df_countries = pd.read_csv('dataset/countries.csv')
    df_merge = pd.merge(data, df_countries, how = 'left', on = 'country')
    df_merge = df_merge.dropna()

    columns = ['customer_id', 'gross_revenue', 'recency_days',
        'qtde_invoices', 'qtde_items', 'qtde_products', 'avg_ticket',
        'avg_recency_days', 'frequency', 'qtde_returns', 'avg_basket_size',
        'avg_unique_basket_size', 'country', 'latitude', 'longitude']

    data = df_merge[columns]
    
    return data