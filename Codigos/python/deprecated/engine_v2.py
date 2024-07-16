import face_recognition as fr
import cv2
import mysql.connector
import numpy as np

# Conexão com o banco de dados
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
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        ret, frame = cam.read()
        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            if ret:
                face_encodings = facial_recognition(frame)
                if len(face_encodings) > 0:
                    save_face_to_database(nome, face_encodings[0])
                    print("Rosto do", nome, "cadastrado com sucesso.")
                else:
                    print("Rosto não cadastrado")
            else:
                print("Não foi possível capturar a imagem.")
            break

    cam.release()
    cv2.destroyAllWindows()

def identify_face():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Could not open camera.")
        return

    face_identificado = False  # Flag para controle de identificação

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
                match = fr.compare_faces([known_face_encoding], face_encoding, tolerance= 0.4)
                if match[0]:
                    print(f"IDENTIFICADO: {nome}")
                    face_identificado = True
                    break
        if cv2.waitKey(1):
            break

        if face_identificado:
            break

    cam.release()
    cv2.destroyAllWindows()

    if not face_identificado:
        print("NÃO IDENTIFICADO: Rosto não reconhecido.")

# Loop principal do programa
while True:
    print("---------------------------------------------------")
    print("O que deseja fazer?")
    print("1 - Cadastrar um rosto")
    print("2 - Verificar se um rosto está cadastrado")
    print("3 - Sair")

    opcao = input("Digite o número da opção desejada: ")

    if opcao == "1":
        new_face(input("Digite o nome da pessoa que deseja cadastrar: "))
    elif opcao == "2":
        identify_face()
    elif opcao == "3":
        print("Saindo do programa. Até mais!")
        break
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")