import pandas as pd
import utils.dataset as dt
import utils.tools as tools
import os
import matplotlib.pyplot as plt
import pycountry

dataset_path = "dataset/Global_Cybersecurity_Threats_2015-2024.csv"

if not os.path.exists(dataset_path):
    dt.download_dataset()

"""
COLUNAS DO DATASET:
- Country
- Year
- Attack Type
- Target Industry
- Financial Loss (in Million $)
- Number of Affected Users
- Attack Source
- Security Vulnerability Type
- Defense Mechanism Used
- Incident Resolution Time (in Hours)
"""

try:
    dataset = pd.read_csv(dataset_path)
    print(dataset.head())
except Exception as e:
    print("Ocorreu um erro ao carregar o dataset:", e)


# Limpeza e pré-processamento dos dados
dataset = tools.preprocess_data(dataset)


# RESPONDENDO AS PERGUNTAS!


# 1. Quais os países que mais sofreram ataques cibernéticos (por ano)?
attacks_by_country_year = dataset.groupby(['Year', 'Country']).size().reset_index(name='Attack Count')
avg_attacks_country = attacks_by_country_year.groupby('Country')['Attack Count'].mean().sort_values(ascending=False).head(10)
print("Top 10 países com maior média anual de ataques cibernéticos:")
print(avg_attacks_country)
# Gráfico
plt.figure(figsize=(10, 6))
bars = avg_attacks_country.plot(kind='barh', color='#2c3e50') # Azul escuro/cinza profissional
plt.title('Top 10 Países por Média Anual de Incidentes Cibernéticos (2015–2024)', fontsize=14, pad=15)
plt.xlabel('Média Anual de Incidentes', fontsize=12)
plt.ylabel('País', fontsize=12)
plt.gca().invert_yaxis()
plt.grid(axis='x', linestyle='--', alpha=0.7)
# Adicionando rótulos de dados
for index, value in enumerate(avg_attacks_country):
    plt.text(value, index, f'{value:.0f}', ha='left', va='center')
plt.tight_layout()
plt.show()

# 2. Quais indústrias são mais afetadas por esses ataques (por ano)?
attacks_by_sector_year = dataset.groupby(['Year', 'Target Industry']).size().reset_index(name='Attack Count')
avg_attacks_sector = attacks_by_sector_year.groupby('Target Industry')['Attack Count'].mean().sort_values(ascending=False).head(10)
print("Top 10 setores com maior média anual de ataques cibernéticos:")
print(avg_attacks_sector)
# Gráfico
plt.figure(figsize=(12, 6))
avg_attacks_sector.plot(kind='bar', color='#e67e22')
plt.title('Top 10 Setores por Média Anual de Incidentes Cibernéticos (2015–2024)', fontsize=14, pad=15)
plt.ylabel('Média Anual de Incidentes', fontsize=12)
plt.xlabel('Setor', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()


# 3. Quais os vetores de ataque mais eficientes e menos eficientes?
# O que define a eficiência de um vetor de ataque?
# Pode ser o que causa mais prejuízo financeiro, ou o que afeta mais usuários, ou o que leva mais tempo para resolver.
avg_financial_loss = dataset.groupby('Attack Type')['Financial Loss (in Million $)'].mean()
avg_resolution_time = dataset.groupby('Attack Type')['Incident Resolution Time (in Hours)'].mean()
avg_affected_users = dataset.groupby('Attack Type')['Number of Affected Users'].mean()

# Definirei 3 tipos de eficacia
# 1. Prejuízo / hora
efficacy_1 = avg_financial_loss/avg_resolution_time
efficacy_1 = efficacy_1.nlargest(10)

# 2. Usuários afetados / hora
efficacy_2 = avg_affected_users/avg_resolution_time
efficacy_2 = efficacy_2.nlargest(10)

# 3. Prejuízo / Usuário
efficacy_3 = avg_financial_loss/avg_affected_users
efficacy_3 = efficacy_3.nlargest(10)

efficacy_2 /= 1000
efficacy_3 *= 1000000

print(f'\nMais Eficaz de acordo com:\n'
      f'Prejuízo por hora:\n{efficacy_1}\n'
      f'Usuários afetados por hora:\n{efficacy_2}\n'
      f'Prejuízo por usuário afetado:\n{efficacy_3}\n\n')
# Gráficos
# Título fora da tela
fig, axes = plt.subplots(1, 3, figsize=(18, 7), sharey=False)
# (mantive a logica mas plotei de um jeito diferente pra ficar mais visual)
# Paletas de cores
cmap_p = plt.colormaps['Reds']
cmap_u = plt.colormaps['Oranges']
cmap_r = plt.colormaps['Blues']

cores_p = [cmap_p(i / len(efficacy_1)) for i in range(len(efficacy_1))]
cores_u = [cmap_u(i / len(efficacy_2)) for i in range(len(efficacy_2))]
cores_r = [cmap_r(i / len(efficacy_3)) for i in range(len(efficacy_3))]

# Gráfico 1: Prejuízo por hora
efficacy_1.plot(kind='bar', ax=axes[0], title='Eficácia 1: Prejuízo/Hora', color=cores_p, edgecolor='black')
axes[0].set_ylabel('Eficácia (Milhões US$/Hora)')
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45, ha='right')
axes[0].grid(axis='y', linestyle='--', alpha=0.5)

