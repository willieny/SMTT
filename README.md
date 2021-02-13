# SMTT

## Introdução

Esta é uma atividade que visa a construção de alguma ferramenta tecnológica por via de programação, a resolver uma das problemáticas acerca do Sistema de Transporte
Coletivo de Maceió. Um dos relatórios que serve como base para tomada de decisão é o relatório de tempo de viagem, no qual é possível ter acesso a indicadores importantes para a avaliação da qualidade do sistema, como atraso, adiantamento e cumprimento de viagem.

Se caracteriza como **atraso** a viagem com horário realizado após o horário previsto. **Adiantamento de viagem** é quando o horário realizado é antes do horário previsto. **Cumprimento de viagem** é quando a viagem foi realizada (as não realizadas não possuem valor em “hora realizada”).

## Objetivo 

O objetivo é desenvolver a apresentação de um resumo a partir de pelo menos um dos índices apresentados.

## Compreensão dos dados

### Importando das bibliotecas
Antes de qualquer preparação, é necessário importar as bibliotecas Python contendo a funcionalidade necessária que será utilizada.

```
import pandas as pd
import numpy as np
import math

from sklearn import preprocessing

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import seaborn as sns
```

### Lendo o conjunto de dados

```
df = pd.read_csv('viagens.csv')
```

Além disso, vamos ver o tipo de dados e seus tipos relacionados:

```
df.info()
```
```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 21702 entries, 0 to 21701
Data columns (total 14 columns):
 #   Column                         Non-Null Count  Dtype  
---  ------                         --------------  -----  
 0   Unnamed: 0                     21702 non-null  int64  
 1   numero_viagem_da_linha_no_dia  21702 non-null  int64  
 2   ordem_veiculo_na_linha_no_dia  21702 non-null  int64  
 3   duracao_total_realizada        19072 non-null  float64
 4   nome_linha                     21702 non-null  object 
 5   atendimento                    21702 non-null  object 
 6   empresa                        21702 non-null  object 
 7   numero_ordem_veiculo           21702 non-null  int64  
 8   numero_linha                   21702 non-null  int64  
 9   hora_prevista                  21702 non-null  object 
 10  hora_realizada                 19528 non-null  object 
 11  duracao_prevista               21702 non-null  int64  
 12  duracao_realizada              18169 non-null  float64
 13  sentido_viagem                 21702 non-null  object 
dtypes: float64(2), int64(6), object(6)
memory usage: 2.3+ MB
```

### Tratando o conjunto de dados

Primeiro vamos identificar os dados faltantes:

```
df.isnull().sum()
```
```
numero_viagem_da_linha_no_dia       0
ordem_veiculo_na_linha_no_dia       0
duracao_total_realizada          2630
nome_linha                          0
atendimento                         0
empresa                             0
numero_ordem_veiculo                0
numero_linha                        0
hora_prevista                       0
hora_realizada                   2174
duracao_prevista                    0
duracao_realizada                3533
sentido_viagem                      0
dtype: int64
```
#### Completando e removendo dados faltantes

Como a análise será feita apenas a partir das colunas 'empresa', 'numero_linha', 'hora_prevista',	'hora_realizada' e 'sentido_viagem', então os dados faltantes nas colunas 'duracao_total_realizada' e 'duracao_realizada' serão preenchidos pela média de cada coluna. Além disso, os indicadores escolhidos para avaliação da qualidade do sistema são atraso e adiantamento da viagem. Dessa forma, os valores falantes em 'hora_realizada', que caracteriza o não cumprimento da viagem, serão removidos. Após alterações:

```
df.isnull().sum()
```
```
numero_viagem_da_linha_no_dia    0
ordem_veiculo_na_linha_no_dia    0
duracao_total_realizada          0
nome_linha                       0
atendimento                      0
empresa                          0
numero_ordem_veiculo             0
numero_linha                     0
hora_prevista                    0
hora_realizada                   0
duracao_prevista                 0
duracao_realizada                0
sentido_viagem                   0
dtype: int64
```

#### Transformando as variáveis categóricas em variáveis numéricas

