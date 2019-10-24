##########################################################
#---------------------RASPYNSTAGRAM----------------------#
#----------UNIVERSIDAD PONTIFICIA BOLIVARIANA------------#
#-----------PROCESAMIENTO DIGITAL DE IMÁGENES------------#
#........................................................#
#---------JULIÁN FERNANDO BOHÓRQUEZ GUTIÉRREZ------------#
#---------------JOSÉ ANDRÉS PÉREZ RIVERO-----------------#
#-----------PhD.MIGUEL ALFONSO ALTUVE PAREDES------------#
#........................................................#
##########################################################
import numpy as np
import PIL
import cv2
import time
import tkinter as tk
from tkinter import *
from tkinter.filedialog import asksaveasfile
from PIL import ImageTk,Image 
from tkinter.ttk import *
from math import *
from scipy.interpolate import UnivariateSpline
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
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
        self.imagen=0
        self.imagenbup=0
        self.faceflag=0
        self.colorflag=0
        self.contrflag=0
        self.invflag=0
        self.grayflag=0
        self.bwflag=0
        self.smoothflag=0
        self.cartoonflag=0
        self.coldflag=0
        self.warmflag=0
        self.filtflag=0
        self.flagr=0
        self.flagg=0
        self.flagb=0
#***********************************************************************************************
################################################################################################
        #APARTADO GRÁFICO/VISUAL
################################################################################################
#***********************************************************************************************
        
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
        #Menu de detección
        self.deteccion=Menu(self.menubar, tearoff=0) 
        self.menubar.add_cascade(label="Detección", menu=self.deteccion)
        self.deteccion.add_command(label="Detección Facial",command=self.faceon)
        self.deteccion.add_command(label="Detección de Color",command=self.coloron)
        #Creando menú de mejoramiento
        self.ajustes=Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Ajustar", menu=self.ajustes)
        self.ajustes.add_command(label="Contraste",command=self.contraste)
        self.ajustes.add_command(label="Suavizar",command=self.smooth)
        #Menu de color
        self.color=Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label="Color", menu=self.color)
        self.color.add_command(label="Invertir Color",command=self.inv)
        self.color.add_command(label="Escala de Grises",command=self.gray)
        self.color.add_command(label="Blanco y negro",command=self.bw)
        self.color.add_command(label="Caricatura",command=self.cartoon_on)
        self.color.add_command(label="Frio",command=self.cold_on)
        self.color.add_command(label="Calido",command=self.warm_on)
        #Menu de filtros
        self.filtros=Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label="Filtros", menu=self.filtros)
        self.filtros.add_command(label="Espectro",command=self.espectrum)
        self.filtros.add_command(label="Pasa Bajos",command=self.lpf)
        self.filtros.add_command(label="Pasa Altos",command=self.hpf)
        self.filtros.add_command(label="Pasa Banda",command=self.bpf)
        self.filtros.add_command(label="Rechaza Banda",command=self.rpf)
###############################################################################################
    #CREANDO BOTONES PARA INTERACTUAR CON LA VISUALIZACIÓN DE LA IMAGEN
###############################################################################################        
        #creando botón de reintentar
        self.ret=tk.Button(mainwin, text='TOMAR DE NUEVO', command=self.reint)#Creando botón para reintentar la captura de la fotografía, como comando llama a la función reint()
        self.ret.pack(side="bottom", fill="x", expand="yes",padx=4, pady=6)#Posición del botón
        #creando boton de captura
        self.snap=tk.Button(mainwin, text='¡FOTO!', command=self.capture)#Creando botón para realizar la captura de la fotografía, como comando llama a la función capture()
        self.snap.pack(side="bottom", fill="x", expand="yes",padx=4, pady=6)#Posición del botón
##############################################################################################
    #CREANDO LIENZO DE VISUALIZACIÓN
##############################################################################################
        self.lmain = tk.Label(master=mainwin) #label de visualización
        self.lmain.pack(side='left',padx=4, pady=3) #posición del label     
##############################################################################################
   #LLAMANDO ACTUALIZACIÓN DE LA IMAGEN
##############################################################################################
        time.sleep(2.0)#tiempo de espera para el obturador
        self.actualizar()#llamando función de actulización
        self.mainwin.mainloop() #inicializando GUI
#-----------------------------------------------------------------------------------------------------------
################################################################################################
    #VENTANA DE CONTRASTE
################################################################################################    
    def contraste(self):
        self.contrflag=1
        self.adjcont=tk.Toplevel(self.mainwin)
        self.cont=DoubleVar()
        self.adjcont.title("Contraste")
        self.adjcont.geometry("300x100+670+20")
        self.slider=tk.Scale(self.adjcont,from_=0.001, to=3, cursor="arrow", orient=HORIZONTAL,resolution=0.001,showvalue=NO, variable=self.cont,length=300,command=self.conts)
        self.slider.set(1)
        self.slider.pack(side="bottom",fill="x",expand="yes",padx=4, pady=6)
        self.adjcont.protocol("WM_DELETE_WINDOW", self.closecont)
