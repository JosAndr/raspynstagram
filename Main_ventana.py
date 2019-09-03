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
capflag=0 #bandera de captura de imagen estática

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
    return imagen #retonando la imagen a la variable global
#############################################################################################
         #DETECCIÖN DE COLOR
#############################################################################################
def detc_color(imagen):
    #Los valoresde H normalmente estan entre 0°y 360°, sin embargo en openCV estan normalizados a 0°-180°
    #debido al uso de uchart en éste parametro. Los valores de saturación(S) y brillo(V) estan de 0-255(bits), esto debe tenerse en cuenta
    #ya que en la mayoría de asistentes de color estoa valores estan en porcetaje(0-100%)
    imhsv=cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV) #convirtiendo de BGR a HSV
    #definiendo límites de color
    #ROJO 1
    redinf1=np.array([0,120,50])#límite inferior en HSV
    redsup1=np.array([10,255,255])#límte superior en HSV
    maskr1=cv2.inRange(imhsv,redinf1,redsup1)#umbralizando la imagen con los límites
    #ROJO 2
    redinf2=np.array([170,120,50])#límite inferior en HSV
    redsup2=np.array([180,255,255])#límte superior en HSV
    maskr2=cv2.inRange(imhsv,redinf2,redsup2)#umbralizando la imagen con los límites
    #para el rojo son necesarios 2 umbralizaciones debido a que en HSV los valores de intensidad de color(H) estan ordenados en una circunferencia
    #en la que el color rojo se encutra en el 0°. 
    #AZUL
    blueinf1=np.array([110,128,50])#límite inferior en HSV
    bluesup1=np.array([130,255,255])#límte superior en HSV
    maskb1=cv2.inRange(imhsv,blueinf1,bluesup1)
    #VERDE
    greeninf1=np.array([50,128,50])#límite inferior en HSV
    greensup1=np.array([70,255,255])#límte superior en HSV
    maskg1=cv2.inRange(imhsv,greeninf1,greensup1)#umbralizando la imagen con los límites
    ############################################################################################
    #mascaras de color y transformación
    veci=np.ones((5, 5),"uint8")#definiendo tamaño de máscara para transformación y segmentación
    #ROJO
    mask_R=maskr1+maskr2#generando máscara del rojo
    redO=cv2.morphologyEx(mask_R, cv2.MORPH_OPEN,veci,iterations=2) #transformación de apertura
    redO=cv2.dilate(redO,veci,iterations=1)#transformación de dilatación
    resR=cv2.bitwise_and(imagen, imagen, mask=redO)#aplicando la máscara a la imagen
    #AZUL
    mask_B=maskb1
    blueO=cv2.morphologyEx(mask_B,cv2.MORPH_OPEN,veci, iterations=2)#transformación de apertura
    blueO=cv2.dilate(blueO,veci,iterations=1)#transformación de dilatación
    resB=cv2.bitwise_and(imagen, imagen, mask=blueO)#aplicando la máscara a la imagen
    #VERDE
    mask_G=maskg1
    greenO=cv2.morphologyEx(mask_G,cv2.MORPH_OPEN,veci, iterations=2)#trasnformación de apertura
    greenO=cv2.dilate(greenO,veci,iterations=1)#transformación de dilatación
    resG=cv2.bitwise_and(imagen, imagen, mask=greenO)#aplicando la máscara a la imagen
    ###############################################################################################
    #seguimiento de color
    #ROJO
    contours, hierarchy=cv2.findContours(redO,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)#detectando el contorno en la máscara
    for contour in contours:
        area=cv2.contourArea(contour)
        if area>500:#ajustando un tamaño mínimo para realiza la marca del contorno
            cv2.drawContours(imagen, contours, -1, (0,0,255),3)#realizando el contorno de color rojo alrededor de los objetos de este color
    #AZUL
    contours, hierarchy=cv2.findContours(blueO,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)#detectando el contorno en la máscara
    for contour in contours:
        area=cv2.contourArea(contour)
        if area>500:#ajustando un tamaño mínimo para realiza la marca del contorno
            cv2.drawContours(imagen, contours, -1, (255,0,0),3)#realizando el contorno de color azul alrededor de los objetos de este color
    #VERDE
    contours, hierarchy=cv2.findContours(greenO,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)#detectando el contorno en la máscara
    for contour in contours:
        area=cv2.contourArea(contour)
        if area>500:#ajustando un tamaño mínimo para realiza la marca del contorno
            cv2.drawContours(imagen, contours, -1, (0,255,0),3)#realizando el contorno de color verde alrededor de los objetos de este color
    return imagen#retonando la imagen a la variable global
###############################################################################################
        #VISUAlIZANDO IMAGEN
###############################################################################################   
def show_frame():
    global run 
    try:
        _, frame = VS.read()#obteniendo los "frames" captados por la cámara
        imagen= cv2.flip(frame, 1) #invirtiendo para que la imagen coincida con la imagen real
        imagen=detc_facial(imagen)
        imagen=detc_color(imagen)
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
    capflag=1 #actualizando el valor de la bandera de captura a 1 para evitar ejecutar la captura de video
    global imagen, imgtk #se declaran variables globales para poder intercambiar entre video e imagen estática.
    global run#variable que captura la actulización del lienzo
    if run:  
        mainwin.after_cancel(run) #deteniendo el ciclo de actulización
        run=None # reiniciando el valor de "run"
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
    capflag=0 #reiniciando valor de la bandera de captura y permitir la ejecución de la captura de video
    time.sleep(1.0) #tiempo de espera para la cámara
    show_frame() #ejecutando nuevamente la captura de video