As colunas 'atraso' e 'adiantamento' foram obtidas após a comparação entre as colunas 'hora_prevista' e 'hora_realizada'. Em 'empresa', o nome da empresa foi subtituído por um valor inteiro, o mesmo foi feito para 'sentido_viagem'. Conjunto de dados após alterações:

![image](https://user-images.githubusercontent.com/32077255/107834049-f1c7c580-6d73-11eb-9a64-077ae626f4cf.png)

#### Contagem do atraso e do adiantamento em relação as variáveis para visualização dos dados

A partir das features/variáveis do dataframe anterior foi criado um dataframe para cada variável, que relaciona uma variável a quantidade de atraso ou adiantamento. Por exemplo, para fazer de 'empresa' relacionada ao 'atraso' foi obtido o seguinte resultado:

![image](https://user-images.githubusercontent.com/32077255/107834867-4c622100-6d76-11eb-883e-319557a2417a.png)

### Explorando os dados a partir de gráficos para descrever e resumir as features.

Inicialmente serão visualizados a quantidade total de atraso e adiantamento por número de viagens.

![image](https://user-images.githubusercontent.com/32077255/107835148-46207480-6d77-11eb-93b9-0364be967486.png)

Em seguida, o atraso e adiantamento serão visualizados por empresa. Assim, podemos analisar qual empresa tem melhor e pior desempenho.

![image](https://user-images.githubusercontent.com/32077255/107835252-9992c280-6d77-11eb-859c-530950b4bc6b.png)

Outra feature, que nos ajudará a ter uma visualização melhor sobre o atraso e adiantamento de viagem, é o sentido da viagem. Assim, saberemos se é na ida ou na volta que acontece mais atrasos ou mais adiantamentos. O resultado a seguir corresponde a quantidade total de atraso e adiantamento por sentido.

![image](https://user-images.githubusercontent.com/32077255/107835582-c5627800-6d78-11eb-909f-3021f86e1ea3.png)

Para obter um melhor resultado a respeito das empresas e do sentido foi criado alguns gráficos que mostram a quantidade de atrasos e de adiantamentos de cada empresa por sentido da viagem. Uma vez que uma empresa pode ter tido uma quantidade alta de atrasos totais, mas pode ter tido um bom desempenho em algum sentido de viagem.

![image](https://user-images.githubusercontent.com/32077255/107837479-c1862400-6d7f-11eb-93cf-7e3a32600f3f.png)

Além das features anteriores, o número da linha também foi utilizada para fazer análise dos indicadores apresentados e foi obtido o seguinte resultado:

![image](https://user-images.githubusercontent.com/32077255/107836143-d57b5700-6d7a-11eb-8497-69ab021e1716.png)

Para uma visualização mais geral a respeito do número da linha, então foi criado o seguinte gráfico, no qual representa a quantidade total de linhas que tiveram mais atrasos e mais adiantamentos.

![image](https://user-images.githubusercontent.com/32077255/107836478-0445fd00-6d7c-11eb-83f5-439dce9cc422.png)

Por fim, o seguinte gráfico foi plotado para representar as distribuições do número da linha que atrasou ou não atrasou.

![image](https://user-images.githubusercontent.com/32077255/107836534-4b33f280-6d7c-11eb-9916-7a5d8830cb16.png)

## Conclusão

Tendo em vista apenas os gráficos mais gerais ('adiatamento e atraso', 'sentido da viagem' e 'quantidade de linhas que mais atrasaram e as que mais adiantaram'), a quantidade de atrasos se sobressai mostrando um desempenho ruim do sistema. Contudo, é possível fazer algumas ressalvas com base nos demais gráficos apresentados.
A respeito do gráfico 'Empresas', a empresa "Empresa São Francisco" teve o pior desempenho com quase o dobro de atraso em contraste com as outras empresas. E a empresa "Real Transportes Urbanos Ltda." teve o melhor desempenho com quase a mesma quantidade de atrasos e adiantamentos. 
A partir dos gráficos de atraso e adiantamento por sentido da viagem de cada empresa, é possível observar que a empresa "Auto Viação Veleiro LTDA" teve um bom resultado na ida, já as empresas "Real Transportes Urbanos Ltda." e "Viação Cidade de Maceió" tiveram bons resultados na volta.
