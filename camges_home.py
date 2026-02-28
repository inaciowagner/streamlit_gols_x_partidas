import scipy.stats as stats
import streamlit as st
import pandas as pd
import numpy as np
from scipy import integrate

st.set_page_config(layout="wide", page_icon="⚽", page_title="CAMGES - Calculadora de Probabilidades")

# CSS personalizado para melhorar a estética
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .probability-card {
        background-color: #000000;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2a5298;
        margin: 0.5rem 0;
    }
    .highlight-prob {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1e3c72;
    }
    .botao-chamada {
        background: linear-gradient(90deg, #ff8c00 0%, #ff6b00 100%);
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin: 1rem 0;
    }
    .botao-chamada:hover {
        background: linear-gradient(90deg, #ff6b00 0%, #ff4500 100%);
        color: white;
    }
    .footer {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 2rem;
    }
    .odds-table {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header principal
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown("""
    <div class="main-header">
        <h1>⚽ CAMGES</h1>
        <h3>Calculadora Avançada de Médias de Gols para Estratégias</h3>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/54/54523.png", width=80)
    
with col3:
    st.markdown('''### Aposte com sabedoria!''')

def calculate_poisson_probability(mean, k):
    """Calcula probabilidade de marcar exatamente k gols usando Poisson"""
    return stats.poisson.pmf(k, mean)

def calculate_team_scores_probability(mean):
    """Calcula probabilidade do time marcar pelo menos 1 gol"""
    return 1 - stats.poisson.pmf(0, mean)

def calculate_btts_probability(mean_a, mean_b):
    """Calcula probabilidade de ambos marcarem (BTTS)"""
    prob_a_scores = calculate_team_scores_probability(mean_a)
    prob_b_scores = calculate_team_scores_probability(mean_b)
    
    # Considerando independência (aproximação)
    prob_btts = prob_a_scores * prob_b_scores
    return prob_btts

def calculate_match_probabilities(mean_home, mean_away, mean_home_conceded, mean_away_conceded):
    """
    Calcula probabilidades usando distribuição de Poisson ajustada
    """
    # Ajustando as médias considerando defesas e ataques
    home_attack = mean_home
    away_attack = mean_away
    home_defense = mean_home_conceded
    away_defense = mean_away_conceded
    
    # Médias ajustadas
    lambda_home = max(0.1, (home_attack + away_defense) / 2)  # Evitar médias muito baixas
    lambda_away = max(0.1, (away_attack + home_defense) / 2)
    
    # Probabilidades de cada time marcar
    prob_home_scores = 1 - stats.poisson.pmf(0, lambda_home)
    prob_away_scores = 1 - stats.poisson.pmf(0, lambda_away)
    prob_btts = prob_home_scores * prob_away_scores
    
    # Probabilidades de placares exatos (até 5 gols)
    max_goals = 5
    score_matrix = np.zeros((max_goals + 1, max_goals + 1))
    total_prob = 0
    
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            prob = stats.poisson.pmf(i, lambda_home) * stats.poisson.pmf(j, lambda_away)
            score_matrix[i, j] = prob
            total_prob += prob
    
    # Normalizar para garantir soma = 1
    score_matrix = score_matrix / total_prob
    
    return {
        'home_scores': prob_home_scores,
        'away_scores': prob_away_scores,
        'btts': prob_btts,
        'score_matrix': score_matrix,
        'lambda_home': lambda_home,
        'lambda_away': lambda_away
    }

def calculate_specific_under_over_probabilities(mean_home, mean_away, mean_home_conceded, mean_away_conceded):
    """Calcula probabilidades específicas para Under/Over 0.5, 1.5, 2.5, 3.5, 4.5, 5.5"""
    lambda_home = max(0.1, (mean_home + mean_away_conceded) / 2)
    lambda_away = max(0.1, (mean_away + mean_home_conceded) / 2)
    lambda_total = lambda_home + lambda_away
    
    # Valores específicos para cálculo
    goals_thresholds = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
    results = []
    
    for threshold in goals_thresholds:
        # Para distribuição Poisson, P(Under X.5) = P(≤ floor(X.5))
        # Como X.5, floor é o inteiro abaixo (ex: 1.5 -> 1)
        max_goals = int(threshold)
        prob_under = stats.poisson.cdf(max_goals, lambda_total)
        prob_over = 1 - prob_under
        
        results.append({
            'threshold': threshold,
            'under_prob': prob_under * 100,  # Converter para porcentagem
            'over_prob': prob_over * 100
        })
    
    return results

# Sidebar melhorada
with st.sidebar:
    st.markdown("### 🏆 Dados dos Times")
    st.markdown("---")
    
    team_a = st.text_input("🏠 Time da casa:", placeholder="Ex: Flamengo")
    team_b = st.text_input("✈️ Time visitante:", placeholder="Ex: Palmeiras")
    
    st.markdown("### ⚽ Médias de Gols")
    col_a, col_b = st.columns(2)
    with col_a:
        team_a_goals_mean = st.number_input("Gols marcados (casa):", min_value=0.0, max_value=10.0, value=1.5, step=0.1)
        team_a_goals_allowed_mean = st.number_input("Gols sofridos (casa):", min_value=0.0, max_value=10.0, value=1.2, step=0.1)
    with col_b:
        team_b_goals_mean = st.number_input("Gols marcados (fora):", min_value=0.0, max_value=10.0, value=1.3, step=0.1)
        team_b_goals_allowed_mean = st.number_input("Gols sofridos (fora):", min_value=0.0, max_value=10.0, value=1.4, step=0.1)
    
    st.markdown("---")
    calculate_button = st.button('📊 Calcular Probabilidades', use_container_width=True)

# Área principal
if calculate_button and team_a and team_b:
    # Cálculos
    match_probs = calculate_match_probabilities(
        team_a_goals_mean, team_b_goals_mean,
        team_a_goals_allowed_mean, team_b_goals_allowed_mean
    )
    
    specific_probs = calculate_specific_under_over_probabilities(
        team_a_goals_mean, team_b_goals_mean,
        team_a_goals_allowed_mean, team_b_goals_allowed_mean
    )
    
    # Título do confronto
    st.markdown(f"<h2 style='text-align: center; color: #1e3c72;'>{team_a} 🆚 {team_b}</h2>", unsafe_allow_html=True)
    
    # Métricas principais em cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="probability-card">
            <h4>🏠 {team_a}</h4>
            <div class="highlight-prob">{match_probs['home_scores']*100:.1f}%</div>
            <p>marcar gol</p>
            <small>Média: {match_probs['lambda_home']:.2f} gols</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="probability-card">
            <h4>✈️ {team_b}</h4>
            <div class="highlight-prob">{match_probs['away_scores']*100:.1f}%</div>
            <p>marcar gol</p>
            <small>Média: {match_probs['lambda_away']:.2f} gols</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="probability-card">
            <h4>🤝 Ambos marcam</h4>
            <div class="highlight-prob">{match_probs['btts']*100:.1f}%</div>
            <p>(BTTS - Both Teams To Score)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="probability-card">
            <h4>📊 Média Total</h4>
            <div class="highlight-prob">{(match_probs['lambda_home'] + match_probs['lambda_away']):.2f}</div>
            <p>gols esperados</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabela de probabilidades Under/Over específicas
    st.markdown("### 📈 Probabilidades de Gols - Mercados Populares")
    st.markdown("---")
    
    # Criando DataFrame para exibição
    df_specific = pd.DataFrame(specific_probs)
    df_specific.columns = ['Linha de Gols', 'Under (%)', 'Over (%)']
    
    # Adicionando colunas de odds aproximadas (1/probabilidade)
    df_specific['Odd Under'] = (100 / df_specific['Under (%)']).round(2)
    df_specific['Odd Over'] = (100 / df_specific['Over (%)']).round(2)
    
    # Formatando para exibição
    df_display = df_specific.copy()
    df_display['Under (%)'] = df_display['Under (%)'].round(1)
    df_display['Over (%)'] = df_display['Over (%)'].round(1)
    
    # Exibindo tabela completa
    st.markdown('<div class="odds-table">', unsafe_allow_html=True)
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Linha de Gols": st.column_config.TextColumn("Linha", width="small"),
            "Under (%)": st.column_config.NumberColumn("Under %", format="%.1f%%", width="small"),
            "Over (%)": st.column_config.NumberColumn("Over %", format="%.1f%%", width="small"),
            "Odd Under": st.column_config.NumberColumn("Odd Under", format="%.2f", width="small"),
            "Odd Over": st.column_config.NumberColumn("Odd Over", format="%.2f", width="small")
        }
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Heatmap de placares mais prováveis
    st.markdown("### 🎯 Placas Mais Prováveis")
    st.markdown("---")
    
    # Pegando os 5 placares mais prováveis
    score_probs = []
    for i in range(6):
        for j in range(6):
            prob = match_probs['score_matrix'][i, j] * 100
            if prob > 0.5:  # Mostrar apenas probabilidades > 0.5%
                score_probs.append({
                    'Placar': f"{i} x {j}",
                    'Probabilidade': f"{prob:.1f}%",
                    'Time Casa': i,
                    'Time Fora': j,
                    'Prob': prob
                })
    
    score_probs.sort(key=lambda x: x['Prob'], reverse=True)
    
    if score_probs:
        cols = st.columns(3)
        for idx, score in enumerate(score_probs[:6]):
            with cols[idx % 3]:
                st.markdown(f"""
                <div style="background-color: {'#2a5298' if idx == 0 else "#e8e8ea"}; 
                            padding: 10px; 
                            border-radius: 5px; 
                            text-align: center;
                            color: {'white' if idx == 0 else 'black'};
                            margin: 5px;">
                    <h3>{score['Placar']}</h3>
                    <h4>{score['Probabilidade']}</h4>
                </div>
                """, unsafe_allow_html=True)

else:
    st.info("👈 Preencha os dados dos times na barra lateral e clique em 'Calcular Probabilidades'")

# Rodapé
st.markdown("---")

# Link do GitHub
st.markdown("<div style='text-align: center; padding: 1rem;'><a href='https://github.com/inaciowagner' target='_blank'><b>👨‍💻 Conheça meu perfil no GitHub - inaciowagner</b></a></div>", unsafe_allow_html=True)
