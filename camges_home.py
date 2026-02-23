import streamlit as st
import pandas as pd
import scipy.stats as stats

# Configuração da página
st.set_page_config(layout="wide", page_icon="⚽", page_title="CAMGES")

def calculate_poisson_probs(home_avg, away_avg, home_allowed, away_allowed):
    # Força de ataque cruzada com a média de gols sofridos do oponente
    lambda_home = (home_avg + away_allowed) / 2
    lambda_away = (away_avg + home_allowed) / 2

    # P(0) = chance de não marcar gol
    prob_home_zero = stats.poisson.pmf(0, lambda_home)
    prob_away_zero = stats.poisson.pmf(0, lambda_away)

    # Probabilidades individuais e BTTS
    prob_home_score = (1 - prob_home_zero) * 100
    prob_away_score = (1 - prob_away_zero) * 100
    prob_btts = ((1 - prob_home_zero) * (1 - prob_away_zero)) * 100

    return prob_home_score, prob_away_score, prob_btts

def calculate_probabilities(team_a_goals_mean, team_b_goals_mean):
    total_goals_mean = team_a_goals_mean + team_b_goals_mean
    total_goals_std = 1 # Simplificação conforme script original
    
    results = []
    for i in range(1, 12):
        g = float(i / 2)
        # Cálculo usando distribuição normal acumulada (CDF)
        prob_under = stats.norm.cdf(i/2, total_goals_mean, total_goals_std) * 100
        prob_over = 100 - prob_under
        results.append({"gols": g, "under": prob_under, "over": prob_over})
    return results

# Interface e Inputs
st.html("<img src='https://raw.githubusercontent.com/inaciowagner/streamlit_gols_x_partidas/refs/heads/main/camges.png' height='90px' width='272px' alt='CAMGES logo' >")
st.html("<h3>Calculadora Avançada de Médias de Gols para Estratégias</h3>")

team_a = st.text_input("Qual é o time de casa?", value="Crystal Palace")
team_b = st.text_input("Qual é o time de fora", value="Wolves")

col1, col2 = st.columns(2)
with col1:
    home_m = st.number_input(f"Média de gols marcados - {team_a}:", min_value=0.0, value=1.1, step=0.1)
    home_s = st.number_input(f"Média de gols sofridos - {team_a}:", min_value=0.0, value=1.2, step=0.1)
with col2:
    away_m = st.number_input(f"Média de gols marcados - {team_b}:", min_value=0.0, value=0.7, step=0.1)
    away_s = st.number_input(f"Média de gols sofridos - {team_b}:", min_value=0.0, value=1.9, step=0.1)

if st.button('Calcular Probabilidades'):
    # Cálculos principais
    probs_list = calculate_probabilities(home_m, away_m)
    home_score, away_score, btts = calculate_poisson_probs(home_m, away_m, home_s, away_s)

    st.divider()
    st.subheader(f"{team_a} x {team_b}")

    # Exibição das métricas de gols individuais e ambos marcam
    c1, c2, c3 = st.columns(3)
    c1.metric(f"Gol {team_a}", f"{home_score:.1f}%")
    c2.metric(f"Gol {team_b}", f"{away_score:.1f}%")
    c3.metric("Ambos Marcam", f"{btts:.1f}%")

    st.divider()
    
    # Lógica para encontrar os valores específicos solicitados
    # 1. Primeiro "Mais de" mais próximo de 100%
    best_over = max(probs_list, key=lambda x: x['over'] if x['over'] < 100 else 0)
    
    # 2. Primeiro "Menos de" igual a 100% ou mais próximo
    best_under = next((x for x in probs_list if x['under'] >= 99.9), probs_list[-1])

    # Saída formatada conforme o print de referência
    st.write(f"Menos de {best_over['gols']} gols: {best_over['under']:.1f}% < - > **Mais de {best_over['gols']} gols: {best_over['over']:.1f}%**")
    st.write("")
    st.write(f"**Menos de {best_under['gols']} gols: {best_under['under']:.1f}%** < - > Mais de {best_under['gols']} gols: {best_under['over']:.1f}%")

st.html("<br><br><a href='https://github.com/inaciowagner' target='_blank'><b>Conheça meu perfil no GitHub - inaciowagner</b></a>")
