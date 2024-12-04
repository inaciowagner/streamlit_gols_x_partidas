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
st.html("<img src='https://raw.githubusercontent.com/inaciowagner/streamlit_gols_x_partidas/refs/heads/main/camges.png' height='90px' width='272px' alt='CAMGES logo' >")
#st.html("<h3>CAMGES</h3>")
st.html("<h3>Calculadora Avançada de Médias de Gols para Estratégias</h3>")
st.html("<a href='https://youtu.be/2PF0aPN72hc' ><b>Veja um tutorial do app clicando aqui</b></a>")


# Inputs

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
    st.html(f"<h3>{team_a} x {team_b}<h3>")
    for i, probability in enumerate(probabilities):
        g = float((i+1)/2)
        probability = probability * 100
        st.write(f"Menos de {g} gols:", "{:.1f}%".format(probability))



########### Fim do bloco CAMGES #############


st.html("<br><br><br><br><a href='https://github.com/inaciowagner' target='_blank'><b>Conheça meu perfil no GitHub - inaciowagner</b></a>")