# Gráfico 2: Usuários afetados por hora
efficacy_2.plot(kind='bar', ax=axes[1], title='Eficácia 2: Usuários Afetados/Hora', color=cores_u, edgecolor='black')
axes[1].set_ylabel('Eficácia (Milhares de Usuários Afetados/Hora)')
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45, ha='right')
axes[1].grid(axis='y', linestyle='--', alpha=0.5)

# Gráfico 3: Prejuízo por usuário
efficacy_3.plot(kind='bar', ax=axes[2], title='Eficácia 3: Prejuízo/Usuário', color=cores_r, edgecolor='black')
axes[2].set_ylabel('Eficácia (US$/Usuário)')
axes[2].set_xticklabels(axes[2].get_xticklabels(), rotation=45, ha='right')
axes[2].grid(axis='y', linestyle='--', alpha=0.5)

fig.suptitle('Top 10 Vetores de Ataque Mais Eficazes por Métrica', fontsize=16, y=1.02)
plt.tight_layout()
plt.show()


# 4 Qual o impacto financeiro desse vetor de ataque? (Descobrimos que é o DDoS)
total_ddos_loss = dataset['Financial Loss (in Million $)'].sum()
ddos_loss_by_year = dataset.groupby('Year')['Financial Loss (in Million $)'].sum()
avg_ddos_loss_per_year = ddos_loss_by_year.mean()

print(f"\n--- Impacto Financeiro do DDoS ---")
print(f"Prejuízo total (2015-2024): US$ {total_ddos_loss:,.2f} milhões")
print(f"Prejuízo médio anual: US$ {avg_ddos_loss_per_year:,.2f} milhões\n")
# Gráfico do prejuízo anual por DDoS
plt.figure(figsize=(10, 5))
ddos_loss_by_year.plot(kind='line', marker='o', color='#c0392b', linewidth=3, markersize=8) # Vermelho escuro
plt.title('Impacto Financeiro Total por Ano (2015-2024)', fontsize=14, pad=15)
plt.ylabel('Prejuízo (em milhões de US$)', fontsize=12)
plt.xlabel('Ano', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(ddos_loss_by_year.index) # Garante que todos os anos sejam mostrados

# Anotação de Pico
max_year = ddos_loss_by_year.idxmax()
max_value = ddos_loss_by_year.max()
plt.annotate(f'Pico: {max_value:,.0f}M',
             xy=(max_year, max_value),
             xytext=(max_year, max_value * 0.9),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=8),
             ha='center')

plt.tight_layout()
plt.show()

# 5. Quais as estratégias de mitigação de risco mais eficiente e menos eficiente?
# O que define a eficiência de uma estratégia de mitigação?
# Pode ser o que impediu prejuízo financeiro, afetou menos usuários, ou o que levou menos tempo para resolver.

