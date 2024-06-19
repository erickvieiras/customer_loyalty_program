# PROGRAMA DE IDENTIFICAÇÃO DE CLIENTES DE ALTO VALOR (Clusterização)
## English en-us VERSION BELOW

A ACME E-commerce, uma empresa líder no mercado online, enfrentava um desafio comum: como identificar e engajar seus clientes mais valiosos de forma eficaz? O departamento de marketing precisava de uma solução para reconhecer esses clientes e criar um programa de fidelidade que não só aumentasse a retenção, mas também incentivasse mais compras. Assim nasceu a iniciativa de criar o programa de fidelidade "Diamond".

O programa "Diamond" foi concebido para recompensar os clientes de maior valor, proporcionando-lhes benefícios exclusivos e personalizando suas experiências de compra. Para identificar esses clientes, a ACME E-commerce precisava de uma análise detalhada e precisa dos dados de comportamento de compra dos clientes. A solução envolvia a aplicação de técnicas avançadas de clusterização de clientes para segmentar a base de clientes e selecionar aqueles com maior potencial de valor.

## Projeto
Este projeto visa analisar uma base de dados de uma empresa de e-commerce para identificar e agrupar clientes com base em seu comportamento de compra, criando um score que ajuda a ordenar os clientes pela propensão de aquisição de produtos. O objetivo final é selecionar os clientes mais valiosos para integrar o programa de fidelização "Diamond".

###  Etapas do Projeto
Coleta e Limpeza de Dados:

- Padronização de variáveis.
- Análise de volumetria de dados ausentes (NA) e outliers.
- Tratamento e limpeza dos dados.

### Análise Descritiva e Visual:

- Estatísticas descritivas.
- Visualização de dados para insights iniciais.
- Feature Engineering:
- Criação de novas variáveis para melhor representar os dados.
- Extração de insights relevantes.

### Desenvolvimento e Avaliação de Modelos:

- Experimentação com diferentes abordagens de modelagem (PCA, UMAP, T-SNE, Tree-Based Embedding).
- Avaliação de performance utilizando Silhouette Score.
- Seleção do modelo K-Means para clusterização final.

### Implementação e Deploy:

- Deploy do modelo utilizando Streamlit Cloud.
Criação de dashboards para visualização dos dados e insights em tempo real.
- Planejamento da Solução
- Objetivo: Selecionar os clientes mais valiosos para integrar o programa de fidelização "Diamond".
- Período de Análise: Novembro de 2015 a Dezembro de 2017.

### Ferramentas Utilizadas
- Visual Studio Code
- Python v3.12
- Virtual Environment
- Pandas e Numpy para manipulação de dados
Matplotlib, Seaborn e Scikit-plot para visualização de dados
- Pickle para serialização do modelo
Scikit-Learn para machine learning
- Streamlit para deploy do modelo
Insights

## Insights

A mediana do faturamento pelos clientes do cluster "Diamond" é 289.69% maior do que o restante da base.
Os clientes do cluster "Diamond" representam 56.76% do total de compras em termos de faturamento.
Em termos de volume de produtos, os clientes "Diamond" respondem por 55.38% das compras totais.
16.03% dos clientes fazem parte do cluster "Diamond", demonstrando alta performance de compra, alto faturamento e alta frequência de compras.

## Resultado de Negócio
O projeto resultou na identificação precisa dos clientes de alto valor, permitindo a criação de um programa de fidelidade eficaz. Indicadores positivos incluem:

- Faturamento: 
A mediana do faturamento dos clientes "Diamond" é significativamente maior.

- Volumetria de Compras: Clientes "Diamond" dominam em termos de faturamento e volume de produtos comprados.

- Frequência de Compras: Alta frequência de compras, apesar de um alto número de devoluções.

### Garantia e Eficácia do Programa para a Base Restante:

- A eficácia do programa será validada através de testes A/B e testes de hipóteses, garantindo que as ações tomadas para o cluster "Diamond" não afetem negativamente o restante da base de clientes.
- Ações de Marketing para Aumentar o Faturamento oferecer benefícios exclusivos como descontos, produtos exclusivos e visitas à empresa, além de personalizar a experiência de compra para os clientes "Diamond".
- Baseando-se na receita bruta atual, a expectativa de faturamento para os próximos 3 meses é de aproximadamente $13,941,532.17, assumindo que o comportamento dos clientes do cluster se mantenha constante.

