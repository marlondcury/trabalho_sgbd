import pandas as pd
import requests
import xml.etree.ElementTree as ET
import json
from typing import List

def get_dados_prefeitura(anos: List[int]) -> pd.DataFrame:
    """
    Itera sobre a API da Transparência para baixar pagamentos.
    Retorna: DataFrame com dados brutos ou vazio em caso de erro.
    """
    base_url = "https://alegre-es.portaltp.com.br/api/transparencia.asmx/json_pagamentos"
    dados_acumulados = []
    
    print(f"--- [E] Iniciando Extração Prefeitura ({min(anos)} a {max(anos)}) ---")
    
    for ano in anos:
        for mes in range(1, 13):
            print(f"\r-> Baixando: {mes:02d}/{ano}...", end="")
            try:
                params = {"ano": ano, "mes": mes}
                response = requests.get(base_url, params=params, timeout=10)
                
                if response.status_code == 200:
                    xml_root = ET.fromstring(response.content)
                    conteudo_json = xml_root.text
                    
                    if conteudo_json:
                        dados = json.loads(conteudo_json)
                        if len(dados) > 0:
                            dados_acumulados.append(pd.DataFrame(dados))
            except Exception as e:
                print(f" [Erro: {e}]")
                
    print("\nExtração da Prefeitura concluída!")
    
    if dados_acumulados:
        return pd.concat(dados_acumulados, ignore_index=True)
    return pd.DataFrame()

def get_dados_ibge() -> pd.DataFrame:

    print("--- [E] Iniciando Extração IBGE (URL Corrigida) ---")
    
    url = "https://apisidra.ibge.gov.br/values/t/6579/n6/3200201/v/9324/p/last%2015"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            
         
            df = df.loc[:, ['D3N', 'V']].rename(columns={'D3N': 'ano', 'V': 'populacao'})
            
            # Limpeza (Remove cabeçalho e anos inválidos)
            df = df[df['ano'].str.isnumeric()]
            df['ano'] = df['ano'].astype(int)
            df['populacao'] = pd.to_numeric(df['populacao'], errors='coerce')
            
            print(f"   -> Dados do IBGE recuperados: {len(df)} registros.")
            return df
            
    except Exception as e:
        print(f"Erro IBGE: {e}")
        
    return pd.DataFrame()