# -*- coding: utf-8 -*-
"""SMTT.ipynb
Importando as libs
"""

import pandas as pd
import numpy as np
import math

from sklearn import preprocessing

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import seaborn as sns

"""Lendo o dataset"""

df = pd.read_csv('viagens.csv')
df.head()

df.tail()

df.info()

"""Tratando os dados """

# Remove a primeira coluna, que representa o índice
df = df.drop(['Unnamed: 0'], axis=1)

# Identificando os dados faltantes
df.isnull().sum()

# Obtendo a média para substituir nos dados faltantes
dtr_media = df['duracao_total_realizada'].mean()
dr_media = df['duracao_realizada'].mean()

# Arredondando a média
dtr_media = math.floor(dtr_media)
dr_media = math.floor(dr_media)

# Dando update nos dados faltantes em 'duracao_total_realizada' e 'duracao_realizada'
df.update(df['duracao_total_realizada'].fillna(dtr_media))
df.update(df['duracao_realizada'].fillna(dr_media))

# As viagens não realizadas não possuem valor em 'hora_realizada'. Dessa forma, uma vez que não será analisado o cumprimento de viagem, então serão removidas as linhas cujo valor em 'hora_realizada' esteja faltando.
print('Antes de remover as linhas: ', df.shape)
df = df.dropna(axis=0)
print('Depois de remover as linhas: ', df.shape)

# Após update em 'duracao_total_realizada' e 'duracao_realizada'
df.isnull().sum()

# Renomear o índice do dataset porque ao remover os dados faltantes em 'hora_realizada' o índice ficou com alguns buracos.
index = []
for j in range(len(df)):
  index.append(j)

df = df.set_index([pd.Index(index)])
df

"""Transformando as variáveis categóricas em variáveis numéricas """

# Criando variáveis 'adiantamento' e 'atraso' a partir de 'hora_prevista' e 'hora_realizada'
adiantamento = pd.DataFrame(np.where(df['hora_prevista']>df['hora_realizada'], 1, 0), columns=['adiantamento'])
atraso = pd.DataFrame(np.where(df['hora_prevista']<df['hora_realizada'], 1, 0), columns=['atraso'])

adiantamento.head()
atraso.head()

# Trocando o nome da empresa por um inteiro
label = preprocessing.LabelEncoder()

empresa = {'empresa': label.fit_transform(df['empresa'])}
empresa_df = pd.DataFrame(data=empresa)

empresa_dict = dict(zip([0,1,2,3], label.classes_)) # dicionário 
empresa_df

# Trocando o sentido da viagem (ida e volta) por um inteiro
label = preprocessing.LabelEncoder()

sentido = {'sentido': label.fit_transform(df['sentido_viagem'])}
sentido_df = pd.DataFrame(data=sentido) # 0 = ida, 1 = volta

sentido_dict = dict(zip([0,1], label.classes_)) # dicionário 
sentido_df

# Criando uma variável para cada valor único de 'sentido_viagem'
numero_linha = df['numero_linha']
numero_linha.head()

# Features/Variáveis selecionadas para o dataset
# adiantamento, atraso, empresa e sentido_viagem
data = pd.concat([adiantamento, atraso, empresa_df, numero_linha, sentido_df], axis=1)
data

"""Contagem do atraso e do adiantamento em relação as variáveis para visualização dos dados"""

# Geral
soma_at = data['atraso'].sum()
soma_ad = data['adiantamento'].sum()

# Empresa
e_at = data[['empresa', 'atraso']].groupby(['empresa'], as_index=False).sum().sort_values(by='empresa')
e_ad = data[['empresa', 'adiantamento']].groupby(['empresa'], as_index=False).sum().sort_values(by='empresa')

# Sentido
sen_at = data[['sentido', 'atraso']].groupby(['sentido'], as_index=False).sum().sort_values(by='sentido')
sen_ad = data[['sentido', 'adiantamento']].groupby(['sentido'], as_index=False).sum().sort_values(by='sentido')

# Número de linha
nl_at = data[['numero_linha', 'atraso']].groupby(['numero_linha'], as_index=False).sum().sort_values(by='numero_linha')
nl_ad = data[['numero_linha', 'adiantamento']].groupby(['numero_linha'], as_index=False).sum().sort_values(by='numero_linha')

nl_at_40 = nl_at.loc[0:40]
nl_ad_40 = nl_ad.loc[0:40]

