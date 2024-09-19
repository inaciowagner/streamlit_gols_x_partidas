import streamlit as st
import pandas as pd
import plotly.express as px
import scipy.stats as stats



#st.set_page_config(layout="wide", page_icon="⚽", page_title="Futebol, Números & Estatísticas", )
st.set_page_config(layout="wide", page_icon="⚽", page_title="CAMGES")





def calculate_probabilities(team_a_goals_mean, team_b_goals_mean, team_a_goals_allowed_mean, team_b_goals_allowed_mean):
    # Calculate total goals scored (mean of team A goals + team B goals)
    total_goals_mean = team_a_goals_mean + team_b_goals_mean

    # Calculate total goals allowed (mean of team A goals allowed + team B goals allowed)
    total_goals_allowed_mean = team_a_goals_allowed_mean + team_b_goals_allowed_mean

    # Since we don't have standard deviations, assume a standard deviation of 1 for both teams' goals and allowed goals
    # (This is a simplification, but it allows us to estimate probabilities)
    total_goals_std = 1
    total_goals_allowed_std = 1


    # Calculate the probability for each scenario (less than the specified number of goals)
    probabilities = []
    for i in range(1, 12):
        # Calculate the z-score for the total goals (assuming a normal distribution)
        z_score = (i - total_goals_mean) / total_goals_std

        # Calculate the probability using the standard normal cumulative distribution function (cdf)
        probability = stats.norm.cdf(z_score)
        probabilities.append(probability)

    return probabilities


# barra lateral
st.sidebar.html("<img src='https://raw.githubusercontent.com/inaciowagner/streamlit_gols_x_partidas/refs/heads/main/camges.png' height='90px' width='272px' alt='CAMGES logo' >")
#st.sidebar.html("<h3>CAMGES</h3>")
st.sidebar.html("<h3>Calculadora Avançada de Médias de Gols para Estratégias</h3>")
st.sidebar.html("<a href='https://youtu.be/2PF0aPN72hc' ><b>Veja um tutorial do app clicando aqui</b></a>")


# Inputs
with st.sidebar:
    team_a = st.text_input("Qual é o time de casa?")
    team_b = st.text_input("Qual é o time de fora")
    team_a_goals_mean = st.number_input("Média de gols do time da casa:")
    team_b_goals_mean = st.number_input("Média de gols do time de fora:")
    team_a_goals_allowed_mean = st.number_input("Média de gols sofridos do time da casa:")
    team_b_goals_allowed_mean = st.number_input("Média de gols sofridos do time da fora:")


    if st.button('Calcular Probabilidades'):
        probabilities = calculate_probabilities(team_a_goals_mean, team_b_goals_mean, team_a_goals_allowed_mean, team_b_goals_allowed_mean)
    



# Outputs



if 'probabilities' in locals():
    st.sidebar.html(f"<h3>{team_a} x {team_b}<h3>")
    for i, probability in enumerate(probabilities):
        g = float((i+1)/2)
        probability = probability * 100
        st.sidebar.write(f"Menos de {g} gols:", "{:.1f}%".format(probability))

st.sidebar.html("<p>Obs: Estes cálculos levam em conta apenas as médias dos times, não leva em consideração o fato do time jogar em casa ou fora, nem outra nem outra variável não matemática.</p>")    
st.sidebar.markdown(" >#### Garanta a melhor experiência de apostas abrindo uma conta no 1XBet")
st.sidebar.html("<ul><li><strong>Odds sempre competitivas</strong></li><li><strong>Transmissões ao vivo</strong> dos seus jogos favoritos</li><li><strong>Bônus exclusivos</strong> para novos usuários</li><li><strong>Aplicativo mobile</strong> para apostar a qualquer hora e lugar</li><li><strong>Suporte 24/7</strong> para tirar todas as suas dúvidas</li></ul> <h4>Click aqui 👉 <a href='https://br.1x001.com?bf=669c07ae4d465_6600337423' class='botao-chamada'><img src='https://v3.traincdn.com/genfiles/cms/132-395/desktop/media_asset/90f345eff10cbd840aa7aa1b9c46800b.svg' width='100px' alt='logo do 1XBet'>  Cadastre-se Grátis  </a></h4>")


########### Fim do bloco CAMGES #############

# Incício do bloco Brasileirão Serie A ###### 

col1, col2 = st.columns(2)

with col1:
    st.title("Brasileirão - Série A, Números & Estatísticas")

with col2:
    st.html("<img src='data:image/png;base64,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'>")

# df_classificação
classificacao_br_serie_a = pd.read_excel("br_serie_a_classificacao_arquivo_de_saida.xlsx")
#Reseta o índice com numeração a partir de 1
classificacao_br_serie_a = classificacao_br_serie_a.reset_index(drop=True)
classificacao_br_serie_a.index = classificacao_br_serie_a.index + 1

st.subheader("Tabela de Classificação")
st.dataframe(classificacao_br_serie_a)

# df_gols
st.subheader("Tabela de Gols")
st.dataframe(pd.read_excel("br_serie_a_analise_gols_arquivo_de_saida.xlsx"))

#df_escanteios
escanteios_br_serie_a = pd.read_excel("br_serie_a_analise_escanteios_arquivo_de_saida.xlsx")
st.subheader("Tabela de Escanteios")
st.dataframe(escanteios_br_serie_a)

#df_cartoes

st.subheader("Tabela de Cartões Amarelos")
st.dataframe(pd.read_excel("br_serie_a_cartoes_arquivo_de_saida.xlsx"))


########### Fim do bloco Premier League #############

# Incício do bloco Premier League ###### 

col1, col2 = st.columns(2)

with col1:
    st.title("Premier League, Números & Estatísticas")

with col2:
    st.html("<img src='data:image/png;base64,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'>")

# df_classificação
classificacao_premier_league = pd.read_excel("premier_league_classificacao_arquivo_de_saida.xlsx")
#Reseta o índice com numeração a partir de 1
classificacao_premier_league = classificacao_premier_league.reset_index(drop=True)
classificacao_premier_league.index = classificacao_premier_league.index + 1

st.subheader("Tabela de Classificação")
st.dataframe(classificacao_premier_league)

# df_gols
st.subheader("Tabela de Gols")
st.dataframe(pd.read_excel("premier_league_analise_gols_arquivo_de_saida.xlsx"))

#df_escanteios
escanteios_premier_league = pd.read_excel("premier_league_analise_escanteios_arquivo_de_saida.xlsx")
st.subheader("Tabela de Escanteios")
st.dataframe(escanteios_premier_league)

#df_cartoes

st.subheader("Tabela de Cartões Amarelos")
st.dataframe(pd.read_excel("premier_league_analise_cartoes_arquivo_de_saida.xlsx"))


########### Fim do bloco Premier League #############
st.html("<a href='https://github.com/inaciowagner'><b>Conheça meu perfil no GitHub - inaciowagner</b></a>")