##############################################################################################
   #FUNCIÓN PARA CERRAR VENTANA DE CONTRASTE
##############################################################################################        
    def closecont(self):
        self.contrflag=0
        self.imagenbup=self.imagen
        self.adjcont.destroy()
#-----------------------------------------------------------------------------------------------------------
################################################################################################
    #VENTANA DE SUAVIZADO
################################################################################################    
    def smooth(self):
        self.smoothflag=1
        self.suavizar=tk.Toplevel(self.mainwin)
        self.smth=1
        self.suavizar.title("Suavizado")
        self.suavizar.geometry("300x100+670+20")
        self.sigsli=tk.Scale(self.suavizar,from_=1, to=10, cursor="arrow", orient=HORIZONTAL,showvalue=NO, variable=self.smth,length=300,command=self.suaval)
        self.sigsli.set(1)
        self.sigsli.pack(side="bottom",fill="x",expand="yes",padx=4, pady=6)
        self.suavizar.protocol("WM_DELETE_WINDOW", self.closesuav)
##############################################################################################
   #FUNCIÓN PARA CERRAR VENTANA DE SUAVIZADO
##############################################################################################        
    def closesuav(self):
        self.smoothflag=0
        self.imagenbup=self.imagen
        self.suavizar.destroy()
##############################################################################################
   #VENTANA DE FILTROS
##############################################################################################
    def espectrum(self):
        self.filtflag=0
        self.frec=tk.Toplevel(self.mainwin)
        self.frec.title("Frecuencia R")
        self.frec.geometry("360x450+670+20")
        self.hp=tk.Button(self.frec, text='ROJO',command=self.rf)
        self.hp.pack(side="bottom", fill="x", expand="yes",padx=4, pady=1)
        self.lp=tk.Button(self.frec, text='VERDE',command=self.gf)
        self.lp.pack(side="bottom", fill="x", expand="yes",padx=4, pady=1)
        self.color=tk.Button(self.frec, text='AZUL',command=self.bf)
        self.color.pack(side="bottom", fill="x", expand="yes",padx=4, pady=1)
        #------------------------------------------------------------------------------------------
        self.b,self.g,self.r=cv2.split(self.imagen)#separar image en canales
        self.dtfsR=np.fft.fftshift(cv2.dft(np.float32(self.r),flags = cv2.DFT_COMPLEX_OUTPUT))#transformada de Fourier del canal rojo
        self.Rcomplex= self.dtfsR[:,:,0] + 1j* self.dtfsR[:,:,1]#valores complejos de transformada de Fourier
        self.Rabs=np.abs(self.Rcomplex) + 1 #magnitud de los valores de la transformada de Fourier del canal rojo
        self.Rumb=20 * np.log(self.Rabs)#umbralización de los valores de la transformada
        self.rspec=255 * self.Rumb / np.max(self.Rumb) #normalizando de 0 a 255
        self.rspec= self.rspec.astype(np.uint8)#convirtiendo a uint8 para permitir la visualización
        #------------------------------------------------------------------------------------------
        self.Vspect = tk.Label(master=self.frec)
        self.Vspect.pack(side='left',padx=4, pady=3)
        self.imgspect=Image.fromarray(self.rspec)
        self.specttk = ImageTk.PhotoImage(image=self.imgspect)#convirtiendo la imagen a formato de fotografía
        self.Vspect.configure(image=self.specttk)#definiendo fuente de la imagen del lienzo
        self.Vspect.image=self.specttk
        self.frec.protocol("WM_DELETE_WINDOW", self.especlose)
    def especlose(self):
        self.imagen=cv2.merge([self.b,self.g,self.r])
        self.flagr=0
        self.flagg=0
        self.flagb=0
        self.showst()
        self.frec.destroy()
    def filtslide(self):
        self.filtwin=tk.Toplevel(self.mainwin)
        self.sigmaf=DoubleVar()
        self.centf=DoubleVar()
        self.filtwin.title("Frecuencia y Radio")
        self.filtwin.geometry("300x200+670+20")
        self.sigmsli=tk.Scale(self.filtwin,from_=1, to=100, cursor="arrow", orient=HORIZONTAL,resolution=0.001,showvalue=YES, variable=self.sigmaf,length=300,command=self.filt)
        self.sigmsli.set(3)
        self.sigmsli.pack(side="bottom",fill="x",expand="yes",padx=4, pady=6)
        self.frec=tk.Scale(self.filtwin,from_=1, to=100, cursor="arrow", orient=HORIZONTAL,resolution=0.001,showvalue=YES, variable=self.centf,length=300)
        self.frec.set(3)
        self.frec.pack(side="bottom",fill="x",expand="yes",padx=4, pady=6)
        self.filtwin.protocol("WM_DELETE_WINDOW", self.filtclose)
    def filtclose(self):
        self.filtwin.destroy()
