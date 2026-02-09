# Importa as funções dos outros módulos
from extract import get_dados_prefeitura, get_dados_ibge
from transform import executar_transformacao
from load import executar_carga

def main():
    """
    Pipeline principal de ETL (Extração, Transformação e Carga).
    """
    print("INICIANDO PIPELINE DE DADOS - ALEGRE/ES (MySQL)\n")
    
    # 1. EXTRAÇÃO
    anos = range(2015, 2026)
    
    df_pref = get_dados_prefeitura(anos)
    df_ibge = get_dados_ibge()
    
    if df_pref.empty:
        print("Erro: Falha ao baixar dados da prefeitura. Pipeline abortado.")
        return

    # 2. TRANSFORMAÇÃO
    df_final = executar_transformacao(df_pref, df_ibge)
    
    # 3. CARGA (Agora vai para o MySQL)
    executar_carga(df_final)
    
    print("\nPROCESSO FINALIZADO COM SUCESSO!")

if __name__ == "__main__":
    main()