import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Caminho do arquivo
caminho = r'C:\Users\Luiza\Downloads\titanic\titanic.xlsx'

# Lendo o Excel
df = pd.read_excel(caminho)

# RENOMEANDO E RECODIFICANDO (Padronização FEAUSP) ---

# Primeiro Passo: Troca o nome da coluna de 'sexo' para 'gênero'
df = df.rename(columns={'sexo': 'gênero'})

# Padronizar valores 
df['gênero'] = df['gênero'].astype(str).str.lower().map({
    'masculino': 'Masculino',
    'feminino': 'Feminino',
    '0': 'Masculino',
    '1': 'Feminino'
})

print(" Coluna 'gênero' atualizada com nomes (Masculino/Feminino).")

# Padronizando as faixas etárias (Criança/Adulto/Idoso)
bins = [0, 12, 100]
labels = ['Criança (0-12)', 'Adulto (13+)']
df['faixa_etaria'] = pd.cut(df['idade'], bins=bins, labels=labels)

# 1. Ler o formato das variáveis 
print(df.dtypes)

# 2. TRANSFORMAÇÃO DE FORMATOS E TIPOS

# A. Dummificação da variável 'sobreviveu' (1=sim, 0=nao)
df['sobreviveu'] = df['sobreviveu'].map({'sim': 1, 'nao': 0})

# B. (mantido comentado como você já fez)
# df['gênero'] = df['gênero'].map({'feminino': 1, 'masculino': 0})

# C. Categorização Ordinal da variável 'classe'
ordem_classes = ['primeira', 'segunda', 'terceira']
df['classe'] = pd.Categorical(df['classe'], categories=ordem_classes, ordered=True)

# D. TRATAMENTO DA IDADE
df['idade'] = df['idade'].round().astype('Int64')

# 3. DIAGNÓSTICO DE DADOS OMISSOS
print(df.isnull().sum())

# --- 4. TRATAMENTO DE DADOS OMISSOS ---
if 'nivel_cabine' in df.columns:
    df = df.drop(columns=['nivel_cabine'])

mediana_idade = df['idade'].median()
df['idade'] = df['idade'].fillna(mediana_idade).round().astype(int) 

moda_embarque = df['embarque'].mode()[0]
df['embarque'] = df['embarque'].fillna(moda_embarque)

# HISTOGRAMA + BOXPLOT juntos
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

sns.histplot(df['idade'], kde=True, ax=ax1)
ax1.set_title('Distribuição da Idade')

sns.boxplot(y=df['idade'], ax=ax2)
ax2.set_title('Boxplot da Idade')

plt.show()

# --- 5. VISUALIZAÇÃO DE OUTLIERS ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
sns.boxplot(y=df['valor_tarifa'], ax=ax1, color='skyblue')
sns.boxplot(y=df['idade'], ax=ax2, color='salmon')
plt.show()

# 6 e 7. TRATAMENTO DE OUTLIERS
limite_p95 = df['valor_tarifa'].quantile(0.95)
df['tarifa_tratada'] = df['valor_tarifa'].clip(upper=limite_p95)

# 8. ANÁLISE: SOBREVIVÊNCIA POR GÊNERO
plt.figure(figsize=(8, 6))
sns.countplot(x='gênero', hue='sobreviveu', data=df, palette='viridis')
plt.title('Distribuição de Sobreviventes por Gênero')
plt.legend(title='Sobreviveu', labels=['Não', 'Sim'])
plt.show()

# 9. ANÁLISE: SOBREVIVÊNCIA POR CLASSE
plt.figure(figsize=(10, 6))
sns.countplot(x='classe', hue='sobreviveu', data=df, palette='magma', order=['primeira', 'segunda', 'terceira'])
plt.show()

# 10. ANÁLISE: IDADE VS SOBREVIVÊNCIA 
plt.figure(figsize=(8, 6))
sns.boxplot(x='sobreviveu', y='idade', data=df)
plt.xticks([0, 1], ['Não Sobreviveu', 'Sobreviveu'])
plt.show()

plt.show()