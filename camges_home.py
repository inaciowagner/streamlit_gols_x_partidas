import scipy.stats as stats

# Função para calcular probabilidades
def calcular_probabilidades(media_gols_time_a, media_gols_time_b, media_gols_sofridos_time_a, media_gols_sofridos_time_b, desvio_padrao_gols):
    # Calcula a média total de gols
    media_total_gols = media_gols_time_a + media_gols_time_b

    # Calcula a média total de gols sofridos
    media_total_gols_sofridos = media_gols_sofridos_time_a + media_gols_sofridos_time_b

    # Utiliza o desvio padrão informado pelo usuário
    desvio_padrao_total_gols = desvio_padrao_gols

    # Calcula a probabilidade para cada cenário (menos de um determinado número de gols)
    probabilidades = []
    for i in range(1, 12):
        # Calcula o z-score para a média total de gols
        z_score = (i - media_total_gols) / desvio_padrao_total_gols

        # Calcula a probabilidade usando a função de distribuição acumulada normal padrão (cdf)
        probabilidade = stats.norm.cdf(z_score)
        probabilidades.append(probabilidade)

    return probabilidades

# Inputs
time_casa = input("Qual é o time de casa? ")
time_fora = input("Qual é o time de fora? ")
media_gols_casa = float(input("Média de gols do time da casa: "))
media_gols_fora = float(input("Média de gols do time de fora: "))
media_gols_sofridos_casa = float(input("Média de gols sofridos pelo time da casa: "))
media_gols_sofridos_fora = float(input("Média de gols sofridos pelo time de fora: "))
desvio_padrao_gols = float(input("Informe o desvio padrão para os gols: "))

# Calcula as probabilidades
probabilidades = calcular_probabilidades(media_gols_casa, media_gols_fora, media_gols_sofridos_casa, media_gols_sofridos_fora, desvio_padrao_gols)

# Exibe os resultados
print(f"\n{time_casa} x {time_fora}\n")
for i, probabilidade in enumerate(probabilidades):
    g = float((i + 1) / 2)
    probabilidade_percentual = probabilidade * 100
    print(f"Menos de {g} gols: {probabilidade_percentual:.1f}%")

print("\nObs: Estes cálculos levam em conta apenas as médias dos times, não consideram fatores como jogar em casa ou fora, nem outras variáveis não matemáticas.")