# Vou copiar a estratégia do Tales, mas fazendo o inverso, ou seja, quanto menor o prejuízo, mais eficiente é a defesa.
avg_loss_by_defense = dataset.groupby('Defense Mechanism Used')['Financial Loss (in Million $)'].mean()
avg_users_by_defense = dataset.groupby('Defense Mechanism Used')['Number of Affected Users'].mean()
avg_time_by_defense = dataset.groupby('Defense Mechanism Used')['Incident Resolution Time (in Hours)'].mean()

eff_financial = 1 / avg_loss_by_defense
eff_users = 1 / avg_users_by_defense
eff_time = 1 / avg_time_by_defense

print("\nEficiência das estratégias de mitigação de risco (quanto maior, melhor):")
print("\nEficiência baseada em prejuízo financeiro médio:")
print(eff_financial.sort_values(ascending=False).head(10))
print("\nEficiência baseada em número médio de usuários afetados:")
print(eff_users.sort_values(ascending=False).head(10))
print("\nEficiência baseada em tempo médio de resolução de incidentes:")
print(eff_time.sort_values(ascending=False).head(10))

# Combinação das três métricas (média normalizada)
efficiency_score = (eff_financial + eff_users + eff_time) / 3

# Ordenar do mais eficiente para o menos
efficiency_score = efficiency_score.sort_values(ascending=False)

print("\n\nRanking geral de eficiência dos mecanismos de defesa (quanto maior, melhor):")
print(efficiency_score)

# Gráfico

top_defenses = efficiency_score.head(10)
plt.figure(figsize=(10, 6))
bars = top_defenses.plot(kind='barh', color='#2ecc71') # Verde vibrante
plt.title('Top 10 Mecanismos de Defesa Mais Eficientes (Índice Combinado)', fontsize=14, pad=15)
plt.xlabel('Índice de Eficiência (Quanto maior, melhor)', fontsize=12)
plt.ylabel('Mecanismo de Defesa', fontsize=12)
plt.gca().invert_yaxis()
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Adicionando rótulos de dados
for index, value in enumerate(top_defenses):
    plt.text(value, index, f'{value:.2f}', ha='left', va='center')

plt.tight_layout()
plt.show()

# 6. Quais as fontes de ataques mais comuns conhecidas?
top_source = dataset['Attack Source'].value_counts().head(10)
print("Top 10 fontes de ataques mais comuns:") # Fazer uma torta (gráfica)
print(top_source)