#********************************************************************************************
#############################################################################################
    #CALLBACKS Y FUCIONES
#############################################################################################
#********************************************************************************************
        
#############################################################################################
    #DETECCIÖN FACIAL
#############################################################################################   
    def detc_facial(self):
        self.face_det=cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')#clasificador pre-entrenado de reconcoimeinto facial
        self.imnoroi=cv2.cvtColor(self.imagen, cv2.COLOR_BGR2RGBA)#convirtiendo de BGR a RGB
        self.gris=cv2.cvtColor(self.imagen,cv2.COLOR_BGR2GRAY)
        self.faces = self.face_det.detectMultiScale( #función de detección 
        self.gris,     
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20)
        )
        #dibujando rectángulos sobre los rostros detectados
        for (x,y,w,h) in self.faces:
            cv2.rectangle(self.imagen,(x,y),(x+w,y+h),(200,255,3),2) #definiendo rectángulo para las ROI
            self.roi_color = self.imagen[y:y+h, x:x+w] #dibujando ROI sobre la imagen BGR
#############################################################################################
    #FUNCION PARA ACTIVAR/DESACTIVAR DETECCIÖN FACIAL
#############################################################################################              
    def faceon(self):
        if self.faceflag==0:
            self.faceflag=1
            self.showst()
        elif self.faceflag==1:
            self.faceflag=0
            self.imagen=self.imagenbup
            self.showst()
#############################################################################################
         #DETECCIÖN DE COLOR
#############################################################################################
    def detc_color(self):
        #Los valoresde H normalmente estan entre 0°y 360°, sin embargo en openCV estan normalizados a 0°-180°
        #debido al uso de uchart en éste parametro. Los valores de saturación(S) y brillo(V) estan de 0-255(bits), esto debe tenerse en cuenta
        #ya que en la mayoría de asistentes de color estoa valores estan en porcetaje(0-100%)
        self.imhsv=cv2.cvtColor(self.imagen, cv2.COLOR_BGR2HSV) #convirtiendo de BGR a HSV
        #definiendo límites de color
        #ROJO 1
        self.redinf1=np.array([0,120,50])#límite inferior en HSV
        self.redsup1=np.array([10,255,255])#límte superior en HSV
        self.maskr1=cv2.inRange(self.imhsv,self.redinf1,self.redsup1)#umbralizando la imagen con los límites
        #ROJO 2
        self.redinf2=np.array([170,120,50])#límite inferior en HSV
        self.redsup2=np.array([180,255,255])#límte superior en HSV
        self.maskr2=cv2.inRange(self.imhsv,self.redinf2,self.redsup2)#umbralizando la imagen con los límites
        #para el rojo son necesarios 2 umbralizaciones debido a que en HSV los valores de intensidad de color(H) estan ordenados en una circunferencia
        #en la que el color rojo se encutra en el 0°. 
        #AZUL
        self.blueinf1=np.array([110,128,50])#límite inferior en HSV
        self.bluesup1=np.array([130,255,255])#límte superior en HSV
        self.maskb1=cv2.inRange(self.imhsv,self.blueinf1,self.bluesup1)
        #VERDE
        self.greeninf1=np.array([50,128,50])#límite inferior en HSV
        self.greensup1=np.array([70,255,255])#límte superior en HSV
        self.maskg1=cv2.inRange(self.imhsv,self.greeninf1,self.greensup1)#umbralizando la imagen con los límites
        ############################################################################################
        #mascaras de color y transformación
        self.veci=np.ones((5, 5),"uint8")#definiendo tamaño de máscara para transformación y segmentación
        #ROJO
        self.mask_R=self.maskr1+self.maskr2#generando máscara del rojo
        self.redO=cv2.morphologyEx(self.mask_R, cv2.MORPH_OPEN,self.veci,iterations=2) #transformación de apertura
        self.redO=cv2.dilate(self.redO,self.veci,iterations=1)#transformación de dilatación
        self.resR=cv2.bitwise_and(self.imagen,self.imagen,mask=self.redO)#aplicando la máscara a la imagen
        #AZUL
        self.mask_B=self.maskb1
        self.blueO=cv2.morphologyEx(self.mask_B,cv2.MORPH_OPEN,self.veci, iterations=2)#transformación de apertura
        self.blueO=cv2.dilate(self.blueO,self.veci,iterations=1)#transformación de dilatación
        self.resB=cv2.bitwise_and(self.imagen, self.imagen, mask=self.blueO)#aplicando la máscara a la imagen
        #VERDE
        self.mask_G=self.maskg1
        self.greenO=cv2.morphologyEx(self.mask_G,cv2.MORPH_OPEN,self.veci, iterations=2)#trasnformación de apertura
        self.greenO=cv2.dilate(self.greenO,self.veci,iterations=1)#transformación de dilatación
        self.resG=cv2.bitwise_and(self.imagen, self.imagen, mask=self.greenO)#aplicando la máscara a la imagen
        ###############################################################################################
        #seguimiento de color
        #ROJO
        self.contours, self.hierarchy=cv2.findContours(self.redO,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)#detectando el contorno en la máscara
        for contour in self.contours:
            self.area=cv2.contourArea(contour)
            if self.area>500:#ajustando un tamaño mínimo para realiza la marca del contorno
                cv2.drawContours(self.imagen, self.contours, -1, (0,0,255),3)#realizando el contorno de color rojo alrededor de los objetos de este color
        #AZUL
        self.contours, self.hierarchy=cv2.findContours(self.blueO,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)#detectando el contorno en la máscara
        for contour in self.contours:
            self.area=cv2.contourArea(contour)
            if self.area>500:#ajustando un tamaño mínimo para realiza la marca del contorno
                cv2.drawContours(self.imagen,self.contours, -1, (255,0,0),3)#realizando el contorno de color azul alrededor de los objetos de este color
        #VERDE
        self.contours,self.hierarchy=cv2.findContours(self.greenO,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)#detectando el contorno en la máscara
        for contour in self.contours:
            self.area=cv2.contourArea(contour)
            if self.area>500:#ajustando un tamaño mínimo para realiza la marca del contorno
                cv2.drawContours(self.imagen,self. contours, -1, (0,255,0),3)#realizando el contorno de color verde alrededor de los objetos de este color