nl_at_80 = nl_at.loc[41:80]
nl_ad_80 = nl_ad.loc[41:80]

e_at

"""Explorando os dados a partir de gráficos para descrever e resumir as features."""

#VISUALIZAÇÃO GERAL DE ATRASO
X = np.arange(1)
fig = plt.figure(figsize = (4, 6))
indx = np.arange(2)
ax = fig.add_axes([0,0,1,1])
ax.bar(X + 0.4, soma_ad, color = 'pink', width = 0.2, label = 'adiantamento')
ax.bar(X + 0.6, soma_at, color = 'r', width = 0.2, label = 'atraso')
ax.set_xticks(indx)
ax.set(title="adiantamento e atraso", ylabel="nº de viagens")
ax.legend()

#VISUALIZAÇÃO ATRASO POR EMPRESA
X = np.arange(4)
fig = plt.figure(figsize = (10, 8))
labels = ['Auto Viação Veleiro LTDA','Empresa São Francisco','Real Transportes Urbanos Ltda.','Viação Cidade de Maceió']
indx = np.arange(len(labels))
ax = fig.add_axes([0,0,1,1])
ax.bar(X + 0.0, e_ad['adiantamento'], color = 'pink', width = 0.2, label = 'adiantamento')
ax.bar(X + 0.2, e_at['atraso'], color = 'r', width = 0.2, label = 'atraso')
ax.set_xticks(indx)
ax.set_xticklabels(labels)
ax.legend()
ax.set(title="Empresas", ylabel="nº de viagens")

#VISUALIZAÇÃO GERAL IDA E VOLTA
X = np.arange(2)
fig = plt.figure(figsize = (6, 6))
labels = ['ida', 'volta']
indx = np.arange(len(labels))

ax = fig.add_axes([0,0,1,1])
ax.bar(X + 0.0, sen_ad['adiantamento'], color = 'y', width = 0.2, label = 'adiantamento')
ax.bar(X + 0.2, sen_at['atraso'], color = 'g', width = 0.2, label = 'atraso')
ax.set_xticks(indx)
ax.set_xticklabels(labels)
ax.legend()

ax.set(title="Sentido da viagem", ylabel="nº de viagens")

# Agrupando variáveis por empresa
empresa0 = data.loc[data['empresa'] == 0]
empresa1 = data.loc[data['empresa'] == 1]
empresa2 = data.loc[data['empresa'] == 2]
empresa3 = data.loc[data['empresa'] == 3]

# Empresa 0 
e0_at = empresa0[['sentido', 'atraso']].groupby(['sentido'], as_index=False).sum().sort_values(by='sentido')
e0_ad = empresa0[['sentido', 'adiantamento']].groupby(['sentido'], as_index=False).sum().sort_values(by='sentido')

# Empresa 1
e1_at = empresa1[['sentido', 'atraso']].groupby(['sentido'], as_index=False).sum().sort_values(by='sentido')
e1_ad = empresa1[['sentido', 'adiantamento']].groupby(['sentido'], as_index=False).sum().sort_values(by='sentido')

# Empresa 2
e2_at = empresa2[['sentido', 'atraso']].groupby(['sentido'], as_index=False).sum().sort_values(by='sentido')
e2_ad = empresa2[['sentido', 'adiantamento']].groupby(['sentido'], as_index=False).sum().sort_values(by='sentido')

# Empresa 3
e3_at = empresa3[['sentido', 'atraso']].groupby(['sentido'], as_index=False).sum().sort_values(by='sentido')
e3_ad = empresa3[['sentido', 'adiantamento']].groupby(['sentido'], as_index=False).sum().sort_values(by='sentido')

#VISUALIZAÇÃO DO ATRASO EM CADA EMPRESA POR SENTIDO
X = np.arange(2)
labels = ['ida', 'volta']
indx = np.arange(len(labels))

fig, (ax, ax1) = plt.subplots(1, 2, figsize=(12,6))

ax.bar(X + 0.0, e0_ad['adiantamento'], color='y', width = 0.2, label = 'adiantamento')
ax.bar(X + 0.2, e0_at['atraso'], color = 'g', width = 0.2, label = 'atraso')
ax.set_xticks(indx)
ax.set_xticklabels(labels)
ax.legend(loc = 'upper center')

ax1.bar(X + 0.0, e1_ad['adiantamento'], color = 'y', width = 0.2, label = 'adiantamento')
ax1.bar(X + 0.2, e1_at['atraso'], color = 'g', width = 0.2, label = 'atraso')
ax1.set_xticks(indx)
ax1.set_xticklabels(labels)
ax1.legend(loc = 'upper center')

