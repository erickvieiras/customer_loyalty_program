#imports====================================================================================================
import pandas                   as pd
import numpy                    as np
import matplotlib.pyplot        as plt
import plotly.express           as px
import seaborn                  as sns
import inflection
import re
import streamlit                as st
import folium 
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from streamlit_option_menu import option_menu
import data_processing         as dp
import cluster                 as clst
import pickle

#set_page config===========================================================================================
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
st.title('High Value Customer Identification')
sns.set_theme(rc = {'figure.figsize':(15,10)})

def inject_css(css: str):
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

css = """
.stApp h1 {
    margin-top: -50px;  /* Ajuste o valor conforme necessário */
};
"""
inject_css(css)

#load data=================================================================================================
df_raw = pd.read_csv('dataset/data.csv', encoding='latin-1')
data = dp.cleaning_data(df_raw)
df = dp.merge_data(data)

#main======================================================================================================

# 2. horizontal menu
selected2 = option_menu(None, ['About Project', 'Preprocessed Data', 'Customer Analysis', 'Geolocation View', 'Cluster Analysis'], 
    icons=['house', 'table', "bar-chart", 'map', 'server'], 
    menu_icon="cast", default_index=0, orientation="horizontal",     
    styles={"nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px"},
        "nav-link-selected": {"background-color": "#4fc4c0"},
    }
)

if selected2 == 'About Project':
    st.header('ACME E-commerce: Diamond Loyalty Program')

    # Introduction text
    intro_text = """
    ACME E-commerce, a leading company in the online market, faced a common challenge: how to identify and engage their most valuable customers effectively? 
    The marketing department needed a solution to recognize these customers and create a loyalty program that not only increased retention but also encouraged more purchases. 
    Thus, the initiative to create the "Diamond" loyalty program was born.

    The "Diamond" program was designed to reward the highest-value customers by providing them with exclusive benefits and personalizing their shopping experiences. 
    To identify these customers, ACME E-commerce needed a detailed and accurate analysis of customer purchase behavior data. 
    The solution involved applying advanced customer clustering techniques to segment the customer base and select those with the highest potential value.
    """

    # Markdown section
    st.markdown(intro_text)
    with st.expander('Raw Dataset Info'):
        st.dataframe(df_raw)

elif selected2 == 'Preprocessed Data':
    st.dataframe(df.set_index('customer_id'), use_container_width = True)

elif selected2 == 'Customer Analysis':

    columns1, columns2 = st.columns(2)

    with columns1:
        df_purchase = df[['country', 'qtde_invoices', 'qtde_returns']].groupby('country').mean().reset_index()
        df_purchase_filter = df_purchase.sort_values(by = 'qtde_invoices', ascending = False).head(10)
        fig = px.bar(df_purchase_filter, x = 'country', y = 'qtde_invoices', text_auto = '0.2s', color = 'country', title = 'Countries with the highest average purchasing volume')
        # Calculando a média dos valores de gross_revenue
        purchase_line = df_purchase_filter['qtde_invoices'].mean()
        # Adicionando uma linha horizontal representando a média
        fig.add_hline(y = purchase_line, line_dash="dash", line_color="red", annotation_text=f'Mean: {purchase_line:.0f}', annotation_position="bottom right")
        st.plotly_chart(fig, use_container_width= True)

    with columns2:
        df_returns_filter = df_purchase_filter.sort_values(by = 'qtde_returns', ascending = True).head(4)
        fig1= px.pie(df_returns_filter, names = 'country', values = 'qtde_returns', hole = 0.5, color = 'country', title = 'Countries with lower volume of returns among higher volume of purchases')
        st.plotly_chart(fig1, use_container_width= True)

    columns3, columns4 = st.columns(2)
    with columns3:
        df_purchase2 = df[['country', 'gross_revenue', 'qtde_invoices', 'qtde_returns']].groupby('country').mean().reset_index()
        df_purchase_filter2 = df_purchase2.sort_values(by = 'gross_revenue', ascending = False).head(10)
        fig3 = px.bar(df_purchase_filter2, x = 'country', y = 'gross_revenue', text_auto = '0.2s', color = 'country', title = 'Countries with the highest revenue volume')
        st.plotly_chart(fig3, use_container_width= True)
    with columns4:
        st.dataframe(df_purchase2.sort_values(by = 'gross_revenue', ascending = False), use_container_width = True)