#############################################################################################
    #FUNCION PARA ACTIVAR/DESACTIVAR DETECCIÖN DE COLOR
#############################################################################################              
    def coloron(self):
        if self.colorflag==0:
            self.colorflag=1
            self.showst()
        elif self.colorflag==1:
            self.colorflag=0
            self.imagen=self.imagenbup
            self.showst()
#############################################################################################
    #COLD
#############################################################################################
    def cold(self):
        self.uplut= UnivariateSpline([0, 64, 128, 192, 256],[0, 70, 140, 210, 256])#Generando un spline de intercambio de valores ascendente
        self.uplut=self.uplut(range(256))#LookUpTable con los valores modificados
        self.downlut=UnivariateSpline([0, 64, 128, 192, 256],[0, 30,  80, 120, 192])#Generando un spline de intercambio de valores descendente
        self.downlut=self.downlut(range(256))#LookUpTable con los valores modificados
        self.color=self.imagen
        self.b, self.g, self.r=cv2.split(self.color)#separando la imagen en canales bgr
        self.b=cv2.LUT(self.b,self.uplut).astype(np.uint8) #aplicando LUT de valores ascendentes al color azul
        self.r=cv2.LUT(self.r,self.downlut).astype(np.uint8)#aplicando LUT de valores descendentes al color rojo
        self.color=cv2.merge((self.b,self.g,self.r))#reagrupando los canales en bgr
        
        self.color=cv2.cvtColor(self.color, cv2.COLOR_BGR2HSV)#convirtiendo a hsv
        self.h,self.s,self.v=cv2.split(self.color)#separando imagen en sus valores hsv
        self.s=cv2.LUT(self.s,self.downlut).astype(np.uint8)#aplicando LUT descendente al valor de saturación
        self.color=cv2.cvtColor(cv2.merge((self.h,self.s,self.v)), cv2.COLOR_HSV2BGR)#reagrupando los canales en hsv
        self.imagen= self.color
#############################################################################################
    #ACTIVAR FUNCION COLD
#############################################################################################              
    def cold_on(self):
        if self.coldflag==0:
            self.coldflag=1
            self.imagen=self.imagenbup
            self.showst()
        elif self.coldflag==1:
            self.coldflag=0
            self.imagen=self.imagenbup
            self.showst()
#############################################################################################
    #WARM