fig, (ax2, ax3) = plt.subplots(1, 2, figsize=(12,6))

ax2.bar(X + 0.0, e2_ad['adiantamento'], color = 'y', width = 0.2, label = 'adiantamento')
ax2.bar(X + 0.2, e2_at['atraso'], color = 'g', width = 0.2, label = 'atraso')
ax2.set_xticks(indx)
ax2.set_xticklabels(labels)
ax2.legend(loc = 'upper center')

ax3.bar(X + 0.0, e3_ad['adiantamento'], color = 'y', width = 0.2, label = 'adiantamento')
ax3.bar(X + 0.2, e3_at['atraso'], color = 'g', width = 0.2, label = 'atraso')
ax3.set_xticks(indx)
ax3.set_xticklabels(labels)
ax3.legend(loc = 'upper center')

ax.set(title="Auto Viação Veleiro LTDA", xlabel="sentido", ylabel="nº de viagens")
ax1.set(title="Empresa São Francisco", xlabel="sentido", ylabel="nº de viagens")
ax2.set(title="Real Transportes Urbanos Ltda.", xlabel="sentido", ylabel="nº de viagens")
ax3.set(title="Viação Cidade de Maceió", xlabel="sentido", ylabel="nº de viagens")

#VISUALIZAÇÃO ATRASO POR LINHA
fig, ax = plt.subplots(figsize=(24, 6))

X = np.arange(len(nl_ad_40))
labels = nl_at_40['numero_linha']
indx = np.arange(len(labels))
ax.bar(X + 0.0, nl_ad_40['adiantamento'], color = '#87CEFA', width = 0.2, label = 'adiantamento')
ax.bar(X + 0.2, nl_at_40['atraso'], color = '#1C86EE', width = 0.2, label = 'atraso')
ax.set_xticks(indx)
ax.set_xticklabels(labels)
ax.legend()

fig, ax1 = plt.subplots(figsize=(24, 6))

X1 = np.arange(len(nl_ad_80))
labels1 = nl_at_80['numero_linha']
indx = np.arange(len(labels1))
ax1.bar(X1 + 0.0, nl_ad_80['adiantamento'], color = '#87CEFA', width = 0.2, label = 'adiantamento')
ax1.bar(X1 + 0.2, nl_at_80['atraso'], color = '#1C86EE', width = 0.2, label = 'atraso')
ax1.set_xticks(indx)
ax1.set_xticklabels(labels1)
ax1.legend()

ax.set(title="Número de linha entre [17-503]", ylabel="nº de viagens")
ax1.set(title="Número de linha entre [599-7151]", ylabel="nº de viagens")

# Quantidade de linhas que tem mais atraso do que adiantamento e linhas que tem mais adiantamento do que atraso
linhas_at = pd.DataFrame(np.where(nl_at['atraso']>nl_ad['adiantamento'], 1, 0), columns=['atraso'])
linhas_ad = pd.DataFrame(np.where(nl_at['atraso']<nl_ad['adiantamento'], 1, 0), columns=['adiantamento'])

n_linhas_at = linhas_at['atraso'].sum()
n_linhas_ad = linhas_ad['adiantamento'].sum()
print(n_linhas_at, n_linhas_ad)

#VISUALIZAÇÃO GERAL QUANTIDADE DE LINHAS QUE MAIS ATRASARAM OU MAIS ADIANTARAM
X = np.arange(1)
fig = plt.figure(figsize = (4, 6))
indx = np.arange(2)
ax = fig.add_axes([0,0,1,1])
ax.bar(X + 0.4, n_linhas_ad, color = '#87CEFA', width = 0.2, label = 'adiantamento')
ax.bar(X + 0.6, n_linhas_at, color = '#1C86EE', width = 0.2, label = 'atraso')
ax.set_xticks(indx)
ax.set(title="quantidade de linhas que mais atrasaram e as que mais adiantaram", ylabel="nº de linhas")
ax.legend()

# Plot das distribuições do número da linha que atrasou ou não atrasou
a = sns.FacetGrid(data, hue = 'atraso', height=3.5, aspect=5.5)
a.map(sns.kdeplot, 'numero_linha', shade= True )
a.set(xlim=(0 , data['numero_linha'].max()))
a.set_axis_labels("Número da linha")
a.add_legend()