elif selected2 == 'Geolocation View':

    # Função para criar o mapa
    def create_map(df_map, selected_countries = None, zoom=1):
        # Inicializa uma figura de tamanho específico
        f = folium.Figure(width=900, height=768)
    
        if country_select:
            # Filtra o dataframe para incluir apenas os países selecionados
            df_map = df_map[df_map['country'].isin(country_select)]

        # Cria um mapa centrado na média das coordenadas de latitude e longitude dos dados
        m = folium.Map(max_bounds=True, location=[df_map["latitude"].mean(), df_map["longitude"].mean()], zoom_start=zoom).add_to(f)

        # Cria um cluster de marcadores para agrupar os pontos próximos
        marker_cluster = MarkerCluster().add_to(m)

        # Itera sobre as linhas do dataframe para adicionar marcadores no mapa
        for _, line in df_map.iterrows():
            # Extrai os dados que serão exibidos no popup
            country = line["country"]
            latitude = line["latitude"]
            longitude = line["longitude"]

            # Formata o conteúdo HTML do popup
            html = "<p>Country: <strong>{}</strong></p>".format(country)
            html += "Latitude: {}<br>".format(latitude)
            html += "Longitude: {}<br>".format(longitude)
            html = html.format(country, latitude, longitude)

            # Cria o popup com o HTML formatado
            popup = folium.Popup(
                folium.Html(html, script=True),
                max_width=500,
            )

            # Adiciona um marcador com base na latitude e longitude da linha atual
            folium.Marker(
                [latitude, longitude],
                popup=popup,
                icon=folium.Icon(icon="home", prefix="fa"),
            ).add_to(marker_cluster)

        # Renderiza o mapa estático no Streamlit
        folium_static(m, width=1024, height=400)

    # Interface do Streamlit para seleção de países
    country_select = st.multiselect("Which countries would you like to research?", df['country'].unique(), df['country'].unique())

    # Chama a função para criar o mapa
    create_map(df, selected_countries=country_select, zoom=1)

elif selected2 == 'Cluster Analysis':
    
    tab1, tab2, tab3 = st.tabs(['Cluster Data', 'Revenue Analysis and Purchase Volume', 'Frequency and Representativeness Analysis'])
    with tab1:
        df_cluster = clst.clustering(df_raw)
        st.dataframe(df_cluster.set_index('customer_id'), use_container_width = True)

    with tab2:
        
        graph1 = px.bar(df_cluster, x='cluster', y='gross_revenue', text_auto = '0.2s', title = 'Cluster Billing Behavior',
                        color='cluster', color_continuous_scale=px.colors.qualitative.Prism)
        # Calculando a média dos valores de gross_revenue
        mean_value = df_cluster['gross_revenue'].mean()
        # Adicionando uma linha horizontal representando a média
        graph1.add_hline(y = mean_value, line_dash="dash", line_color="red", annotation_text=f'Mean: US$ {mean_value:.2f}', annotation_position="bottom right")
        # Exibindo o gráfico no Streamlit
        st.plotly_chart(graph1, use_container_width=True)

        cols1, cols2 = st.columns(2)
        with cols1:
            graph2 = px.bar(df_cluster, x='cluster', y='qtde_products', text_auto = '0.2s', title = 'Purchasing Volume by Cluster', color='cluster', color_continuous_scale=px.colors.qualitative.Prism)
            # Calculando a média dos valores de gross_revenue
            mean_value2 = df_cluster['qtde_products'].mean()
            # Adicionando uma linha horizontal representando a média
            graph2.add_hline(y=mean_value2, line_dash="dash", line_color="red", annotation_text=f'Mean: {mean_value2:.0f}', annotation_position="bottom right")
            # Exibindo o gráfico no Streamlit
            st.plotly_chart(graph2, use_container_width=True)

        with cols2:
            graph3 = px.bar(df_cluster, x='cluster', y='qtde_returns', text_auto = '0.2s', title = 'Volume of Returns by Cluster', color='cluster', color_continuous_scale=px.colors.qualitative.Prism)
            # Calculando a média dos valores de gross_revenue
            mean_value3 = df_cluster['qtde_returns'].mean()
            # Adicionando uma linha horizontal representando a média
            graph3.add_hline(y=mean_value3, line_dash="dash", line_color="red", annotation_text=f'Mean: {mean_value3:.0f}', annotation_position="bottom right")
            # Exibindo o gráfico no Streamlit
            st.plotly_chart(graph3, use_container_width=True)

    with tab3:
        cols3, cols4 = st.columns(2)
        with cols3:
            graph6 = px.bar(df_cluster, x='cluster', y='percentual_customer', text_auto = '0.2s', title = 'Volume of Customers per Cluster',
                        color='cluster', color_continuous_scale=px.colors.qualitative.Prism)
            mean_value6 = df_cluster['percentual_customer'].mean()
            # Adicionando uma linha horizontal representando a média
            graph6.add_hline(y=mean_value6, line_dash="dash", line_color="red", annotation_text=f'Mean: {mean_value6:.0f}', annotation_position="bottom right")
            # Exibindo o gráfico no Streamlit
            st.plotly_chart(graph6, use_container_width=True)


        with cols4:
            graph5 = px.bar(df_cluster, x='cluster', y='recency_days', text_auto = '0.2s', title = 'Average Purchase Frequency', color='cluster', color_continuous_scale=px.colors.qualitative.Prism)
            # Calculando a média dos valores de gross_revenue
            mean_value5 = df_cluster['recency_days'].mean()
            # Adicionando uma linha horizontal representando a média
            graph5.add_hline(y=mean_value5, line_dash="dash", line_color="red", annotation_text=f'Mean Days {mean_value5:.0f}', annotation_position="bottom right")
            # Exibindo o gráfico no Streamlit
            st.plotly_chart(graph5, use_container_width=True)