#############################################################################################
    def warm(self):
        self.uplut= UnivariateSpline([0, 64, 128, 192, 256],[0, 70, 140, 210, 256])#Generando un spline de intercambio de valores ascendente
        self.uplut=self.uplut(range(256))#LookUpTable con los valores modificados
        self.downlut=UnivariateSpline([0, 64, 128, 192, 256],[0, 30,  80, 120, 192])#Generando un spline de intercambio de valores descendente
        self.downlut=self.downlut(range(256))#LookUpTable con los valores modificados
        self.color=self.imagen
        self.b, self.g, self.r=cv2.split(self.color)#separando la imagen en canales bgr
        self.r=cv2.LUT(self.r,self.uplut).astype(np.uint8)#aplicando LUT de valores ascendentes al color rojo
        self.b=cv2.LUT(self.b,self.downlut).astype(np.uint8)#aplicando LUT de valores descendentes al color azul
        self.color=cv2.merge((self.b,self.g,self.r))#reagrupando los canales en bgr
        
        self.color=cv2.cvtColor(self.color, cv2.COLOR_BGR2HSV)#convirtiendo a hsv
        self.h,self.s,self.v=cv2.split(self.color)#separando imagen en sus valores hsv
        self.s=cv2.LUT(self.s,self.uplut).astype(np.uint8)#aplicando LUT descendente al valor de saturación
        self.color=cv2.cvtColor(cv2.merge((self.h,self.s,self.v)), cv2.COLOR_HSV2BGR)#reagrupando los canales en hsv
        self.imagen= self.color
#############################################################################################
    #ACTIVAR FUNCION WARM
#############################################################################################              
    def warm_on(self):
        if self.warmflag==0:
            self.warmflag=1
            self.showst()
        elif self.warmflag==1:
            self.warmflag=0
            self.imagen=self.imagenbup
            self.showst()
##############################################################################################
  #FUNCIÓN DE ACTUALIZACIÓN
##############################################################################################        
    def actualizar(self):
        ret,frame, frame1=self.VS.get_frame() #llamando la función de obtención de imagen
        self.imagen=cv2.flip(frame, 1)#invirtiendo para que la imagen coincida con la imagen real
        self.b,self.g,self.r=cv2.split(self.imagen)
        #reiniciando valores de las banderas
        self.imagenbup=self.imagen
        self.faceflag=0
        self.colorflag=0
        self.contrflag=0
        self.invflag=0
        self.grayflag=0
        self.bwflag=0
        self.smoothflag=0
        self.cartoonflag=0
        self.coldflag=0
        self.warmflag=0
        if ret:#si hay "frames" capturados
            self.cv2image = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2RGBA)#convirtiendo de BGR a RGB   
            self.img = Image.fromarray(self.cv2image)#convirtiendo matriz a imagen
            self.imgtk = ImageTk.PhotoImage(image=self.img)#convirtiendo la imagen a formato de fotografía
            self.lmain.configure(image=self.imgtk)#definiendo fuente de la imagen del lienzo
            self.lmain.image=self.imgtk#mostrando la imagen en el lienzo
        if self.run==0:#modo por defecto:visualización de video
           self.lmain.after(1,self.actualizar)#reiniciando la función 
            
        if self.run==1:#modo forzado:imagen estática
           self.showst()
##############################################################################################
   #FUNCIONES PARA EL CAMBIO DE MODO ACTUALIZACIÓN
##############################################################################################   
    def capture(self):#Modo estático/tomar fotografía
      self.run=1 #cambiando el valor de la bandera
    def reint(self):#Modo video
      self.run=0#reiniciando el valor del a bandera
      self.actualizar()
    def showst(self): #modo estático
        if self.faceflag==1:
           self.detc_facial()
            #..............................................................
        if self.colorflag==1:
            self.detc_color()
            #..............................................................
        if self.invflag==1:
            self.imagen=cv2.bitwise_not(self.imagen)#función de inversión de la imagen
            #.............................................................
        if self.grayflag==1:
            self.imagen=cv2.cvtColor(self.imagen,cv2.COLOR_BGR2GRAY)#conversión a escala de grises
            #.............................................................
        if self.bwflag==1:
            self.grisesc=cv2.cvtColor(self.imagen,cv2.COLOR_BGR2GRAY).astype('uint8')
            self.imagen = cv2.adaptiveThreshold(self.grisesc,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)#umbralización adaptativa
            #........................................................................................................
        if self.cartoonflag==1:
            self.cartoon()
            #........................................................................................................
        if self.coldflag==1:
            self.cold()
            #........................................................................................................
        if self.warmflag==1:
            self.warm()
        if self.flagr==1:
            self.imagen=self.r
        if self.flagg==1:
            self.imagen=self.g
        if self.flagb==1:
            self.imagen=self.b
        self.cv2image = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2RGBA)#convirtiendo de BGR a RGB   
        self.img = Image.fromarray(self.cv2image)#convirtiendo matriz a imagen
        self.imgtk = ImageTk.PhotoImage(image=self.img)#convirtiendo la imagen a formato de fotografía
        self.lmain.configure(image=self.imgtk)#definiendo fuente de la imagen del lienzo
        self.lmain.image=self.imgtk#mostrando la imagen en el lienzo
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
##############################################################################################
   #FUNCIÓN PARA AJUSTAR EL CONTRASTE
