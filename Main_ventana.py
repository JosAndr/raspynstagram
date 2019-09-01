from multiprocessing import Process, Queue
import numpy as np
import PIL
import cv2
import imutils
import time
import tkinter as tk
from tkinter import *
from tkinter.filedialog import asksaveasfile
from PIL import ImageTk,Image 
from tkinter.ttk import *
###############################################################################################
face_det=cv2.CascadeClassifier('/usr/share/opencv/lbpcascades/lbpcascade_frontalface.xml')#clasificador pre-entrenado de reconcoimeinto facial
capflag=0;

#############################################################################################
        #DETECCIÖN FACIAL
#############################################################################################   
def detc_facial(imagen):
    imnoroi=cv2.cvtColor(imagen, cv2.COLOR_BGR2RGBA)#convirtiendo de BGR a RGB
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)#Convirtiendo de BGR a escala de grises
    faces = face_det.detectMultiScale( #función de detección 
    gris,     
    scaleFactor=1.2,
    minNeighbors=5,     
    minSize=(20, 20)
    )
    #############################################################################################
    #dibujando rectángulos sobre los rostros detectados
    for (x,y,w,h) in faces:
        cv2.rectangle(imagen,(x,y),(x+w,y+h),(255,255,255),2) #definiendo rectángulo para las ROI
        roi_gray = gris[y:y+h, x:x+w]#dibujando ROI sobre la imagen en escala de grises
        roi_color = imagen[y:y+h, x:x+w] #dibujando ROI sobre la imagen BGR
    return imagen
#############################################################################################
         #DETECCIÖN DE COLOR
