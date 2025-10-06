import pandas as pd
import utils.dataset as dt
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