##############################################################################################     
    def conts(self,gamma):
        self.imagen=self.imagenbup
        self.bg,self.gg,self.rg=cv2.split(self.imagen) #obteniendo los canales bgr
        self.gamma=self.slider.get()#obteniendo el valor del slider de la gamma
        self.invgamma=1/self.gamma #generando el valor de gamma inversa
        self.table=np.array([((self.i / 255.0) ** self.invgamma) * 255 #generando LUT con el valor de gamma inversa 
		for self.i in np.arange(0, 256)]).astype("uint8")
        #aplicando la LUT con los valors de gamma inversa a cada canal
        self.bg=cv2.LUT(self.bg,self.table)
        self.gg=cv2.LUT(self.gg,self.table)
        self.rg=cv2.LUT(self.rg,self.table)
        self.imagen=cv2.merge([self.bg,self.gg,self.rg])#reagrupando los canales bgr
        self.showst()
##############################################################################################
   #FUNCIÓN PARA SUAVIZAR
##############################################################################################     
    def suaval(self,sigma):
        self.imagen=self.imagenbup
        self.scolor=self.imagen
        self.iter=self.sigsli.get()#obteniendo el valor del slider de suavizado
        self.scolor=cv2.bilateralFilter(self.scolor,self.iter,3*self.iter,3*self.iter)#aplicando suavizado bilateral
        self.imagen=self.scolor
        self.showst()
##############################################################################################
   #INVERTIR COLOR
##############################################################################################     
    def inv(self):
        if self.invflag==0:
            self.invflag=1
            self.showst()
        elif self.invflag==1:
            self.invflag=0
            self.imagen=self.imagenbup
            self.showst()
##############################################################################################
  #ESCALA DE GRISES
##############################################################################################     
    def gray(self):
        if self.grayflag==0:
            self.grayflag=1
            self.showst()
        elif self.grayflag==1:
            self.grayflag=0
            self.imagen=self.imagenbup
            self.showst()
##############################################################################################
  #B&W
##############################################################################################     
    def bw(self):
        if self.bwflag==0:
            self.bwflag=1
            self.showst()
        elif self.bwflag==1:
            self.bwflag=0
            self.imagen=self.imagenbup
            self.showst()
##############################################################################################
  #CARICATURA
##############################################################################################     
    def cartoon(self):
       self.color=self.imagen
       self.down=2 #bandera para reduccion de tamaño
       self.bildif=7#valor de aplicación de filtro bilateral
       for _ in range(self.down):
           self.color=cv2.pyrDown(self.color)#aplicación de disminución de tamaño
       for _ in range(self.bildif):
           self.color=cv2.bilateralFilter(self.color,5,5,3)#aplicación del filtro bilateral
       for _ in range(self.down):
           self.color=cv2.pyrUp(self.color)  #regresando al valor original 
       self.graysc=cv2.cvtColor(self.imagen, cv2.COLOR_BGR2GRAY) #convirtiendo a escala de grises
       self.dif=cv2.medianBlur(self.graysc, 7) #aplicando filtro de media
       self.bordes=cv2.adaptiveThreshold(self.dif,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,blockSize=9,C=2)#obteniendo bordes por umbralización adaptativa
       self.bordes=cv2.cvtColor(self.bordes, cv2.COLOR_GRAY2BGR)#convirtiendo de gris a bgr
       self.imagen=cv2.bitwise_and(self.color, self.bordes)#realizando función and con los bordes y la imagen suavizada
##############################################################################################
  #HABILITANDO CARICATURA
##############################################################################################     
    def cartoon_on(self):
       if self.cartoonflag==0:
            self.cartoonflag=1
            self.showst()
       elif self.cartoonflag==1:
           self.cartoonflag=0
           self.imagen=self.imagenbup
           self.showst()
##############################################################################################
  #FILTROS DE FRECUENCIA
