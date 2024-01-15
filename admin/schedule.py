import schedule
import time
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv('C:/Users/dantf/Documents/projeto-viajapass/config.env')

def gerar_relatorio():

    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    
    # Conexão com o banco de dados usando SQLAlchemy
    engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@localhost/vjps')

    data_fim = datetime.now().date()
    data_inicio = data_fim - timedelta(days=1)

    query = f"""
    SELECT * FROM vendas 
    WHERE data_compra >= '{data_inicio}' AND data_compra < '{data_fim}'
    """

    # Usando pandas com SQLAlchemy
    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn)

    # Definindo o caminho completo do arquivo
    nome_arquivo = f"C:/Users/dantf/Downloads/relatorio_vendas_{data_inicio}.xlsx"
    df.to_excel(nome_arquivo, index=False)

# Agendar a tarefa para ser executada diariamente às 00:01
schedule.every().day.at("00:39").do(gerar_relatorio)

while True:
    schedule.run_pending()
    time.sleep(1)
