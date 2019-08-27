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
face_det=cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt2.xml')
#Función para convertir matriz opencv a imagen tkinter a través de pillow
#Entradas matriz imagen de opencv tamaño deseado
#Salida imagen tkinter
def CV2TK(matcv,x, y):
    imagenpil=PIL.Image.fromarray(matcv)
    imagenpil.thumbnail((x, y))
    tempim=imagenpil.copy()
    dispim= PIL.ImageTk.PhotoImage(tempim)
    return dispim

    
  

def show_frame():
    _, frame = VS.read()
    imagen= cv2.flip(frame, 1)
    imnoroi=cv2.cvtColor(imagen, cv2.COLOR_BGR2RGBA)
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    faces = face_det.detectMultiScale(
        gris,     
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20)
    )
    for (x,y,w,h) in faces:
        cv2.rectangle(imagen,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gris[y:y+h, x:x+w]
        roi_color = imagen[y:y+h, x:x+w]  
    cv2image = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    visor.create_image(0,0, anchor=NW, image=imgtk)
    visor.after(10,show_frame)
    visor.update()
    

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



