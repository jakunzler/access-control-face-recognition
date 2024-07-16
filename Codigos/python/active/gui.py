from database import *
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox, Label
import cv2
from PIL import Image, ImageTk
import face_recognition as fr
import numpy as np
from engine import *

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Carlos H Azevedo\Desktop\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.geometry("780x650")
window.configure(bg = "#FFFFFF")

# Defina a variável global para armazenar a imagem capturada
captured_frame = None

def facial_recognition(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = fr.face_locations(rgb_frame)
    face_encodings = fr.face_encodings(rgb_frame, face_locations)
    face = face_encodings
    return face

def cadastrar():
    global captured_frame
    if captured_frame is None:
        print("Erro: Nenhuma imagem foi capturada.")
        return

    # Processar a imagem para obter o encoding
    face_encodings = facial_recognition(captured_frame)
    if len(face_encodings) > 0:
        # Salvar o encoding no banco de dados
        insert_save_face_to_database(entry_1.get(), face_encodings[0], entry_2.get())
        print("Imagem salva no banco de dados.")
        mostrar_mensagem_sucesso()
        limpar_campos()
    else:
        exibir_erro("Erro: Nenhum rosto detectado na imagem capturada.")

def capturar():
    global captured_frame

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Could not open camera.")
        return
    
    while True:
        ret, frame = cam.read()
        cv2.imshow("Camera", frame)
        window.update()  # Atualiza a janela do Tkinter
        
        # Atualizar a variável global com o frame capturado
        captured_frame = frame
        
        if cv2.waitKey(1) & 0xFF == ord("f"):
            break
    
    cam.release()
    cv2.destroyAllWindows()

    # Processar a imagem para obter o encoding
    face_encodings = facial_recognition(captured_frame)
    if len(face_encodings) == 0:
        # Exibir mensagem de erro diretamente na janela
        messagebox.showerror("ERRO", "Rosto não encontrado")    
    else:
        # Exibir mensagem de sucesso diretamente na janela
        print("kkk")
        messagebox.showinfo("SUCESSO", "Rosto registrado com SUCESSO")

def mostrar_mensagem_sucesso():
    messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")

def limpar_campos():
    entry_1.delete(0, 'end')  # Limpa o conteúdo do Entry 1
    entry_2.delete(0, 'end')  # Limpa o conteúdo do Entry 2
    entry_1.focus_set()  # Define o foco no Entry 1 após limpar os campos

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 617,
    width = 774,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    387.0,
    68.0,
    image=image_image_1
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    388.3717956542969,
    381.4169807434082,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#F3EBEB",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=77.69784545898438,
    y=343.0,
    width=621.347900390625,
    height=74.8339614868164
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    388.3717956542969,
    237.48678970336914,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#F3EBEB",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=77.69784545898438,
    y=199.06980895996094,
    width=621.347900390625,
    height=74.8339614868164
)

canvas.create_text(
    68.0,
    149.0,
    anchor="nw",
    text="Nome",
    fill="#A4A4A4",
    font=("Poppins Regular", 20 * -1)
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    43.0,
    237.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    45.0,
    385.7981262207031,
    image=image_image_3
)

canvas.create_text(
    68.0,
    295.0,
    anchor="nw",
    text="Email",
    fill="#A4A4A4",
    font=("Poppins Regular", 20 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: cadastrar(),
    relief="flat",
    bg="white",  # Cor de fundo do botão
    fg="white",   # Cor do texto do botão
    activebackground="white"  # Cor de fundo quando o botão é clicado
)
button_1.place(
    x=209.0319061279297,
    y=551.8075561523438,
    width=357.4920654296875,
    height=65.19245910644531
)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: capturar(),
    relief="flat",
    bg="white",  # Cor de fundo do botão
    fg="white",  # Cor do texto do botão
    activebackground="white"  # Cor de fundo quando o botão é clicado
)
button_2.place(
    x=68.0,
    y=445.0,
    width=225.0,
    height=53.0
)
window.resizable(False, False)
window.mainloop()
