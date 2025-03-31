import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "host": os.getenv("MYSQL_HOST"),
    "database": os.getenv("MYSQL_DATABASE"),
}

def connect_to_mysql():
    try:
        return mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def create_database(cursor):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']};")
    print(f'Banco de dados "{DB_CONFIG["database"]}" criado/verificado com sucesso!')

def create_tables(cursor):
    """Cria as tabelas no banco de dados."""
    tabelas = {
        "clientes": """
            CREATE TABLE IF NOT EXISTS clientes (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                register_number VARCHAR(20) UNIQUE NOT NULL,
                phone VARCHAR(20),
                email VARCHAR(255) UNIQUE,
                address VARCHAR(255),
                city VARCHAR(100),
                state VARCHAR(2),
                country VARCHAR(30),
                local VARCHAR(100),
                complete_address VARCHAR(100),
                zip_code VARCHAR(10)
            );
        """,
        "fornecedores": """
            CREATE TABLE IF NOT EXISTS fornecedores (
                supplier_id INT PRIMARY KEY AUTO_INCREMENT,
                contractor_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                register_number VARCHAR(20) UNIQUE NOT NULL,
                address VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                city VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                uf VARCHAR(2),
                zip_code VARCHAR(10),
                buyed_qty INT DEFAULT 0
            );
        """,
        "produtos": """
            CREATE TABLE IF NOT EXISTS produtos (
                product_id INT PRIMARY KEY AUTO_INCREMENT,
                product_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                category VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                value DECIMAL(10,2) NOT NULL,
                supplier_id INT,
                FOREIGN KEY (supplier_id) REFERENCES fornecedores(supplier_id)
            );
        """,
        "estoque": """
            CREATE TABLE IF NOT EXISTS estoque (
                product_id INT PRIMARY KEY,
                stock_qty INT NOT NULL,
                updated_at DATE NOT NULL,
                supplier_id INT,
                FOREIGN KEY (product_id) REFERENCES produtos(product_id),
                FOREIGN KEY (supplier_id) REFERENCES fornecedores(supplier_id)
            );
        """,
        "vendas": """
            CREATE TABLE IF NOT EXISTS vendas (
                id INT PRIMARY KEY AUTO_INCREMENT,
                client_id INT,
                product_id INT,
                quantity INT NOT NULL,
                sale_date DATE NOT NULL,
                total_value DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (client_id) REFERENCES clientes(id),
                FOREIGN KEY (product_id) REFERENCES produtos(product_id)
            );
        """
    }
    
    for nome, sql in tabelas.items():
        cursor.execute(sql)
        print(f"Tabela '{nome}' criada/verificada com sucesso!")

def main():
    connection = connect_to_mysql()
    if connection:
        try:
            cursor = connection.cursor()
            create_database(cursor)
            connection.database = DB_CONFIG["database"]
            create_tables(cursor)
        except Error as e:
            print(f"Erro ao criar banco de dados ou tabelas: {e}")
        finally:
            cursor.close()
            connection.close()
            print("Conexão encerrada.")

if __name__ == "__main__":
    main()