##############################################################################################   
    def rf(self):
        self.frec.title("Frecuencia R")
        self.flagr=1
        self.flagg=0
        self.flagb=0
        #self.b,self.g,self.r=cv2.split(self.imagen)# seprando canales  bgr
        self.dtfsR=np.fft.fftshift(cv2.dft(np.float32(self.r),flags = cv2.DFT_COMPLEX_OUTPUT))#dft sobre el canal rojo
        self.Rcomplex= self.dtfsR[:,:,0] + 1j* self.dtfsR[:,:,1]#valores complejos de la dft
        self.Rabs=np.abs(self.Rcomplex) + 1#magnitud de los valores de la dft
        self.Rumb=20 * np.log(self.Rabs)#umbralización de los valores de la dft
        self.rspec=255 * self.Rumb / np.max(self.Rumb)#normalización de los valores entre 0 y 255
        self.rspec= self.rspec.astype(np.uint8)#conversión a uint8
        #-----------------------------------------------------------------------------------------
        self.Rimgspect=Image.fromarray(self.rspec)
        self.Rspecttk = ImageTk.PhotoImage(image=self.Rimgspect)#convirtiendo la imagen a formato de fotografía
        self.Vspect.configure(image=self.Rspecttk)#definiendo fuente de la imagen del lienzo
        self.Vspect.image=self.Rspecttk
        self.showst()
    def gf(self):
        self.frec.title("Frecuencia G")
        self.flagg=1
        self.flagr=0
        self.flagb=0
        #self.b,self.g,self.r=cv2.split(self.imagen)# seprando canales  bgr
        self.dtfsG=np.fft.fftshift(cv2.dft(np.float32(self.g),flags = cv2.DFT_COMPLEX_OUTPUT))#dft sobre el canal verde
        self.Gcomplex= self.dtfsG[:,:,0] + 1j* self.dtfsG[:,:,1]#valores complejos de la dft
        self.Gabs=np.abs(self.Gcomplex) + 1#magnitud de los valores de la dft
        self.Gumb=20 * np.log(self.Gabs)#umbralización de los valores de la dft
        self.gspec=255 * self.Gumb/ np.max(self.Gumb)#normalización de los valores entre 0 y 255
        self.gspec= self.gspec.astype(np.uint8)#conversión a uint8
        #------------------------------------------------------------------------------------------
        self.Gimgspect=Image.fromarray(self.gspec)
        self.Gspecttk = ImageTk.PhotoImage(image=self.Gimgspect)#convirtiendo la imagen a formato de fotografía
        self.Vspect.configure(image=self.Gspecttk)#definiendo fuente de la imagen del lienzo
        self.Vspect.image=self.Gspecttk
        self.showst()
    def bf(self):
        self.frec.title("Frecuencia B")
        self.flagb=1
        self.flagg=0
        self.flagr=0
        #self.b,self.g,self.r=cv2.split(self.imagen)# seprando canales  bgr
        self.dtfsB=np.fft.fftshift(cv2.dft(np.float32(self.b),flags = cv2.DFT_COMPLEX_OUTPUT))#dft sobre el canal azul
        self.Bcomplex= self.dtfsB[:,:,0] + 1j* self.dtfsB[:,:,1]#valores complejos de la dft
        self.Babs=np.abs(self.Bcomplex) + 1#magnitud de los valores de la dft
        self.Bumb=20 * np.log(self.Babs)#umbralización de los valores de la dft
        self.bspec=255 * self.Bumb/ np.max(self.Bumb)#normalización de los valores entre 0 y 255
        self.bspec= self.bspec.astype(np.uint8)#conversión a uint8
        #------------------------------------------------------------------------------------------
        self.Bimgspect=Image.fromarray(self.bspec)
        self.Bspecttk = ImageTk.PhotoImage(image=self.Bimgspect)#convirtiendo la imagen a formato de fotografía
        self.Vspect.configure(image=self.Bspecttk)#definiendo fuente de la imagen del lienzo
        self.Vspect.image=self.Bspecttk
        self.showst()
    def lpf(self):
        self.filtsel=1
        self.filtopt()
    def hpf(self):
        self.filtsel=2
        self.filtopt()
    def bpf(self):
        self.filtsel=3
        self.filtopt()
    def rpf(self):
        self.filtsel=4
        self.filtopt()
    def filtopt(self):
        self.imagen=self.imagenbup
        self.b,self.g,self.r=cv2.split(self.imagen)# seprando canales  bgr
        self.rows,self.cols=self.r.shape#obteniendo tamaño de la imagen
        self.imrad=sqrt((self.rows*self.cols)/(2*pi))#radio de la imagen 
        self.dtfR=cv2.dft(np.float32(self.r),flags = cv2.DFT_COMPLEX_OUTPUT)#dft sobre el canal rojo
        self.dtfG=cv2.dft(np.float32(self.g),flags = cv2.DFT_COMPLEX_OUTPUT)#dft sobre el canal verde
        self.dtfB=cv2.dft(np.float32(self.b),flags = cv2.DFT_COMPLEX_OUTPUT)#dft sobre el canal azul
        if self.filtsel==1:
            self.filtslide()
        if self.filtsel==2:
            self.filtslide()
        if self.filtsel==3:
            self.filtslide()
        if self.filtsel==4:
            self.filtslide()  
    def filt(self,radlp):
         self.radlp=self.sigmsli.get()#obteniendo el valor del filtro del slider
         self.rads=(self.radlp/100)*(self.imrad)#calculando la equivlanecia en porcentaje del radio del filtro
         self.u=np.arange(0,self.rows) #arreglo desde 0 hasta el valor de las filas
         self.v=np.arange(0,self.cols) #arreglo desde 0 hasta el valor de las columnas
         self.idx=np.where(self.u > self.rows/2)#obteniendo valores que sean mayores a la mitad de las filas
         self.idy=np.where(self.v > self.cols/2)#obteniendo valores que sean mayores a la mitad de las columnas
         self.u[self.idx]=self.u[self.idx]-self.rows#cambiando los valores en el índice de filas
         self.v[self.idy]=self.v[self.idy]-self.cols#cambiando los valores en el índice de columnas
         self.VF,self.UF=np.meshgrid(self.v,self.u)#creando malla con los valores de filas y columnas nuevos
         self.dist=np.sqrt(self.VF*self.VF+self.UF*self.UF)#caculando las distancias entre pixeles
         if self.filtsel==1:
             self.ham2d=np.exp(-(self.dist**2)/(2*(self.rads**2)))#creando ventana de Gauss pasabajas
         if self.filtsel==2:
             self.ham2d=1-np.exp(-(self.dist**2)/(2*(self.rads**2)))#creando ventana de Gauss pasaaltas
         if self.filtsel==3:
             eps = np.finfo(float).eps
             self.central=(self.frec.get()/100)*(self.imrad)
             self.ham2d=np.exp(-(((self.dist**2)-(self.rads**2))/(self.dist*self.central+eps))**2)
         if self.filtsel==4:
             eps = np.finfo(float).eps
             self.central=(self.frec.get()/100)*(self.imrad)
             self.ham2d=1-np.exp(-(((self.dist**2)-(self.rads**2))/(self.dist*self.central+eps))**2)
         #----------------------------------------------------------------
         self.Rcomplex= self.dtfR[:,:,0] + 1j* self.dtfR[:,:,1]#valores complejos del canal rojo
         self.Rfilt=self.Rcomplex*self.ham2d#multiplicando la dft del canal rojo con la ventana
         self.Rinv=np.fft.ifft2(self.Rfilt)#realizando la idft
         self.Rback=np.abs(self.Rinv)#magnitud de los valores de la idft
         self.Rback-=self.Rback.min()
         self.Rback=self.Rback*255 / self.Rback.max()#normalizando entre 0 y 255
         self.Rback=self.Rback.astype(np.uint8)#convirtiendo a uint8
         #----------------------------------------------------------------
         self.Gcomplex= self.dtfG[:,:,0] + 1j* self.dtfG[:,:,1]#valores complejos del canal verde
         self.Gfilt=self.Gcomplex*self.ham2d#multiplicando la dft del canal verde con la ventana
         self.Ginv=np.fft.ifft2(self.Gfilt)#realizando la idft
         self.Gback=np.abs(self.Ginv)#magnitud de los valores de la idft
         self.Gback-=self.Gback.min()
         self.Gback=self.Gback*255 / self.Gback.max()#normalizando entre 0 y 255
         self.Gback=self.Gback.astype(np.uint8)#convirtiendo a uint8
         #----------------------------------------------------------------
         self.Bcomplex= self.dtfB[:,:,0] + 1j* self.dtfB[:,:,1]#valores complejos del canal azul
         self.Bfilt=self.Bcomplex*self.ham2d#multiplicando la dft del canal verde con la ventana
         self.Binv=np.fft.ifft2(self.Bfilt)#realizando la idft
         self.Bback=np.abs(self.Binv)#magnitud de los valores de la idft
         self.Bback-=self.Bback.min()
         self.Bback=self.Bback*255 / self.Bback.max()#normalizando entre 0 y 255
         self.Bback=self.Bback.astype(np.uint8)#convirtiendo a uint8
         self.imagen=cv2.merge([self.Bback,self.Gback,self.Rback])#reagrupando canales bgr
         self.showst()
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
        
        if	not	self.VS.isOpened():#si la no cámara está habilitada
            raiseValueError("Fuente de video 0", 0)
    def get_frame(self):#función para capturar los "frames" de la cámara
        if self.VS.isOpened():#si la cámara esta habilitada
            ret,frame=self.VS.read()#leyendo los "frames" de la cámara
            if self.frame1 is None:#
                frame1= cv2.flip(frame, 1)
            if ret:
                return(ret, frame,  self.frame1)
            else:
                return (ret, None)
        else:
            return (ret, None)
    def __del__(self): #definiendo el evento de destrucción de la clase
        if self.VS.isOpened():
            self.VS.release()#liberando la cámara
    
    
##############################################################################################
   #EJECUCIÓN DE LA GUI
############################################################################################## 
    
App(tk.Tk(),"Raspynstagram")