#############################################################################################
def detc_color(imagen):
    imhsv=cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV) #convirtiendo de BGR a HSV
    #definiendo límites de color
    #ROJO 1
    redinf1=np.array([0,120,50])
    redsup1=np.array([10,255,255])
    maskr1=cv2.inRange(imhsv,redinf1,redsup1)
    #ROJO 2
    redinf2=np.array([170,120,50])
    redsup2=np.array([180,255,255])
    maskr2=cv2.inRange(imhsv,redinf2,redsup2)
    #AZUL
    blueinf1=np.array([110,128,50])
    bluesup1=np.array([130,255,255])
    maskb1=cv2.inRange(imhsv,blueinf1,bluesup1)
    #VERDE
    greeninf1=np.array([50,128,50])
    greensup1=np.array([70,255,255])
    maskg1=cv2.inRange(imhsv,greeninf1,greensup1)
    ############################################################################################
    #mascaras de color y transformación
    veci=np.ones((5, 5),"uint8")
    #ROJO
    mask_R=maskr1+maskr2
    redO=cv2.dilate(mask_R,veci)
    resR=cv2.bitwise_and(imagen, imagen, mask=redO)
    #AZUL
    mask_B=maskb1
    blueO=cv2.dilate(mask_B,veci)
    resB=cv2.bitwise_and(imagen, imagen, mask=blueO)
    #VERDE
    mask_G=maskg1
    greenO=cv2.dilate(mask_G,veci)
    resG=cv2.bitwise_and(imagen, imagen, mask=greenO)
    ###############################################################################################
    #seguimiento de color
    #ROJO
    contours, hierarchy=cv2.findContours(redO,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area=cv2.contourArea(contour)
        if area>5000:
            cv2.drawContours(imagen, contours, -1, (0,0,255),3)
    #AZUL
    contours, hierarchy=cv2.findContours(blueO,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area=cv2.contourArea(contour)
        if area>5000:
            cv2.drawContours(imagen, contours, -1, (255,0,0),3)
    #VERDE
    contours, hierarchy=cv2.findContours(greenO,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area=cv2.contourArea(contour)
        if area>5000:
            cv2.drawContours(imagen, contours, -1, (0,255,0),3)
    return imagen
###############################################################################################
        #VISUAlIZANDO IMAGEN
###############################################################################################   
def show_frame():
    global run
    try:
        _, frame = VS.read()#obteniendo los "frames" captados por la cámara
        imagen= cv2.flip(frame, 1) #invirtiendo para que la imagen coincida con la imagen real
        detc_facial(imagen)
        detc_color(imagen)
        cv2image = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGBA)#convirtiendo de BGR a RGB   
        img = Image.fromarray(cv2image)#convirtiendo matriz a imagen
        imgtk = ImageTk.PhotoImage(image=img)#convirtiendo la imagen a formato de fotografía
        lmain.configure(image=imgtk)
        lmain.image=imgtk
        run=lmain.after(1,show_frame)#tiempo de actualziación
    except RuntimeError as e:
        print("[INFO] caught a RuntimeError")
##############################################################################################
     #FUNCIÖN PARA CAPTURAR FRAME ACTUAL Y DETENER VIDEO
##############################################################################################        
def capture():
    capflag=1
    global imagen, imgtk 
    global run
    if run:
        mainwin.after_cancel(run)
        run=None
    _, frame = VS.read()#obteniendo los "frames" captados por la cámara
    imagen= cv2.flip(frame, 1) #invirtiendo para que la imagen coincida con la imagen real
    cv2image = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGBA)#convirtiendo de BGR a RGB   
    img = Image.fromarray(cv2image)#convirtiendo matriz a imagen
    imgtk = ImageTk.PhotoImage(image=img)#convirtiendo la imagen a formato de fotografía
    lmain.configure(image=imgtk)
    lmain.image=imgtk
##############################################################################################
     #FUNCIÖN PARA REACTIVAR VIDEO
##############################################################################################      
def reint():
    capflag=0
    time.sleep(1.0)
    show_frame()
##############################################################################################
     #FUNCIÖN PARA GUARDAR
##############################################################################################        

def guardar():
    global imagen, imgtk 
    f = tk.filedialog.asksaveasfile(filetypes=(("Portable Network Graphics (*.png)", "*.png"),("Joint Photographic ExpertGroup (*.jpg)","*.jpg"),
                                            ("All Files (*.*)", "*.*")),
                                 mode='wb',
                                 defaultextension='*.*')
    if f is None:
        return

    filename = f.name
    extension = filename.rsplit('.', 1)[-1]

    cv2.imwrite(filename, imagen)
    f.close()
#Creando ventana principal
mainwin=Tk()
tema=Style(mainwin)
tema.theme_use('classic')
mainwin.option_add("*Font", "helvetica")
mainwin.option_add("*Background", "white")
mainwin.config(background="white")
mainwin.geometry("360x370+300+20")#Tamaño y ubicación de la ventana
mainwin.title('Raspynstagram')#Nombre de la ventana
mainwin.resizable(0,0)#Inhabilitando reescalado de la ventana


############################################################################################
#Creando barra de menú
menubar=Menu(mainwin)
mainwin.config(menu=menubar)
#Creando menú de archivo

archivo=Menu(menubar, tearoff=0)

menubar.add_cascade(label="Archivo", menu=archivo)

archivo.add_command(label="Guardar", command=guardar)

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
#creando botón de reintentar
ret=tk.Button(mainwin, text='TOMAR DE NUEVO', command=reint)
ret.pack(side="bottom", fill="x", expand="yes",padx=4, pady=6)
#creando boton de captura
snap=tk.Button(mainwin, text='¡FOTO!', command=capture)
snap.pack(side="bottom", fill="x", expand="yes",padx=4, pady=6)
##############################################################################################
#Creando Lienzo principal
lmain = tk.Label(master=mainwin)
lmain.pack(side='left',padx=4, pady=3)
##############################################################################################
if capflag==0:
    VS=cv2.VideoCapture(0)
    VS.set(cv2.CAP_PROP_FRAME_WIDTH, 352)
    VS.set(cv2.CAP_PROP_FRAME_HEIGHT, 288)
    time.sleep(2.0)
    show_frame()
mainwin.protocol("WM_DELETE_WINDOW", quit)    
mainwin.mainloop()

