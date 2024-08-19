import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go



def gerar_dados_fluxo_caixa(anos=1):
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
             'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    
    dados = []
    
    for ano in range(2023, 2023 + anos):
        receitas = np.random.randint(10000, 20000, size=12)
        despesas = np.random.randint(5000, 15000, size=12)
        fluxo_caixa = receitas - despesas
        
        for i in range(12):
            dados.append({
                'Ano': ano,
                'Mês': meses[i],
                'Receitas': receitas[i],
                'Despesas': despesas[i],
                'Fluxo de Caixa': fluxo_caixa[i]
            })
    
    return pd.DataFrame(dados)

def filtrar_dados(dados, meses_selecionados, anos_selecionados):
    return dados[(dados['Mês'].isin(meses_selecionados)) & (dados['Ano'].isin(anos_selecionados))]

def main():
    st.set_page_config(
        page_title="Fluxo de Caixa", 
        layout="wide",
        page_icon="✅"
        )
    st.title("Análise de Fluxo de Caixa")
    
    anos = st.sidebar.slider("Selecione a quantidade de anos:", 1, 5, 1)
    dados_fluxo_caixa = gerar_dados_fluxo_caixa(anos=anos)
    
    st.sidebar.subheader("Filtros")
    meses = dados_fluxo_caixa['Mês'].unique()
    meses_selecionados = st.sidebar.multiselect("Selecione os meses:", meses, default=meses)
    
    anos = dados_fluxo_caixa['Ano'].unique()
    anos_selecionados = st.sidebar.multiselect("Selecione os anos:", anos, default=anos)
    
    dados_filtrados = filtrar_dados(dados_fluxo_caixa, meses_selecionados, anos_selecionados)
    
    st.subheader("Tabela - Mês a mês")
    st.dataframe(dados_filtrados.style.format({"Receitas": "R${:,.2f}", "Despesas": "R${:,.2f}", "Fluxo de Caixa": "R${:,.2f}"}))
    
    st.subheader("Gráfico - Fluxo de Caixa Mensal")
    # Adicionando a cor das barras com base no valor do fluxo de caixa
    dados_filtrados['Cor'] = dados_filtrados['Fluxo de Caixa'].apply(lambda x: 'red' if x < 0 else 'blue')

    fig = px.bar(dados_filtrados, x='Mês', y='Fluxo de Caixa', color='Ano', barmode='group',
                 labels={'Fluxo de Caixa': 'Valor em R$', 'Mês': 'Meses'}, 
                 title="Fluxo de Caixa Mensal",
                 color_discrete_map={year: 'blue' if dados_filtrados[dados_filtrados['Ano'] == year]['Fluxo de Caixa'].iloc[0] >= 0 else 'red' for year in anos_selecionados})
    
    # Alterando as cores das barras com base no valor
    fig.update_traces(marker=dict(color=dados_filtrados['Cor']))

    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Receitas vs Despesas")
    fig = go.Figure()
    
    for ano in anos_selecionados:
        dados_ano = dados_filtrados[dados_filtrados['Ano'] == ano]
        fig.add_trace(go.Scatter(x=dados_ano['Mês'], y=dados_ano['Receitas'],
                                 mode='lines+markers', name=f'Receitas {ano}', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=dados_ano['Mês'], y=dados_ano['Despesas'],
                                 mode='lines+markers', name=f'Despesas {ano}', line=dict(color='red')))
    
    fig.update_layout(title="Comparação de Receitas e Despesas",
                      xaxis_title="Meses", yaxis_title="Valor em R$",
                      legend_title="Ano", hovermode="x unified")
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Gráfico - Fluxo de Caixa Acumulado")
    dados_filtrados['Fluxo Acumulado'] = dados_filtrados.groupby('Ano')['Fluxo de Caixa'].cumsum()
    fig = px.line(dados_filtrados, x='Mês', y='Fluxo Acumulado', color='Ano',
                  labels={'Fluxo Acumulado': 'Valor Acumulado em R$', 'Mês': 'Meses'},
                  title="Fluxo de Caixa Acumulado")
    st.plotly_chart(fig, use_container_width=True)

if __name__ == '__main__':
    main()