##############################################################################################
     #FUNCIÖN PARA GUARDAR
##############################################################################################        

def guardar():
    global imagen, imgtk #variables globales que pueden utilziarse para guardar
    f = tk.filedialog.asksaveasfile(filetypes=(("Portable Network Graphics (*.png)", "*.png"),("Joint Photographic ExpertGroup (*.jpg)","*.jpg"),
                                            ("All Files (*.*)", "*.*")),
                                 mode='wb',
                                 defaultextension='*.*')#invocando la función que abre ventana de dialogo, se asgignan las estensiones disponibles para guardar
    if f is None:
        return #si el nombre está vacio regresar a la ventana principal

    filename = f.name #obteniendo el nombre del archivo
    extension = filename.rsplit('.', 1)[-1] #asignando la extensión al archivo
    cv2.imwrite(filename, imagen)#guardando la imagen por medio de la función imwrite de OpenCV
    f.close()#cerrando la ventana de dialogo
################################################################################################
    #VETANA DE CONTRASTE
################################################################################################    
def contraste():
    adjcont=tk.Toplevel(mainwin)
    cont=DoubleVar()
    adjcont.title("Contraste")
    adjcont.geometry("300x100")
    slider=tk.Scale(adjcont,from_=-3, to=3, cursor="arrow", orient=HORIZONTAL,resolution=0.1, variable=cont,length=300)
    slider.pack(side="bottom",fill="x",expand="yes",padx=4, pady=6)
    valor=slider.get()
    img2np=np.double(imagen)
    imagen=np.uint8(img2np+valor)
################################################################################################
#FUNCIÓN PARA CREAR LA VENTANA PRINCIPAL
################################################################################################    
mainwin=Tk()
tema=Style(mainwin)
tema.theme_use('classic') #ajustando el tema principal
mainwin.option_add("*Font", "helvetica")#cambiando la fuente de la GUI
mainwin.option_add("*Background", "white")#cambiando el color de los widgets de la GUI
mainwin.config(background="white")#cambiando el color del fondo de la GUI
mainwin.geometry("360x370+300+20")#Tamaño y ubicación de la ventana
mainwin.title('Raspynstagram')#Nombre de la ventana
mainwin.resizable(0,0)#Inhabilitando reescalado de la ventana
#################################################################################################
#CREANDO LA BARRA DE MENÚ
#################################################################################################
menubar=Menu(mainwin)#asignando la ventana principal como "master" del widget menu
mainwin.config(menu=menubar)#asignando el nombre del widget menu como "menubar"

#Creando menú de archivo
archivo=Menu(menubar, tearoff=0)#eliminando la opción por defecto
menubar.add_cascade(label="Archivo", menu=archivo)#creando menú de cascada "Archivo"
archivo.add_command(label="Guardar", command=guardar)#Opción guardar, como comando llama a la función guardar()
archivo.add_separator()#agregando separador
archivo.add_command(label="Salir", command=quit)#agregando botón para salir de la GUI

#Creando menú de ajustes
ajustes=Menu(menubar, tearoff=0)
menubar.add_cascade(label="Ajustes", menu=ajustes)
ajustes.add_command(label="Invertir Color")
ajustes.add_command(label="Ajustar Contraste", command=contraste))
filtrar=Menu(ajustes, tearoff=0)
ajustes.add_cascade(label="Filtros", menu=filtrar)
filtrar.add_command(label="Espaciales")
filtrar.add_command(label="Frecuenciales")

###############################################################################################
#CREANDO BOTONES PARA INTERACTUAR CON LA VISUALIZACIÓN DE LA IMAGEN
###############################################################################################
#creando botón de reintentar
ret=tk.Button(mainwin, text='TOMAR DE NUEVO', command=reint)#Creando botón para reintentar la captura de la fotografía, como comando llama a la función reint()
ret.pack(side="bottom", fill="x", expand="yes",padx=4, pady=6)#Posición del botón
#creando boton de captura
snap=tk.Button(mainwin, text='¡FOTO!', command=capture)#Creando botón para realizar la captura de la fotografía, como comando llama a la función capture()
snap.pack(side="bottom", fill="x", expand="yes",padx=4, pady=6)
##############################################################################################
#Creando Lienzo de visualización
lmain = tk.Label(master=mainwin)
lmain.pack(side='left',padx=4, pady=3)
###############################################################################################
#EJECUCIÓN DE LA CAPTURA DE VIDEO
###############################################################################################
if capflag==0:#evaluando el valor de la bandera de captura
    VS=cv2.VideoCapture(0) #asignando la imagen capturada en la fuente 0 resgitrada en dev/video0
    VS.set(cv2.CAP_PROP_FRAME_WIDTH, 352)#asignando acho de la captura
    VS.set(cv2.CAP_PROP_FRAME_HEIGHT, 288)#asignando alto de la captura
    time.sleep(2.0)#dando tiempo de ajuste al sensor de la cámara
    show_frame()#llamando la fucnión que muestra como secuencia de video los frames capturados y los procesa
###############################################################################################
#CERRANDO LA APLICACIÖN
###############################################################################################
mainwin.protocol("WM_DELETE_WINDOW", quit)
###############################################################################################
mainwin.mainloop()

