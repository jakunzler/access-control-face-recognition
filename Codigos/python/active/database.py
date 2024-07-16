import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="face_recognition",
            user="root",
            password="Yuumi@6733"
        )
        return connection  # Retorna a conexão estabelecida
    except Error as e:
        print("Erro ocorrido ao conectar ao banco de dados:", e)
        return None

def insert_save_face_to_database(nome, encoding, email):
    connection = conectar()
    if connection is None:
        print("Não foi possível estabelecer conexão.")
        return
    
    try:
        cursor = connection.cursor()
        sql = "INSERT INTO faces (nome, encoding, email) VALUES (%s, %s, %s)"
        val = (nome, str(encoding), email)
        cursor.execute(sql, val)
        connection.commit()  # Commit da transação
        print("Salvo com sucesso no banco de dados")
    except Error as e:
        print("Erro ao inserir no banco de dados:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexão fechada")
            print(nome, encoding, email)
            
# Função para selecionar dados do banco de dados
def select_face_from_database():
    connection = conectar()
    if connection is None:
        print("Não foi possível estabelecer conexão com o banco de dados.")
        return None
    
    try:
        cursor = connection.cursor()
        sql = "SELECT nome, encoding FROM faces"
        cursor.execute(sql)
        results = cursor.fetchall()
        return results  # Retorna os resultados da consulta
    except Error as e:
        print("Erro ao selecionar do banco de dados:", e)
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexão fechada")
