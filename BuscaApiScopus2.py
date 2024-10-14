import requests
import csv
import os

# Função para realizar uma busca na API da Scopus com base em uma query específica.
def buscar_na_scopus(query, api_key, start=0):
    url = "https://api.elsevier.com/content/search/scopus"
    headers = {
        'X-ELS-APIKey': 'minhachave',
        'Accept': 'application/json'
    }
    params = {
        'query': query,
        'start': start,
        'count': 25,  # Limite de resultados por página (padrão 25)
        'date': '2014-2024',  # Filtro de data (publicações entre 2014 e 2024)
    }
    response = requests.get(url, headers=headers, params=params)
    # Verificando se a resposta foi bem-sucedida
    if response.status_code != 200:
        print(f"Erro: {response.status_code} - {response.text}")
        return {}  # Retorna um dicionário vazio em caso de erro
    return response.json()

# Função que processa os resultados e salva os detalhes em um arquivo CSV.
def salvar_resultados(resultados, query, caminho_csv):
    with open(caminho_csv, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Verificando se o CSV já tem o cabeçalho
        if os.stat(caminho_csv).st_size == 0:
            writer.writerow(['Authors', 'Author full names', 'Author(s) ID', 'Title', 'Year', 'Source title', 'Volume', 
                             'Issue', 'Art. No.', 'Page start', 'Page end', 'Page count', 'Cited by', 'DOI', 'Link', 
                             'Affiliations', 'Authors with affiliations', 'Abstract', 'Author Keywords', 'Index Keywords', 
                             'Funding Details', 'Funding Texts', 'Correspondence Address', 'Editors', 'Publisher', 
                             'ISSN', 'ISBN', 'CODEN', 'PubMed ID', 'Language of Original Document', 
                             'Abbreviated Source Title', 'Document Type', 'Publication Stage', 'Open Access', 
                             'Source', 'EID'])

        # Iterando sobre os resultados e extraindo os valores para cada coluna
        for item in resultados.get('search-results', {}).get('entry', []):
            authors = item.get('dc:creator', 'N/A')
            author_full_names = item.get('author', 'N/A')
            author_ids = item.get('author-id', 'N/A')
            title = item.get('dc:title', 'N/A')
            year = item.get('prism:coverDate', 'N/A')[:4]  # Apenas o ano
            source_title = item.get('prism:publicationName', 'N/A')
            volume = item.get('prism:volume', 'N/A')
            issue = item.get('prism:issueIdentifier', 'N/A')
            art_no = item.get('artno', 'N/A')
            page_start = item.get('prism:startingPage', 'N/A')
            page_end = item.get('prism:endingPage', 'N/A')
            page_count = item.get('page-count', 'N/A')
            cited_by = item.get('citedby-count', 'N/A')
            doi = item.get('prism:doi', 'N/A')
            link = item.get('link', [{}])[0].get('@href', 'N/A')
            affiliations = item.get('affiliation', 'N/A')
            authors_with_affiliations = item.get('authors-with-affiliations', 'N/A')
            abstract = item.get('dc:description', 'N/A')
            author_keywords = item.get('authkeywords', 'N/A')
            index_keywords = item.get('idxterms', 'N/A')
            funding_details = item.get('funding-details', 'N/A')
            funding_texts = item.get('funding-text', 'N/A')
            correspondence_address = item.get('correspondence-address', 'N/A')
            editors = item.get('editors', 'N/A')
            publisher = item.get('prism:publisher', 'N/A')
            issn = item.get('prism:issn', 'N/A')
            isbn = item.get('prism:isbn', 'N/A')
            codon = item.get('codon', 'N/A')
            pubmed_id = item.get('pubmed-id', 'N/A')
            language = item.get('language', 'N/A')
            abbreviated_source_title = item.get('abbrev_source_title', 'N/A')
            document_type = item.get('prism:aggregationType', 'N/A')
            publication_stage = item.get('prism:pubstage', 'N/A')
            open_access = item.get('openaccess', 'N/A')
            source = item.get('source', 'N/A')
            eid = item.get('eid', 'N/A')

            # Escrevendo a linha com os valores
            writer.writerow([authors, author_full_names, author_ids, title, year, source_title, volume, issue, art_no, 
                             page_start, page_end, page_count, cited_by, doi, link, affiliations, authors_with_affiliations, 
                             abstract, author_keywords, index_keywords, funding_details, funding_texts, correspondence_address, 
                             editors, publisher, issn, isbn, codon, pubmed_id, language, abbreviated_source_title, document_type, 
                             publication_stage, open_access, source, eid])

# Função que realiza a busca com várias queries e salva todos os resultados em CSVs separados.
def buscar_e_salvar_todas_queries(queries, api_key):
    for index, query in enumerate(queries, start=1):  # Usando um contador `index` começando de 1
        start = 0
        total_titulos_query = []
        
        # Nome do CSV para cada query com base no número indicador `index`.
        caminho_csv = f'resultados_busca_scopus_{index}.csv'
        
        while True:
            resultados = buscar_na_scopus(query, api_key, start=start)
            total_results = int(resultados.get('search-results', {}).get('opensearch:totalResults', 0))
            
            # Printando o número da query, a string da query e o total de resultados encontrados
            print(f"Query {index}: '{query}' - Total de resultados: {total_results}")
            
            if total_results == 0:
                break  # Se não houver resultados, sai do loop
            
            salvar_resultados(resultados, query, caminho_csv)
            start += 25  # Incremento para pegar a próxima página de resultados.
            
            # Se o número de resultados coletados já for maior ou igual ao total, sair do loop.
            if start >= total_results:
                break
        #print(f"Resposta completa: {resultados}")
        #import json
        #print(json.dumps(resultados, indent=4))

api_key = "minhachave"
queries = [
    '("automatização") AND ("controle de poeira") AND ("extração de minerais")',
    '("automatização") AND ("controle de poeira") AND ("mineração")',
    '("automatização") AND ("controle de poeira") AND ("processamento de minerais")',
    '("automatização") AND ("controle de poeira") AND ("processamento de minério")',
    '("automatização") AND ("extração de poeira") AND ("extração de minerais")',
    '("automatização") AND ("extração de poeira") AND ("mineração")',
    '("automatização") AND ("extração de poeira") AND ("processamento de minerais")',
    '("automatização") AND ("extração de poeira") AND ("processamento de minério")',
    '("automatização") AND ("gestão de poeira") AND ("extração de minerais")',
    '("automatização") AND ("gestão de poeira") AND ("mineração")',
    '("automatização") AND ("gestão de poeira") AND ("processamento de minerais")',
    '("automatização") AND ("gestão de poeira") AND ("processamento de minério")',
    '("automatização") AND ("remoção de poeira") AND ("extração de minerais")',
    '("automatização") AND ("remoção de poeira") AND ("mineração")',
    '("automatização") AND ("remoção de poeira") AND ("processamento de minerais")',
    '("automatização") AND ("remoção de poeira") AND ("processamento de minério")',
    '("automatização") AND ("supressão de poeira") AND ("extração de minerais")',
    '("automatização") AND ("supressão de poeira") AND ("mineração")',
    '("automatização") AND ("supressão de poeira") AND ("processamento de minerais")',
    '("automatização") AND ("supressão de poeira") AND ("processamento de minério")',
    '("automação") AND ("controle de poeira") AND ("extração de minerais")',
    '("automação") AND ("controle de poeira") AND ("mineração")',
    '("automação") AND ("controle de poeira") AND ("processamento de minerais")',
    '("automação") AND ("controle de poeira") AND ("processamento de minério")',
    '("automação") AND ("extração de poeira") AND ("extração de minerais")',
    '("automação") AND ("extração de poeira") AND ("mineração")',
    '("automação") AND ("extração de poeira") AND ("processamento de minerais")',
    '("automação") AND ("extração de poeira") AND ("processamento de minério")',
    '("automação") AND ("gestão de poeira") AND ("extração de minerais")',
    '("automação") AND ("gestão de poeira") AND ("mineração")',
    '("automação") AND ("gestão de poeira") AND ("processamento de minerais")',
    '("automação") AND ("gestão de poeira") AND ("processamento de minério")',
    '("automação") AND ("remoção de poeira") AND ("extração de minerais")',
    '("automação") AND ("remoção de poeira") AND ("mineração")',
    '("automação") AND ("remoção de poeira") AND ("processamento de minerais")',
    '("automação") AND ("remoção de poeira") AND ("processamento de minério")',
    '("automação") AND ("supressão de poeira") AND ("extração de minerais")',
    '("automação") AND ("supressão de poeira") AND ("mineração")',
    '("automação") AND ("supressão de poeira") AND ("processamento de minerais")',
    '("automação") AND ("supressão de poeira") AND ("processamento de minério")',
    '("sistemas automatizados") AND ("controle de poeira") AND ("extração de minerais")',
    '("sistemas automatizados") AND ("controle de poeira") AND ("mineração")',
    '("sistemas automatizados") AND ("controle de poeira") AND ("processamento de minerais")',
    '("sistemas automatizados") AND ("controle de poeira") AND ("processamento de minério")',
    '("sistemas automatizados") AND ("extração de poeira") AND ("extração de minerais")',
    '("sistemas automatizados") AND ("extração de poeira") AND ("mineração")',
    '("sistemas automatizados") AND ("extração de poeira") AND ("processamento de minerais")',
    '("sistemas automatizados") AND ("extração de poeira") AND ("processamento de minério")',
    '("sistemas automatizados") AND ("gestão de poeira") AND ("extração de minerais")',
    '("sistemas automatizados") AND ("gestão de poeira") AND ("mineração")',
    '("sistemas automatizados") AND ("gestão de poeira") AND ("processamento de minerais")',
    '("sistemas automatizados") AND ("gestão de poeira") AND ("processamento de minério")',
    '("sistemas automatizados") AND ("remoção de poeira") AND ("extração de minerais")',
    '("sistemas automatizados") AND ("remoção de poeira") AND ("mineração")',
    '("sistemas automatizados") AND ("remoção de poeira") AND ("processamento de minerais")',
    '("sistemas automatizados") AND ("remoção de poeira") AND ("processamento de minério")',
    '("sistemas automatizados") AND ("supressão de poeira") AND ("extração de minerais")'
]

buscar_e_salvar_todas_queries(queries, api_key)



