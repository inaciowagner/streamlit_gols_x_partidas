import scipy.stats as stats
import streamlit as st


st.set_page_config(layout="wide", page_icon="⚽")

col1, col2, col3 = st.columns(3)

with col1:
    st.html("<img src='https://upload.wikimedia.org/wikipedia/pt/4/42/Campeonato_Brasileiro_S%C3%A9rie_A_logo.png' alt='logo do Brasileirão' width='100' >")

with col2:
    st.html("<h3>PROBABILIDADE <br> TOTAL DE G⚽LS</h3>")


with col3:
    st.html("<img src='https://upload.wikimedia.org/wikipedia/pt/f/f4/Campeonato_Brasileiro_S%C3%A9rie_B_logo.png' alt='logo do Brasileirão' width='100' >")


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
st.html("<h2>Para Aposta em Total de Gols</h2><br/>")
st.html(f"<h3>{team_a} x {team_b}<h3>")

if 'probabilities' in locals():
    for i, probability in enumerate(probabilities):
        g = float((i+1)/2)
        st.write(f"Menos de {g} gols:", "{:.2f}".format(probability))

st.html("<p>Obs: Estes cálculos levam em conta apenas as médias dos times, não leva em consideração o fato do time jogar em casa ou fora, nem outra nem outra variável não matemática.</p>")
st.html("<h3>Garanta a melhor experiência de apostas abrindo uma conta no 1XBet  </h3><ul><li><strong>Odds sempre competitivas</strong></li><li><strong>Transmissões ao vivo</strong> dos seus jogos favoritos</li><li><strong>Bônus exclusivos</strong> para novos usuários</li><li><strong>Aplicativo mobile</strong> para apostar a qualquer hora e lugar</li><li><strong>Suporte 24/7</strong> para tirar todas as suas dúvidas</li></ul> <h4>Neste link 👉 <a href='https://br.1x001.com?bf=669c07ae4d465_6600337423' class='botao-chamada'>Cadastre-se Grátis</a></h4>")
# apostas usando o método
#  
# 1 aposta - 23/07/2024
#   Ponte Preta - Villa Nova AC 
#       Total Abaixo de (2.5) gols
#       ganho = R$ 3,65