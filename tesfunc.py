#archivo para probar cosas
import numpy as np
import PIL
import cv2
import time
import tkinter as tk
from tkinter import *
from tkinter.filedialog import asksaveasfile
from PIL import ImageTk,Image 
from tkinter.ttk import *
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
################################################################################################
    #CLASE PARA LA CREACIÓN DE LA GUI
################################################################################################
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
class App:

    def __init__(self, mainwin, nombre):
        self.run=0 #bandera de actualización
        imagen=0
################################################################################################
    #FUNCIÓN PARA CREAR LA VENTANA PRINCIPAL
################################################################################################          
        self.mainwin=mainwin
        self.mainwin.title(nombre)
        self.tema=Style(mainwin)
        self.tema.theme_use('classic') #ajustando el tema principal
        self.mainwin.option_add("*Font", "helvetica")#cambiando la fuente de la GUI
        self.mainwin.option_add("*Background", "white")#cambiando el color de los widgets de la GUI
        self.mainwin.config(background="white")#cambiando el color del fondo de la GUI
        self.mainwin.geometry("360x370+300+20")#Tamaño y ubicación de la ventana
        self.mainwin.resizable(0,0)#Inhabilitando reescalado de la ventana
        self.VS=video()
#################################################################################################
        #CREANDO LA BARRA DE MENÚ
#################################################################################################
        self.menubar=Menu(self.mainwin)#asignando la ventana principal como "master" del widget menu
        self.mainwin.config(menu=self.menubar)#asignando el nombre del widget menu como "menubar"

        #Creando menú de archivo
        self.archivo=Menu(self.menubar, tearoff=0)#eliminando la opción por defecto
        self.menubar.add_cascade(label="Archivo", menu=self.archivo)#creando menú de cascada "Archivo"
        self.archivo.add_command(label="Guardar", command=self.guardar)#Opción guardar, como comando llama a la función guardar()
        self.archivo.add_separator()#agregando separador
        self.archivo.add_command(label="Salir", command=self.salir)#agregando botón para salir de la GUI
        #Creando menú de ajustes
        self.ajustes=Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Ajustes", menu=self.ajustes)
        self.ajustes.add_command(label="Invertir Color")
        self.ajustes.add_command(label="Ajustar Contraste")
        self.filtrar=Menu(self.ajustes, tearoff=0)
        self.ajustes.add_cascade(label="Filtros", menu=self.filtrar)
        self.filtrar.add_command(label="Espaciales")
        self.filtrar.add_command(label="Frecuenciales")
###############################################################################################
    #CREANDO BOTONES PARA INTERACTUAR CON LA VISUALIZACIÓN DE LA IMAGEN
###############################################################################################        
        #creando botón de reintentar
        ret=tk.Button(mainwin, text='TOMAR DE NUEVO', command=self.reint)#Creando botón para reintentar la captura de la fotografía, como comando llama a la función reint()
        ret.pack(side="bottom", fill="x", expand="yes",padx=4, pady=6)#Posición del botón
        #creando boton de captura
        self.snap=tk.Button(mainwin, text='¡FOTO!', command=self.capture)#Creando botón para realizar la captura de la fotografía, como comando llama a la función capture()
        self.snap.pack(side="bottom", fill="x", expand="yes",padx=4, pady=6)#Posición del botón
##############################################################################################
    #CREANDO LIENZO DE VISUALIZACIÓN
##############################################################################################
        self.lmain = tk.Label(master=mainwin)
        self.lmain.pack(side='left',padx=4, pady=3)
##############################################################################################
   #LLAMANDO ACTUALIZACIÓN DE LA IMAGEN
##############################################################################################
        self.actualizar()
        self.mainwin.mainloop()
##############################################################################################
   #FUNCIÓN DE ACTUALIZACIÓN
