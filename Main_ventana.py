import numpy
import PIL
import cv2
import imutils
import threading
import os
import time
import tkinter as tk
from tkinter import *
from PIL import ImageTk,Image 
from tkinter import ttk
face_det=cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt2.xml')#modelo pre-entrenado de reconcoimeinto facial
#Función para convertir matriz opencv a imagen tkinter a través de pillow
#Entradas matriz imagen de opencv tamaño deseado
#Salida imagen tkinter
def CV2TK(matcv,x, y):
    imagenpil=PIL.Image.fromarray(matcv)
    imagenpil.thumbnail((x, y))
    tempim=imagenpil.copy()
    dispim= PIL.ImageTk.PhotoImage(tempim)
    return dispim
#función para mostrar la imagen obtenida por la camara en la GUI
def show_frame():
    _, frame = VS.read()#obteniendo los "frames" captados por la cámara
    imagen= cv2.flip(frame, 1) #invirtiendo para que la imagen coincida con la imagen real
    imnoroi=cv2.cvtColor(imagen, cv2.COLOR_BGR2RGBA)#convirtiendo de BGR(opencv) a RGB
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)#convirtiendo de BGR a escala de grises
    faces = face_det.detectMultiScale( #función de detección del modelo pre-entrenado
        gris,     
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20)
    )
    for (x,y,w,h) in faces:
        cv2.rectangle(imagen,(x,y),(x+w,y+h),(255,0,0),2) #definiendo rectángulo para las ROI
        roi_gray = gris[y:y+h, x:x+w]#dibujando ROI sobre la imagen en escala de grises
        roi_color = imagen[y:y+h, x:x+w] #dibujando ROI sobre la imagen BGR  
    cv2image = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGBA)#convirtiendo de BGR(opencv)  RGB
    img = Image.fromarray(cv2image)#convirtiendo matriz a imagen
    imgtk = ImageTk.PhotoImage(image=img)#convirtiendo la imagen a formato de fotografía
    visor.create_image(0,0, anchor=NW, image=imgtk) #mostrando la imagen en el lienzo
    visor.after(10,show_frame)#tiempo de actualziación
    visor.update()#actualizando lienzo
    

#Creando ventana principal
mainwin=Tk()

mainwin.geometry("665x600+300+20")#Tamaño y ubicación de la ventana

mainwin.title('Raspynstagram')#Nombre de la ventana

mainwin.resizable(0,0)#Inhabilitando reescalado de la ventana

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

#Creando Lienzo principal

visor=Canvas(mainwin,width=640,height=480) #defnición del tamaño del lienzo
visor.place(x=21, y=29)#definición de la ubicación del lienzo

visor.create_text(230,230, fill="darkblue",font="Verdana",
                        text="Warming up.")
time.sleep(2.0)
VS=cv2.VideoCapture(0)
show_frame()
mainwin.mainloop()



