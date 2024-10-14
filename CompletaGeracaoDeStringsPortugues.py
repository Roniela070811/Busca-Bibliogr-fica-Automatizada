import nltk
from nltk.corpus import wordnet as wn
import pandas as pd  # Importar a biblioteca Pandas
import os

# Download dos dados necessários.
nltk.download('wordnet')
nltk.download('omw-1.4')

# Função que gera os sinônimos das palavras chaves fornecidas em português.
def gerar_sinonimos(palavras_chave):
    sinonimos = {}
    
    for palavra in palavras_chave:
        lista_sinonimos = set()  # Usando um conjunto para evitar repetições.
        lista_sinonimos.add(palavra)  # Adicionando a palavra chave inicial.
        
        for synset in wn.synsets(palavra, lang='por'):  # Usando 'por' para português
            for lemma in synset.lemmas('por'):
                lista_sinonimos.add(lemma.name())  # Adicionando os sinônimos.
        
        sinonimos[palavra] = list(lista_sinonimos)  # Transformando as adições em lista para ser retornada.
    
    return sinonimos

# Palavras-chaves iniciais traduzidas para o português
automacao = ["automação", "sistemas automatizados", "tecnica de automação"]
despoeiramento = ["supressão de poeira", "controle de poeira", "gestão de poeira", "remoção de poeira", "extração de poeira"]
mineracao = ["mineração", "processamento de minerais", "processamento de minério", "extração de minerais"]

# Gerar sinônimos para cada categoria
automacao_sinonimos = gerar_sinonimos(automacao)
despoeiramento_sinonimos = gerar_sinonimos(despoeiramento)
mineracao_sinonimos = gerar_sinonimos(mineracao)

# Criar listas completas
lista_automacao = [sin for sublist in automacao_sinonimos.values() for sin in sublist]
lista_despoeiramento = [sin for sublist in despoeiramento_sinonimos.values() for sin in sublist]
lista_mineracao = [sin for sublist in mineracao_sinonimos.values() for sin in sublist]

# Remover duplicatas e organizar a lista
lista_automacao = sorted(set(lista_automacao))
lista_despoeiramento = sorted(set(lista_despoeiramento))
lista_mineracao = sorted(set(lista_mineracao))

# Imprimir os resultados de forma organizada
print("\nLista de sinônimos para Automação:")
print(lista_automacao)

print("\nLista de sinônimos para Supressão de Poeira:")
print(lista_despoeiramento)

print("\nLista de sinônimos para Mineração:")
print(lista_mineracao)

# Função para gerar strings de busca
def gerar_strings_busca(lista_automacao, lista_despoeiramento, lista_mineracao):
    strings_busca = []
    
    for auto in lista_automacao:
        for despo in lista_despoeiramento:
            for miner in lista_mineracao:
                string = f'("{auto}") AND ("{despo}") AND ("{miner}")'
                strings_busca.append(string)
    
    return strings_busca

# Gerando as strings de busca
strings_de_busca = gerar_strings_busca(lista_automacao, lista_despoeiramento, lista_mineracao)

# Criando um dataframe com as strings de busca geradas.
df_strings = pd.DataFrame(strings_de_busca, columns=['Strings de Busca'])

# Imprimindo o DataFrame
print("\nDataFrame com Strings de Busca:")
print(df_strings)

# Verificando o diretório atual
diretorio_atual = os.getcwd()

# Caminho para salvar o csv.
caminho_csv = os.path.join(diretorio_atual, 'strings_de_busca.csv')

# Exportando o csv
df_strings.to_csv(caminho_csv, index=False)