##############################################################################################        
    def actualizar(self):
        if self.run==0:#modo por defecto:visualización de video
            ret,frame, frame1=self.VS.get_frame() #llamando la función de obtención de imagen
            self.imagen=cv2.flip(frame, 1)#invirtiendo para que la imagen coincida con la imagen real
            if ret:#si hay "frames" capturados
                self.cv2image = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2RGBA)#convirtiendo de BGR a RGB   
                self.img = Image.fromarray(self.cv2image)#convirtiendo matriz a imagen
                self.imgtk = ImageTk.PhotoImage(image=self.img)#convirtiendo la imagen a formato de fotografía
                self.lmain.configure(image=self.imgtk)#definiendo fuente de la imagen del lienzo
                self.lmain.image=self.imgtk#mostrando la imagen en el lienzo
            self.lmain.after(1,self.actualizar)#reiniciando la función despues de 1 ms
        if self.run==1:#modo forzado:imagen estática
           ret,frame, frame1=self.VS.get_frame()
           self.imagen= cv2.flip(frame, 1) #invirtiendo para que la imagen coincida con la imagen real
           if ret:#si hay "frames" capturados
                self.cv2image = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2RGBA)#convirtiendo de BGR a RGB   
                self.img = Image.fromarray(self.cv2image)#convirtiendo matriz a imagen
                self.imgtk = ImageTk.PhotoImage(image=self.img)#convirtiendo la imagen a formato de fotografía
                self.lmain.configure(image=self.imgtk)#definiendo fuente de la imagen del lienzo
                self.lmain.image=self.imgtk#mostrando la imagen en el lienzo
                #no es necesaria función de actualización pues se quiere mantener el último "frmae" capturado estático
##############################################################################################
   #FUNCIONES PARA EL CAMBIO DE MODO ACTUALIZACIÓN
##############################################################################################   
    def capture(self):
      self.run=1 #cambiando el valor de la bandera
    def reint(self):
      self.run=0#reiniciando el valor del a bandera
      self.actualizar()#ejecutando la función de actulización para refrescar el valor de la bandera
##############################################################################################
   #FUNCIÓN PARA SALIR
##############################################################################################        
    def salir(self):
        self.mainwin.destroy()
##############################################################################################
   #FUNCIÓN PARA GUARDAR
##############################################################################################
    def guardar(self):
        self.f = tk.filedialog.asksaveasfile(filetypes=(("Portable Network Graphics (*.png)", "*.png"),("Joint Photographic ExpertGroup (*.jpg)","*.jpg"),
                                                ("All Files (*.*)", "*.*")),
                                     mode='wb',
                                     defaultextension='*.*')#invocando la función que abre ventana de dialogo, se asgignan las estensiones disponibles para guardar
        if self.f is None:
            return #si el nombre está vacio regresar a la ventana principal

        self.filename = self.f.name #obteniendo el nombre del archivo
        self.extension = self.filename.rsplit('.', 1)[-1] #asignando la extensión al archivo
        cv2.imwrite(self.filename, self.imagen)#guardando la imagen por medio de la función imwrite de OpenCV
        self.f.close()#cerrando la ventana de dialogo
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
################################################################################################
    #CLASE PARA LA CAPTURA DE VIDEO
################################################################################################
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
class video:
    def __init__(self):
        self.VS=cv2.VideoCapture(0)#asignando la imagen capturada en la fuente 0 resgitrada en dev/video0
        self.VS.set(cv2.CAP_PROP_FRAME_WIDTH, 352)#asignando acho de la captura
        self.VS.set(cv2.CAP_PROP_FRAME_HEIGHT, 288)#asignando alto de la captura
        self.frame1=None
        
        if	not	self.VS.isOpened():
            raiseValueError("Unable	to open	video source", 0)
    def get_frame(self):
        if self.VS.isOpened():
            ret,frame=self.VS.read()
            if self.frame1 is None:
                frame1= cv2.flip(frame, 1)
            if ret:
                return(ret, frame,  self.frame1)
            else:
                return (ret, None)
        else:
            return (ret, None)
    def __del__(self):
        if self.VS.isOpened():
            self.VS.release()
    
    
##############################################################################################
   #EJECUCIÓN DE LA GUI
############################################################################################## 
    
App(tk.Tk(),"Raspynstagram")

