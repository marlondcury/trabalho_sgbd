import pandas as pd

def verificar_valor_2024():
    print("---  INICIANDO AUDITORIA DE DADOS (CROSS-CHECK) ---")
    
    # 1. Carregar as tabelas exportadas
    try:
        df_tempo = pd.read_csv("arquivos_tableau/dim_tempo.csv")
        df_fato = pd.read_csv("arquivos_tableau/fato_pagamentos.csv")
    except FileNotFoundError:
        print(" Erro: Arquivos CSV não encontrados. Rode o main.py primeiro.")
        return

    # 2. Filtrar os IDs de Tempo referentes ao ano de 2024
    ids_2024 = df_tempo[df_tempo['ano'] == 2024]['id_tempo']
    
    # 3. Filtrar a Fato usando esses IDs
    vendas_2024 = df_fato[df_fato['id_tempo'].isin(ids_2024)]
    
    # 4. Calcular a Soma
    total = vendas_2024['valor_pago'].sum()
    
    print(f"SOMA TOTAL 2024 (PYTHON): R$ {total:,.2f}")
    print("---------------------------------------------------")

if __name__ == "__main__":
    verificar_valor_2024()