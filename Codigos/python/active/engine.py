import face_recognition as fr
import cv2
import numpy as np
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox, Label
import cv2
from PIL import Image, ImageTk
import face_recognition as fr
import numpy as np
from database import *

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

def capturarP():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Could not open camera.")
        return
    while True:
        ret, frame = cam.read()
        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            if ret:
                face_encodings = facial_recognition(frame)  # Use a função facial_recognition
                if len(face_encodings) > 0:
                    return face_encodings
            else:
                print("Não foi possível capturar a imagem.")
            break

    cam.release()
    cv2.destroyAllWindows()

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
                    insert_save_face_to_database(nome, face_encodings[0])
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

            known_faces = select_face_from_database()

            for nome, encoding_str in known_faces:
                known_face_encoding = np.fromstring(encoding_str[1:-1], dtype=float, sep=' ')
                match = fr.compare_faces([known_face_encoding], face_encoding, tolerance= 0.5)
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