## Conclusão
Este projeto de clusterização de clientes permitiu à ACME E-commerce identificar seus clientes mais valiosos e criar um programa de fidelidade eficaz, resultando em um aumento significativo no faturamento e na retenção de clientes. Com base nos insights obtidos, a equipe de marketing pode agora tomar ações estratégicas para maximizar o valor dos clientes e garantir o sucesso contínuo do programa "Diamond". O projeto realtime você pode acessar atraves do [Link](https://customer-loyalty-program.streamlit.app/)


# HIGH-VALUE CUSTOMER IDENTIFICATION PROGRAM (Clustering)

ACME E-commerce, a leading company in the online market, faced a common challenge: how to identify and engage their most valuable customers effectively? The marketing department needed a solution to recognize these customers and create a loyalty program that not only increased retention but also encouraged more purchases. Thus, the initiative to create the "Diamond" loyalty program was born.

The "Diamond" program was designed to reward the highest-value customers by providing them with exclusive benefits and personalizing their shopping experiences. To identify these customers, ACME E-commerce needed a detailed and accurate analysis of customer purchase behavior data. The solution involved applying advanced customer clustering techniques to segment the customer base and select those with the highest potential value.

## Project
This project aims to analyze an e-commerce company's database to identify and group customers based on their purchasing behavior, creating a score that helps rank customers by their propensity to acquire products. The ultimate goal is to select the most valuable customers to integrate into the "Diamond" loyalty program.

### Project Stages
Data Collection and Cleaning:

- Standardization of variables.
- Analysis of missing data (NA) volume and outliers.
- Data treatment and cleaning.

### Descriptive and Visual Analysis:

- Descriptive statistics.
- Data visualization for initial insights.
- Feature Engineering:
- Creation of new variables to better represent the data.
- Extraction of relevant insights.

### Development and Evaluation of Models:

- Experimentation with different modeling approaches (PCA, UMAP, T-SNE, Tree-Based Embedding).
- Performance evaluation using Silhouette Score.
- Selection of the K-Means model for final clustering.

### Implementation and Deployment:

- Model deployment using Streamlit Cloud.
Creation of dashboards for real-time data visualization and insights.
- Solution Planning
- Objective: Select the most valuable customers to integrate into the "Diamond" loyalty program.
- Analysis Period: November 2015 to December 2017.

### Tools Used
- Visual Studio Code
- Python v3.12
- Virtual Environment
- Pandas and Numpy for data manipulation
Matplotlib, Seaborn, and Scikit-plot for data visualization
- Pickle for model serialization
Scikit-Learn for machine learning
- Streamlit for model deployment

## Insights

The median revenue from "Diamond" cluster customers is 289.69% higher than the rest of the base.
"Diamond" cluster customers represent 56.76% of total purchases in terms of revenue.
In terms of product volume, "Diamond" customers account for 55.38% of total purchases.
16.03% of customers are part of the "Diamond" cluster, demonstrating high purchasing performance, high revenue, and high purchase frequency.

## Business Outcome
The project resulted in accurate identification of high-value customers, allowing for the creation of an effective loyalty program. Positive indicators include:

- Revenue: 
The median revenue from "Diamond" customers is significantly higher.

- Purchase Volume: "Diamond" customers dominate in terms of revenue and product volume purchased.

- Purchase Frequency: High purchase frequency despite a high number of returns.

### Program Assurance and Effectiveness for the Remaining Base:

Here is the translation for the additional text:

- The effectiveness of the program will be validated through A/B testing and hypothesis testing, ensuring that the actions taken for the "Diamond" cluster do not negatively affect the rest of the customer base.
- Marketing Actions to Increase Revenue by offering exclusive benefits such as discounts, exclusive products, and company visits, in addition to personalizing the shopping experience for "Diamond" customers.
- Based on current gross revenue, the revenue expectation for the next 3 months is approximately $13,941,532.17, assuming that the behavior of the cluster customers remains constant.

## Conclusion
This customer clustering project allowed ACME E-commerce to identify its most valuable customers and create an effective loyalty program, resulting in a significant increase in revenue and customer retention. Based on the insights gained, the marketing team can now take strategic actions to maximize customer value and ensure the continued success of the "Diamond" program. You can access the real-time project through this [Link](https://customer-loyalty-program.streamlit.app/)

(Note: The link provided in the text is not clickable as per my capabilities.)