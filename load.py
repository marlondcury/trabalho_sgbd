import pandas as pd
from sqlalchemy import create_engine, text
import os

def carregar_data_mart_hibrido(df_completo, nome_banco="dw_alegre"):
    """
    Estratégia Híbrida:
    1. Carrega no MySQL (Atende requisito de SGBD).
    2. Exporta CSVs (Atende requisito de Tableau/SAD sem erros de driver).
    """
    print(f"--- [L] Iniciando Carga Híbrida (MySQL + CSV) ---")
    
    # --- PARTE 1: PREPARAR OS DADOS (MODELAGEM) ---
    
    # Dimensão Tempo
    dim_tempo = df_completo[['data_pagamento', 'ano', 'mes']].drop_duplicates().sort_values('data_pagamento').reset_index(drop=True)
    dim_tempo['id_tempo'] = dim_tempo.index + 1
    
    # Dimensão Secretaria
    dim_secretaria = df_completo[['secretaria']].drop_duplicates().sort_values('secretaria').reset_index(drop=True)
    dim_secretaria['id_secretaria'] = dim_secretaria.index + 1

    # Dimensão Função
    dim_funcao = df_completo[['funcao_governo']].drop_duplicates().sort_values('funcao_governo').reset_index(drop=True)
    dim_funcao['id_funcao'] = dim_funcao.index + 1

    # Dimensão Favorecido
    dim_favorecido = df_completo[['nome_favorecido']].drop_duplicates().sort_values('nome_favorecido').reset_index(drop=True)
    dim_favorecido['id_favorecido'] = dim_favorecido.index + 1

    # Tabela Fato
    fato = df_completo.copy()
    fato = fato.merge(dim_tempo, on=['data_pagamento', 'ano', 'mes'], how='left')
    fato = fato.merge(dim_secretaria, on='secretaria', how='left')
    fato = fato.merge(dim_funcao, on='funcao_governo', how='left')
    fato = fato.merge(dim_favorecido, on='nome_favorecido', how='left')
    
    fato_final = fato[['id_tempo', 'id_secretaria', 'id_funcao', 'id_favorecido', 'valor_pago', 'populacao']]

    # --- PARTE 2: CARGA NO MYSQL (REQUISITO SGBD) ---
    try:
        usuario = 'root'
        senha = '758963' 
        host = 'localhost'
        string_conexao = f'mysql+pymysql://{usuario}:{senha}@{host}:3306/{nome_banco}'
        
        engine = create_engine(string_conexao)
        conn = engine.connect()
        
        print("   -> [MySQL] Conectado! Enviando tabelas...")
        dim_tempo.to_sql('dim_tempo', engine, if_exists='replace', index=False)
        dim_secretaria.to_sql('dim_secretaria', engine, if_exists='replace', index=False)
        dim_funcao.to_sql('dim_funcao', engine, if_exists='replace', index=False)
        dim_favorecido.to_sql('dim_favorecido', engine, if_exists='replace', index=False)
        fato_final.to_sql('fato_pagamentos', engine, if_exists='replace', index=False)
        print("✅ [MySQL] Data Mart carregado com sucesso!")
        
    except Exception as e:
        print(f"Aviso: Não foi possível conectar ao MySQL ({e}). Mas vamos gerar os CSVs para o Tableau!")

    # --- PARTE 3: EXPORTAR CSVs (REQUISITO TABLEAU) ---
    print("   -> [Tableau] Gerando arquivos compatíveis...")
    os.makedirs("arquivos_tableau", exist_ok=True)
    
    dim_tempo.to_csv("arquivos_tableau/dim_tempo.csv", index=False)
    dim_secretaria.to_csv("arquivos_tableau/dim_secretaria.csv", index=False)
    dim_funcao.to_csv("arquivos_tableau/dim_funcao.csv", index=False)
    dim_favorecido.to_csv("arquivos_tableau/dim_favorecido.csv", index=False)
    fato_final.to_csv("arquivos_tableau/fato_pagamentos.csv", index=False)
    
    print("✅ [Tableau] Arquivos prontos na pasta 'arquivos_tableau'!")

def executar_carga(df_final):
    carregar_data_mart_hibrido(df_final)