import pandas as pd
import utils.dataset as dt
import utils.tools as tools
import os

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


# 1. Quais os países que mais sofreram ataques cibernéticos?
top_countries = dataset['Country'].value_counts().head(10)
print("Top 10 países que mais sofreram ataques cibernéticos:")
print(top_countries)


# 2. Quais os setores mais afetados por esses ataques?
top_setors = dataset['Target Industry'].value_counts().head(10)
print("Top 10 setores mais afetados por ataques cibernéticos:")
print(top_setors)


# 3. Quais os vetores de ataque mais eficientes?
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

print(f'Mais Eficaz de acordo com:\n'
      f'Prejuízo por hora:\n{efficacy_1}\n'
      f'Usuários afetados por hora:\n{efficacy_2}\n'
      f'Prejuízo por usuário afetado:\n{efficacy_3}\n')

# 4 Qual o impacto financeiro desse vetor de ataque?


# 5. Quais as estratégias de mitigação de risco mais eficiente?
# O que define a eficiência de uma estratégia de mitigação?
# Pode ser o que impediu prejuízo financeiro, afetou menos usuários, ou o que levou menos tempo para resolver.


# 6. Quais as fontes de ataques mais comuns conhecidas?
top_source = dataset['Attack Source'].value_counts().head(10)
print("Top 10 fontes de ataques mais comuns:")
print(top_source)


# 7. Qual país teve o maior prejuízo financeiro?
max_loss_country = dataset.groupby('Country')['Financial Loss (in Million $)'].sum().idxmax()
max_loss_value = dataset.groupby('Country')['Financial Loss (in Million $)'].sum()
print(f"País com maior prejuízo financeiro: {max_loss_country} com um total de {max_loss_value[max_loss_country]} milhões de dólares.")


# 8. Qual o vetor de ataque com menor taxa de sucesso?
# O que define a taxa de sucesso de um vetor de ataque?


# 9. Qual a mitigação de risco com menor taxa de sucesso?
# O que define a taxa de sucesso de uma mitigação de risco?


# 10. Qual a proporção de risco de perda em um investimento de mitigação de risco?
# Análise com demanda de dados adicionais para calcular a proporção de risco de perda em um investimento de mitigação de risco.
# Pode ser necessário dados sobre custos de mitigação e frequência de ataques.