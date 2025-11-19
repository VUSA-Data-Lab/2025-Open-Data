# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 00:30:30 2025
@author: doman
"""

import json
import pandas as pd
import matplotlib.pyplot as plt

# Cia kad matytumem visus stulpelius
pd.set_option('display.max_columns', None)
# Cia kad matytumem taisiklingai issidestciusia lentele
pd.set_option('display.width', 200)

# Uzkrauna json duomenis
with open('VilniusData.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Transformuoja JSON duomenys i lentele
df = pd.json_normalize(data['_data'])

# Pirmi keli irasai default = 5
print(df.head())

# Problemos ir kiek tos problemos ivyko
counts = df['problemos_tipas'].value_counts()
print(counts)
print("\n")

# Problemu statusai ir kiek ju yra specifiniai problemai
status_counts = df.groupby('problemos_tipas')['problemos_statusas'].value_counts()
status_counts = status_counts.unstack(fill_value=0)

# Jei noresim rusiuoti
#status_counts_sorted = status_counts.sort_values(by='Išnagrinėta', ascending=False)

print(status_counts)
print("\n")

# Per kiek laiko dienom
df['problem_reg_data'] = pd.to_datetime(df['problem_reg_data'], errors='coerce')
df['problem_issprend_data'] = pd.to_datetime(df['problem_issprend_data'], errors='coerce')

# Naujas stulpelis
df['days_to_solve'] = (df['problem_issprend_data'] - df['problem_reg_data']).dt.days

# Naudoja nauja stulpeli, kad paskaiciuoti per kiek vidutiniskai laiko, problemos buvo issprestos
avg_days = df.groupby('problemos_tipas')['days_to_solve'].mean().sort_values(ascending=False)

print(avg_days)
print("\n")

# Kiek duomenyse pasirodo gatves
counts_adr = df['problem_viet_adresas'].value_counts()

print(counts_adr.head())
print("\n")

# Problemu tipu kiekio grafikas
plt.figure(figsize=(12, 10))
counts.plot(kind='bar')
plt.title('Kiek problemų pagal tipą')
plt.xlabel('Problemos tipas')
plt.ylabel('Kiekis')
plt.tight_layout()
plt.show()

# Problemu isprendimo laiko grafikas
plt.figure(figsize=(12, 10))
avg_days.plot(kind='bar', color='skyblue')
plt.title('Vidutinis sprendimo laikas pagal problemos tipą (dienomis)')
plt.xlabel('Problemos tipas')
plt.ylabel('Dienos')
plt.tight_layout()
plt.show()
