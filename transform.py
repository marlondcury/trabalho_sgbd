import pandas as pd
import numpy as np

def _inferir_funcao_governo(row: pd.Series) -> str:
    """
    Função interna (helper) para aplicar a lógica de negócio linha a linha.
    """
    # 1. Se já existe função válida, mantém
    func_atual = str(row.get('funcao_governo', ''))
    if func_atual != '' and func_atual.upper() != 'NAN':
        return func_atual

    # 2. Prepara variáveis para análise
    secretaria = str(row.get('secretaria', '')).upper()
    tipo = str(row.get('tipo_pagamento', '')).upper()
    
    # 3. Árvore de Decisão
    if 'SAUDE' in secretaria:
        return '10 - SAÚDE (INFERIDO)'
    elif any(x in secretaria for x in ['EDUCACAO', 'FAFIA', 'FUNDEB']):
        return '12 - EDUCAÇÃO (INFERIDO)'
    elif 'ASSISTENCIA SOCIAL' in secretaria:
        return '08 - ASSISTÊNCIA SOCIAL (INFERIDO)'
    elif 'SAAE' in secretaria:
        return '17 - SANEAMENTO (INFERIDO)'
    elif 'PREFEITURA' in secretaria:
        return 'EXTRA ORÇAMENTÁRIO' if 'EXTRA' in tipo else '04 - ADMINISTRAÇÃO (INFERIDO)'
            
    return 'SEM CLASSIFICAÇÃO'

def executar_transformacao(df_bruto: pd.DataFrame, df_ibge: pd.DataFrame) -> pd.DataFrame:
    """
    Orquestra a limpeza e o merge dos dados.
    """
    print("--- [T] Iniciando Transformação ---")
    
    # Cria cópia para evitar SettingWithCopyWarning
    df = df_bruto.copy()
    
    # Padronização básica
    df['secretaria'] = df['unidade_gestora'].astype(str).str.upper().str.strip()
    
    # USO DO .LOC PARA ATRIBUIÇÃO SEGURA
    df.loc[:, 'funcao_governo'] = df['funcao'].fillna('')
    
    print("Aplicando regras de inferência (Isso pode levar alguns segundos)...")
    df['funcao_governo'] = df.apply(_inferir_funcao_governo, axis=1)
    
    # Tipagem
    df['data_pagamento'] = pd.to_datetime(df['data']).dt.date
    df['valor_pago'] = pd.to_numeric(df['valor'], errors='coerce').fillna(0.0)
    df['ano'] = pd.to_datetime(df['data']).dt.year
    df['mes'] = pd.to_datetime(df['data']).dt.month

    # Merge com IBGE
    if not df_ibge.empty:
        print("Cruzando com dados do IBGE...")
        df = pd.merge(df, df_ibge, on='ano', how='left')
        df['populacao'] = df['populacao'].ffill().bfill()
    
    # Seleção final de colunas
    cols_finais = ['ano', 'mes', 'data_pagamento', 'secretaria', 
                   'funcao_governo', 'nome_favorecido', 'valor_pago', 'populacao']
    
    cols_existentes = [c for c in cols_finais if c in df.columns]
    
    # Retorna apenas as colunas desejadas usando .loc
    return df.loc[:, cols_existentes]