# Gráfico Refinado (Barras Horizontais)
plt.figure(figsize=(10, 6))
top_source.sort_values().plot(kind='barh', color='#f39c12') # Amarelo/Laranja
plt.title('Top 10 Fontes de Ataques Cibernéticos Mais Comuns', fontsize=14, pad=15)
plt.xlabel('Número de Ocorrências', fontsize=12)
plt.ylabel('Fonte do Ataque', fontsize=12)
# Não inverte o Y-axis se usou sort_values().plot()
plt.grid(axis='x', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

# 7. Qual país teve o maior prejuízo financeiro?
max_loss_country = dataset.groupby('Country')['Financial Loss (in Million $)'].sum().idxmax()
max_loss_value = dataset.groupby('Country')['Financial Loss (in Million $)'].sum()
print(f"País com maior prejuízo financeiro: {max_loss_country} com um total de {max_loss_value[max_loss_country]} milhões de dólares.")
loss_by_country = dataset.groupby('Country')['Financial Loss (in Million $)'].sum().sort_values(ascending=False).head(10)
# Gráfico
plt.figure(figsize=(10, 6))
bars = loss_by_country.plot(kind='barh', color='#34495e')
plt.title('Top 10 Países por Prejuízo Financeiro Total (Milhões de US$)', fontsize=14, pad=15)
plt.xlabel('Perdas Totais (em Milhões de US$)', fontsize=12)
plt.ylabel('País', fontsize=12)
plt.gca().invert_yaxis()
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Adicionar formatação de milhões ao eixo X (opcional, mas profissional)
from matplotlib.ticker import FuncFormatter
def millions_formatter(x, pos):
    return f'{x:,.0f}M'
plt.gca().xaxis.set_major_formatter(FuncFormatter(millions_formatter))

plt.tight_layout()
plt.show()


# 8. Qual o tempo médio de resolução de incidentes por tipo de ataque?
avg_resolution_by_attack = dataset.groupby('Attack Type')['Incident Resolution Time (in Hours)'].mean().sort_values()
print("Tempo médio de resolução de incidentes por tipo de ataque:") # Mudar gráfico e/ou escala
print(avg_resolution_by_attack)
# Gráfico
plt.figure(figsize=(12, 6))
avg_resolution_by_attack.plot(kind='bar', color='#8e44ad') # Roxo
plt.title('Tempo Médio de Resolução de Incidentes por Tipo de Ataque', fontsize=14, pad=15)
plt.ylabel('Tempo Médio (em Horas)', fontsize=12)
plt.xlabel('Tipo de Ataque', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()


# 9. Quais os tipos de vulnerabilidades de segurança mais exploradas?
top_vulnerabilities = dataset['Security Vulnerability Type'].value_counts().head(10)
print("Vulnerabilidades de segurança mais exploradas:")
print(top_vulnerabilities)
#Gráfico
plt.figure(figsize=(10, 6))
bars = top_vulnerabilities.plot(kind='barh', color='#d35400') # Laranja/Marrom
plt.title('Top 10 Vulnerabilidades de Segurança Mais Exploradas', fontsize=14, pad=15)
plt.xlabel('Número de Ocorrências', fontsize=12)
plt.ylabel('Vulnerabilidade', fontsize=12)
plt.gca().invert_yaxis()
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Adicionando rótulos de dados
for index, value in enumerate(top_vulnerabilities):
    plt.text(value, index, f'{value}', ha='left', va='center')

plt.tight_layout()
plt.show()

# 10. Qual a proporção de crescimento/decrescimento dos setores?
# Falta mudar a escala
sector_trends = dataset.groupby(['Year', 'Target Industry']).size().unstack(fill_value=0)

sector_growth = sector_trends.pct_change().fillna(0).mean().sort_values(ascending=False).head(10)

print("Top 10 Média de crescimento percentual de ataques por setor (2015-2024):")
print(sector_growth)

plt.figure(figsize=(10, 6))
# Coloquei as cores de crescimento pra ver e decrescimento pra vermelho por conveniencia, se tiverem ideias melhores podem mudar
colors = ['#27ae60' if x >= 0 else '#c0392b' for x in sector_growth.sort_values(ascending=True)]
sector_growth.sort_values(ascending=True).plot(kind='barh', color=colors)

plt.title('Top 10 Setores por Crescimento Médio Anual de Incidentes', fontsize=14, pad=15)
plt.xlabel('Taxa Média de Crescimento de Incidentes (%)', fontsize=12)
plt.ylabel('Setor', fontsize=12)
plt.gca().invert_yaxis()

# Formata o eixo X para mostrar o %
plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.0%}'))

plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


# EXPORTANDO DADOS REAIS DOS PAÍSES!

globe_data = dataset.groupby('Country').agg({
    'Financial Loss (in Million $)': 'sum',
    'Number of Affected Users': 'sum',
}).reset_index()


attack_counts = dataset['Country'].value_counts().reset_index()
attack_counts.columns = ['Country', 'Attack Count']
globe_data = pd.merge(globe_data, attack_counts, on='Country', how='left')

def get_country_lat_lon(country_name):
    coords = {
        'USA': (38, -97),
        'China': (35, 103),
        'Russia': (61, 100),
        'Germany': (51, 10),
        'Brazil': (-10, -55),
        'India': (20, 77),
        'UK': (55, -3),
        'France': (46, 2),
        'Japan': (36, 138),
        'Australia': (-25, 133),
    }
    return coords.get(country_name, (0, 0))  # padrão: (0,0)

globe_data[['Latitude', 'Longitude']] = globe_data['Country'].apply(
    lambda c: pd.Series(get_country_lat_lon(c))
)

globe_data = globe_data[[
    'Country', 'Latitude', 'Longitude',
    'Attack Count', 'Financial Loss (in Million $)', 'Number of Affected Users'
]]



os.makedirs('data', exist_ok=True)
globe_data.to_csv('data/globe_data.csv', index=False)
print("\nDados exportados para 'data/globe_data.csv' com sucesso!")
print(globe_data.head())

