import mysql.connector
from mysql.connector import Error
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "host": os.getenv("MYSQL_HOST"),
    "database": os.getenv("MYSQL_DATABASE"),
}

DATA_FILES = {
    "clientes": "../TRATADOS/Clientes_tratado.csv",
    "estoque": "../TRATADOS/Estoque_tratado.csv",
    "fornecedores": "../TRATADOS/Fornecedores_tratado.csv",
    "produtos": "../TRATADOS/Produtos_tratado.csv",
    "vendas": "../TRATADOS/Vendas_tratado.csv",
}

def load_data():
    return {
        key: pd.read_csv(path, sep=";", encoding="ISO-8859-1")
        if key in ["fornecedores", "produtos"] else pd.read_csv(path, sep=";")
        for key, path in DATA_FILES.items()
    }

def connect_to_mysql():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def insert_data(cursor, table, data, id_column):
    for _, row in data.iterrows():
        values = tuple(row)
        cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {id_column} = %s", (row[id_column],))
        if cursor.fetchone()[0] == 0:
            try:
                columns = ", ".join(row.index)
                placeholders = ", ".join(["%s"] * len(row))
                sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
                cursor.execute(sql, values)
            except Exception as e:
                print(f"Erro ao inserir {table} ID {row[id_column]}: {e}")
        else:
            print(f"{table.capitalize()} ID {row[id_column]} já existe, inserção ignorada.")

def main():
    connection = connect_to_mysql()
    if connection:
        try:
            cursor = connection.cursor()
            data = load_data()
            
            tables = {
                "clientes": "id",
                "fornecedores": "supplier_id",
                "produtos": "product_id",
                "estoque": "product_id",
                "vendas": "id",
            }
            
            for table, id_column in tables.items():
                insert_data(cursor, table, data[table], id_column)
            
            connection.commit()
            print("Dados inseridos com sucesso!")
        except Error as e:
            print(f"Erro ao inserir dados: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
            print("Conexão encerrada.")

if __name__ == "__main__":
    main()
