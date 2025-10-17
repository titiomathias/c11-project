import pandas as pd
import utils.dataset as dt
import utils.tools as tools
import os
import matplotlib.pyplot as plt

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
avg_attacks_country.plot(kind='barh', color='darkred', figsize=(10,6))
plt.title('Top 10 países com maior média anual de ataques cibernéticos (2015–2024)')
plt.xlabel('Média anual de ataques')
plt.ylabel('País')
plt.gca().invert_yaxis()
plt.show()


# 2. Quais indústrias são mais afetadas por esses ataques (por ano)?
attacks_by_sector_year = dataset.groupby(['Year', 'Target Industry']).size().reset_index(name='Attack Count')
avg_attacks_sector = attacks_by_sector_year.groupby('Target Industry')['Attack Count'].mean().sort_values(ascending=False).head(10)
print("Top 10 setores com maior média anual de ataques cibernéticos:")
print(avg_attacks_sector)
# Gráfico
avg_attacks_sector.plot(kind='bar', color='orange', figsize=(10,6))
plt.title('Setores com maior média anual de ataques cibernéticos (2015–2024)')
plt.ylabel('Média anual de ataques')
plt.xticks(rotation=45, ha='right')
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

print(f'\nMais Eficaz de acordo com:\n'
      f'Prejuízo por hora:\n{efficacy_1}\n'
      f'Usuários afetados por hora:\n{efficacy_2}\n'
      f'Prejuízo por usuário afetado:\n{efficacy_3}\n\n')
# Gráficos
fig, axes = plt.subplots(1, 3, figsize=(18,6))

efficacy_1.plot(kind='bar', ax=axes[0], title='Prejuízo por hora', color='crimson')
efficacy_2.plot(kind='bar', ax=axes[1], title='Usuários afetados por hora', color='darkorange')
efficacy_3.plot(kind='bar', ax=axes[2], title='Prejuízo por usuário', color='steelblue')

for ax in axes:
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

plt.suptitle('Eficiência média dos vetores de ataque', fontsize=14)
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
ddos_loss_by_year.plot(kind='line', marker='o', color='red', figsize=(10,5))
plt.title('Impacto Financeiro Total por Ano (2015-2024)')
plt.ylabel('Prejuízo (em milhões de US$)')
plt.xlabel('Ano')
plt.grid(True, linestyle='--', alpha=0.6)
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
plt.figure(figsize=(10,5))
top_defenses.plot(kind='barh', color='green')
plt.title('Mecanismos de defesa mais eficientes')
plt.xlabel('Índice de eficiência')
plt.gca().invert_yaxis()
plt.show()

# 6. Quais as fontes de ataques mais comuns conhecidas?
top_source = dataset['Attack Source'].value_counts().head(10)
print("Top 10 fontes de ataques mais comuns:")
print(top_source)
# Gráfico
top_source.plot(kind='pie', autopct='%1.1f%%', figsize=(7,7), startangle=90, colormap='tab20')
plt.title('Fontes de ataques mais comuns')
plt.ylabel('')
plt.show()


# 7. Qual país teve o maior prejuízo financeiro?
max_loss_country = dataset.groupby('Country')['Financial Loss (in Million $)'].sum().idxmax()
max_loss_value = dataset.groupby('Country')['Financial Loss (in Million $)'].sum()
print(f"País com maior prejuízo financeiro: {max_loss_country} com um total de {max_loss_value[max_loss_country]} milhões de dólares.")
loss_by_country = dataset.groupby('Country')['Financial Loss (in Million $)'].sum().sort_values(ascending=False).head(10)
# Gráfico
loss_by_country.plot(kind='barh', color='darkblue', figsize=(10,6))
plt.title('Top 10 países com maior prejuízo financeiro')
plt.xlabel('Perdas totais (em milhões de US$)')
plt.gca().invert_yaxis()
plt.show()


# 8. Qual o tempo médio de resolução de incidentes por tipo de ataque?
avg_resolution_by_attack = dataset.groupby('Attack Type')['Incident Resolution Time (in Hours)'].mean().sort_values()
print("Tempo médio de resolução de incidentes por tipo de ataque:")
print(avg_resolution_by_attack)
# Gráfico
avg_resolution_by_attack.plot(kind='bar', color='purple', figsize=(10,6))
plt.title('Tempo médio de resolução de incidentes por tipo de ataque')
plt.ylabel('Horas (média)')
plt.xticks(rotation=45, ha='right')
plt.show()


# 9. Quais os tipos de vulnerabilidades de segurança mais exploradas?
top_vulnerabilities = dataset['Security Vulnerability Type'].value_counts().head(10)
print("Vulnerabilidades de segurança mais exploradas:")
print(top_vulnerabilities)
#Gráfico
top_vulnerabilities.plot(kind='barh', color='darkorange', figsize=(10,6))
plt.title('Vulnerabilidades de segurança mais exploradas')
plt.xlabel('Número de ocorrências')
plt.gca().invert_yaxis()
plt.show()

# 10. Qual a proporção de crescimento/decrescimento dos setores?
sector_trends = dataset.groupby(['Year', 'Target Industry']).size().unstack(fill_value=0)

sector_growth = sector_trends.pct_change().mean().sort_values(ascending=False)

print("Média de crescimento percentual de ataques por setor nos últimos 10 anos:")
print(sector_growth)
# Gráfico
# Preciso achar uma forma de deixar esse gráfico mais legível