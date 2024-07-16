import face_recognition as fr
import cv2
import os
import mysql.connector
import numpy as np


# Conectando ao banco de dados
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="new_password",
    database="face_recognition"
)
db_cursor = db_connection.cursor()

# Criação da tabela no banco de dados se ela não existir
db_cursor.execute("CREATE TABLE IF NOT EXISTS faces (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), encoding TEXT)")

def facial_recognition(frame):
    # Converte o frame para RGB (face_recognition usa o espaço de cores RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detecta as faces no frame
    face_locations = fr.face_locations(rgb_frame)
    
    # Se não houver nenhuma face detectada, retorna uma lista vazia
    if len(face_locations) == 0:
        return []

    # Extrai os encodings faciais para todas as faces detectadas no frame
    face_encodings = fr.face_encodings(rgb_frame, face_locations)

    return face_encodings


def save_face_to_database(nome, encoding):
    # Função para salvar o rosto e o encoding no banco de dados
    sql = "INSERT INTO faces (nome, encoding) VALUES (%s, %s)"
    val = (nome, str(encoding))
    db_cursor.execute(sql, val)
    db_connection.commit()

def new_face(nome):
    # Função para cadastrar um novo rosto
    take_picture()
    foto_data = fr.load_image_file("./img/picture.jpeg")
    faces1 = fr.face_encodings(foto_data)
    if len(faces1) > 0:
        save_face_to_database(nome, faces1[0])
        print("Rosto do", nome, "cadastrado com sucesso.")
    else:
        print("Rosto não cadastrado")

def take_picture():
    # Função para capturar uma foto
    cam = cv2.VideoCapture(0)
    
    if not cam.isOpened():
        print("Error: Could not open camera.")
        exit()


    while True:
        picture, frame = cam.read()
        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cam.release()
            cv2.destroyAllWindows()
            break
        
        
    if picture:
        if not os.path.exists("img"):
            os.makedirs("img")
        caminho_arquivo = os.path.join("img", "picture.jpeg")
        cv2.imwrite(caminho_arquivo, frame)
    else:
        print("Não foi possível capturar a imagem.")


def identify_face():
    cam = cv2.VideoCapture(0)
    
    if not cam.isOpened():
        print("Error: Could not open camera.")
        exit()


    while True:
        ret, frame = cam.read()
        if not ret:
            print("Não foi possível capturar o quadro da câmera.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_encodings = facial_recognition(rgb_frame)

        if len(face_encodings) > 0:
            face_encoding = face_encodings[0]

            db_cursor.execute("SELECT nome, encoding FROM faces")
            known_faces = db_cursor.fetchall()

            for nome, encoding_str in known_faces:
                known_face_encoding = np.fromstring(encoding_str[1:-1], dtype=float, sep=' ')
                match = fr.compare_faces([known_face_encoding], face_encoding)
                if match[0]:
                    print(f"Rosto identificado como {nome}.")
                    # Desenha um retângulo ao redor do rosto identificado
                    top, right, bottom, left = fr.face_locations(rgb_frame)[0]
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    # Escreve o nome da pessoa identificada acima do retângulo
                    cv2.putText(frame, nome, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    break

        cv2.imshow("Identificação Facial em Tempo Real", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


def edit_face():
    nome_antigo = input("Digite o nome da pessoa que deseja editar: ")
    novo_nome = input("Digite o novo nome: ")

    db_cursor.execute("SELECT nome, encoding FROM faces WHERE nome = %s", (nome_antigo,))
    result = db_cursor.fetchone()

    if result:
        db_cursor.execute("UPDATE faces SET nome = %s WHERE nome = %s", (novo_nome, nome_antigo))
        db_connection.commit()
        print("Informações editadas com sucesso.")
    else:
        print("Rosto não encontrado. Certifique-se de que o nome está correto.")


def show_names():
    db_cursor.execute("SELECT nome FROM faces")
    results = db_cursor.fetchall()

    if results:
        print("Rostos cadastrados:")
        for result in results:
            print(result[0])
    else:
        print("Nenhum rosto cadastrado.")

# Loop principal do programa
while True:
    print("---------------------------------------------------")
    print("O que deseja fazer?")
    print("1 - Cadastrar um rosto")
    print("2 - Verificar se um rosto está cadastrado")
    print("3 - Editar as informações de uma pessoa")
    print("4 - Listar os rostos cadastrados")
    print("5 - Sair")

    n1 = input("Digite o número da opção desejada: ")

    if n1 == "1":
        new_face(input("Digite o nome da pessoa que deseja cadastrar: "))
    elif n1 == "2":
        identify_face()
    elif n1 == "3":
        edit_face()
    elif n1 == "4":
        show_names()
    elif n1 == "5":
        print("Saindo do programa. Até mais!")
        break
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")
