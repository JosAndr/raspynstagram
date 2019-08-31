import numpy as np
import PIL
import cv2
import imutils
import threading
import os
import sys
import time
import tkinter as tk
from tkinter import *
from PIL import ImageTk,Image 
from tkinter.ttk import *
###############################################################################################
face_det=cv2.CascadeClassifier('/usr/share/opencv/lbpcascades/lbpcascade_frontalface.xml')#clasificador pre-entrenado de reconcoimeinto facial

###############################################################################################
#Función para convertir matriz opencv a imagen tkinter a través de pillow
#Entradas matriz imagen de opencv tamaño deseado
#Salida imagen tkinter
def CV2TK(matcv,x, y):
    imagenpil=PIL.Image.fromarray(matcv)
    imagenpil.thumbnail((x, y))
    tempim=imagenpil.copy()
    dispim= PIL.ImageTk.PhotoImage(tempim)
    return dispim
  
############################################################################################
#Creando ventana principal
mainwin=Tk()
tema=Style(mainwin)
tema.theme_use('classic')
mainwin.option_add("*Font", "helvetica")
mainwin.option_add("*Background", "white")
mainwin.config(background="white")
mainwin.geometry("360x340+300+20")#Tamaño y ubicación de la ventana
mainwin.title('Raspynstagram')#Nombre de la ventana
mainwin.resizable(0,0)#Inhabilitando reescalado de la ventana

############################################################################################
#Creando barra de menú
menubar=Menu(mainwin)
mainwin.config(menu=menubar)

#Creando menú de archivo

archivo=Menu(menubar, tearoff=0)

menubar.add_cascade(label="Archivo", menu=archivo)

archivo.add_command(label="Guardar")

archivo.add_separator()

archivo.add_command(label="Salir", command=quit)

#Creando menú de ajustes

ajustes=Menu(menubar, tearoff=0)

menubar.add_cascade(label="Ajustes", menu=ajustes)

ajustes.add_command(label="Invertir Color")

ajustes.add_command(label="Ajustar Contraste")

filtrar=Menu(ajustes, tearoff=0)

ajustes.add_cascade(label="Filtros", menu=filtrar)

filtrar.add_command(label="Espaciales")

filtrar.add_command(label="Frecuenciales")
###############################################################################################
#creando botón
snap=tk.Button(mainwin, text='¡FOTO!')
snap.pack(side="bottom", fill="both", expand="yes",padx=4, pady=3)
###############################################################################################
#Obteniendo imagen de la cámara

VS=cv2.VideoCapture(0)
VS.set(cv2.CAP_PROP_FRAME_WIDTH, 352)
VS.set(cv2.CAP_PROP_FRAME_HEIGHT, 288)
time.sleep(2.0)

##############################################################################################
#Creando Lienzo principal
lmain = tk.Label(master=mainwin)
lmain.pack(side='left',padx=4, pady=3)
##############################################################################################

#función para mostrar la imagen obtenida por la camara en la GUI
def show_frame():
    try:

        _, frame = VS.read()#obteniendo los "frames" captados por la cámara
        imagen= cv2.flip(frame, 1) #invirtiendo para que la imagen coincida con la imagen real
        imnoroi=cv2.cvtColor(imagen, cv2.COLOR_BGR2RGBA)#convirtiendo de BGR a RGB
        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)#convirtiendo de BGR a escala de grises
        imhsv=cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV) #convirtiendo de BGR a HSV
    ############################################################################################
        #definiendo límites de color
        redinf=np.array([0,0,255])
        redsup=np.array([123,123,255])
        
        blueinf=np.array([255,0,0])
        bluesup=np.array([255,123,123])

        greeninf=np.array([0,255,0])
        greensup=np.array([123,255,123])
    ############################################################################################
        #mascaras de color
        maskr=cv2.inRange(imhsv,redinf,redsup)
        redO=cv2.bitwise_and(imagen, imagen, mask=maskr)
        maskb=cv2.inRange(imhsv,blueinf,bluesup)
        blueO=cv2.bitwise_and(imagen, imagen, mask=maskb)
        maskg=cv2.inRange(imhsv,greeninf,greensup)
        greenO=cv2.bitwise_and(imagen, imagen, mask=maskg)
        imagen=cv2.add(imagen, redO)
    #############################################################################################
        faces = face_det.detectMultiScale( #función de detección del modelo pre-entrenado
            gris,     
            scaleFactor=1.2,
            minNeighbors=5,     
            minSize=(20, 20)
        )
    #############################################################################################
        #dibuajando rectnágulos sobre los rostros detectados
        for (x,y,w,h) in faces:
            cv2.rectangle(imagen,(x,y),(x+w,y+h),(255,0,0),2) #definiendo rectángulo para las ROI
            roi_gray = gris[y:y+h, x:x+w]#dibujando ROI sobre la imagen en escala de grises
            roi_color = imagen[y:y+h, x:x+w] #dibujando ROI sobre la imagen BGR
    #############################################################################################        
        cv2image = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGBA)#convirtiendo de BGR a RGB   
        img = Image.fromarray(cv2image)#convirtiendo matriz a imagen
        imgtk = ImageTk.PhotoImage(image=img)#convirtiendo la imagen a formato de fotografía
        lmain.configure(image=imgtk)
        lmain.image=imgtk
        lmain.after(1,show_frame)#tiempo de actualziación
        #lmain.update()
    except RuntimeError as e:
        print("[INFO] caught a RuntimeError")
show_frame()


mainwin.mainloop()
VS.release()



