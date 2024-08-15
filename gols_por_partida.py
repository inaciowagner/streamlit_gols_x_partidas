import scipy.stats as stats
import streamlit as st


st.set_page_config(layout="wide", page_icon="⚽", page_title="CAMGES")

col1, col2, col3 = st.columns(3)

with col1:
    st.html("<h3>CAMGES</h3>")
    st.html("<h4>Calculadora Avançada de Médias de Gols para Estratégias</h4>")

 
with col2:
    st.html("<img src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAAsTAAALEwEAmpwYAAADv0lEQVR4nO2ZX2hTVxzHz8ShjIEwNvBFcBvzYU/byx7tgw04yJ+7untOmoE6blKsMivFmjTVhtom01hXa8U/ON2ck7kh6By6nHPjPR0iWBUczD8PG8LYw/bkRGe6Vpuv3FvaJulNlzJM7oV84AfJ5YR8v7/z53fOuYTUqVPnuQKdBcDpdXD2CIKNgLP3iVuACPohGGaFW0xAsJu2BgS9QtwAOMuVMXCfuAG4vweoz2b856EHVxNXTWTOrk2uQvSqq8TXFHC6B5yO24/hmVg7PGAbMSP1+JgR3y9lYmFtDAj273+Jn8vAVGwxdo0flNs/H7z4ySJX9cBaGyOHjK5jlRhBIrEAgg5CsMfgNPn/jFxUX0NWfRtCbQCnQfDgZgjWC86OgtPv4zL5sM3Y/SQs+ysy0i53jX2ZjUfL/p9sWAhOTxUk6SGpBocvdZ2ptDfM6DN67p3SY28UJ2v1Igh2tqRm7K2KgahM5eZjwIxNMj1x3IilLfHnvS+Bs0yJ+EGAvPDcxX8tt0XmK74w7uiRCxDsp6Jix2knqRZpo/vXSsXukH0PPh7+bPp7SvaUbjMmINQNVRN/NtO+rNIJ3GF8OmrWhe/41neGstuHW2U6f1ePFBoYMxcKUk0OG/FvK83+8Wx0Z+Fvz8v2V6GzVgj2Mzj9qybnhKiRrGjydsq+fxJILCBOAkPKhlzyA5w73Yb1cu+cBr66FNtKnAZS/t/R4YUZ4z0K5MmN0GyMmBOXOA0cXPMuoj5L/HTEvPmx3sD4yBctaM2mpw2cMGIbidPAnsDlIvFm9CsGtk1+zsf9uH1kPfbzrj+J08AB9WV0eieKxCf9f6BfkbNMDTW1EKeBAeVIkcgu71MMKm+i2zdW9Hyn72/iRPDNmttI+SdFmkNmSGkzMz0r+/sCO4jTQEZ9b7pynv7QFH/Ber47cKtIfLcvB1KFjdh8gc5iBaV/BDdaXrS2wfuU0akJbMWAcoA4EehsBTj9DYLewo9sufVMsCbL0A8UONQE9PpHkWhYTNwCOD1XcvfjvJWnHMiorxRdAJibMrnOTdkPbirJfgdxEzBv22bEP4CuLiFuAaL5Lev4NzN8+sq1XRUKBzyh8HVPSHvUGAqPeEKR2r8jsK5XZsSPQqpL7do1fhTxe0JhzI5I7UyYtwUQ7F7BWbbsut/YrN20M9AY0mp3zQ5OVxaM/Sfg6uvl2npCWq6MgfvEIRX55FxtndkD+lRFZr8gw5bN1dbTrPlsDORXBTX3vCuwJnKzdm1yFdKuukp8nTrEuTwDVoztBjU5CrsAAAAASUVORK5CYII='>")

with col3:
    st.html("<a href='https://youtu.be/2PF0aPN72hc' ><b>Veja um tutorial do app clicando aqui</b></a>")
    

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



if 'probabilities' in locals():
    st.html(f"<h3>{team_a} x {team_b}<h3>")
    for i, probability in enumerate(probabilities):
        g = float((i+1)/2)
        probability = probability * 100
        st.write(f"Menos de {g} gols:", "{:.1f}%".format(probability))

st.html("<p>Obs: Estes cálculos levam em conta apenas as médias dos times, não leva em consideração o fato do time jogar em casa ou fora, nem outra nem outra variável não matemática.</p>")
st.markdown(" >#### Garanta a melhor experiência de apostas abrindo uma conta no 1XBet")
st.html("<ul><li><strong>Odds sempre competitivas</strong></li><li><strong>Transmissões ao vivo</strong> dos seus jogos favoritos</li><li><strong>Bônus exclusivos</strong> para novos usuários</li><li><strong>Aplicativo mobile</strong> para apostar a qualquer hora e lugar</li><li><strong>Suporte 24/7</strong> para tirar todas as suas dúvidas</li></ul> <h4>Click aqui 👉 <a href='https://br.1x001.com?bf=669c07ae4d465_6600337423' class='botao-chamada'><img src='https://v3.traincdn.com/genfiles/cms/132-395/desktop/media_asset/90f345eff10cbd840aa7aa1b9c46800b.svg' width='100px' alt='logo do 1XBet'>  Cadastre-se Grátis  </a></h4>")

st.html("<a href='bit.ly/mesclapdfs'><b>Conheça o MesclarPDFs, aplicativo que cria um documento único a partir de vários PDFs separados por páginas</b></a>")
