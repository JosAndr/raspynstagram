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
        self.imagen=0
        self.faceflag=0
        self.colorflag=0
        self.contrflag=0
        self.invflag=0
        self.grayflag=0
        self.bwflag=0
        self.smoothflag=0
        self.cartoonflag=0
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
        self.deteccion.add_command(label="Detección Facial: NO",command=self.faceon)
        self.deteccion.add_command(label="Detección de Color: NO",command=self.coloron)
        #Creando menú de mejoramiento
        self.ajustes=Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Mejoramiento", menu=self.ajustes)
        self.ajustes.add_command(label="Contraste",command=self.contraste)
        self.ajustes.add_command(label="Suavizar",command=self.smooth)
        #Menu de color
        self.color=Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label="Color", menu=self.color)
        self.color.add_command(label="Invertir Color",command=self.inv)
        self.color.add_command(label="Escala de Grises",command=self.gray)
        self.color.add_command(label="Blanco y negro",command=self.bw)
        self.color.add_command(label="Caricatura",command=self.cartoon_on)
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
        time.sleep(2.0)
        self.actualizar()
        self.mainwin.mainloop()
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
        self.sigsli=tk.Scale(self.suavizar,from_=1, to=15, cursor="arrow", orient=HORIZONTAL,showvalue=YES, variable=self.smth,length=300,command=self.suaval)
        self.sigsli.set(1)
        self.sigsli.pack(side="bottom",fill="x",expand="yes",padx=4, pady=6)
        self.suavizar.protocol("WM_DELETE_WINDOW", self.closesuav)
##############################################################################################
   #FUNCIÓN PARA CERRAR VENTANA DE SUAVIZADO
##############################################################################################        
    def closesuav(self):
        self.smoothflag=0
        self.suavizar.destroy()        
#********************************************************************************************
#############################################################################################
    #CALLBACKS Y FUCIONES
#############################################################################################
#********************************************************************************************
        
#############################################################################################
    #DETECCIÖN FACIAL
#############################################################################################   
    def detc_facial(self):
        self.face_det=cv2.CascadeClassifier('/usr/share/opencv/lbpcascades/lbpcascade_frontalface.xml')#clasificador pre-entrenado de reconcoimeinto facial
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
            cv2.rectangle(self.imagen,(x,y),(x+w,y+h),(255,255,255),2) #definiendo rectángulo para las ROI
            self.roi_color = self.imagen[y:y+h, x:x+w] #dibujando ROI sobre la imagen BGR
#############################################################################################
    #FUNCION PARA ACTIVAR/DESACTIVAR DETECCIÖN FACIAL
#############################################################################################              
    def faceon(self):
        if self.faceflag==0:
            self.faceflag=1
            self.deteccion.entryconfig(0,label="Detección Facial: SI")
        elif self.faceflag==1:
            self.faceflag=0
            self.deteccion.entryconfig(0,label="Detección Facial: NO")
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
    #FUNCION PARA ACTIVAR/DESACTIVAR DETECCIÖN FACIAL
#############################################################################################              
    def coloron(self):
        if self.colorflag==0:
            self.colorflag=1
            self.deteccion.entryconfig(1,label="Detección de Color: SI")
        elif self.colorflag==1:
            self.colorflag=0
            self.deteccion.entryconfig(1,label="Detección de Color: NO")                
##############################################################################################
  #FUNCIÓN DE ACTUALIZACIÓN
##############################################################################################        
    def actualizar(self):
        ret,frame, frame1=self.VS.get_frame() #llamando la función de obtención de imagen
        self.imagen=cv2.flip(frame, 1)#invirtiendo para que la imagen coincida con la imagen real
        if ret:#si hay "frames" capturados
            if self.faceflag==1:
                self.detc_facial()
                #..............................................................
            if self.colorflag==1:
                self.detc_color()
                #..............................................................
            if self.contrflag==1:
                self.conts(1)
                #..............................................................
            if  self.smoothflag==1:
                self.suaval(1)
                #.............................................................
            if self.invflag==1:
                self.imagen=cv2.bitwise_not(self.imagen)
                #.............................................................
            if self.grayflag==1:
                self.imagen=cv2.cvtColor(self.imagen,cv2.COLOR_BGR2GRAY)
                #.............................................................
            if self.bwflag==1:
                self.grisesc=cv2.cvtColor(self.imagen,cv2.COLOR_BGR2GRAY).astype('uint8')
                self.imagen = cv2.adaptiveThreshold(self.grisesc,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
                #........................................................................................................
            if self.cartoonflag==1:
                self.cartoon()
            self.cv2image = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2RGBA)#convirtiendo de BGR a RGB   
            self.img = Image.fromarray(self.cv2image)#convirtiendo matriz a imagen
            self.imgtk = ImageTk.PhotoImage(image=self.img)#convirtiendo la imagen a formato de fotografía
            self.lmain.configure(image=self.imgtk)#definiendo fuente de la imagen del lienzo
            self.lmain.image=self.imgtk#mostrando la imagen en el lienzo

        if self.run==0:#modo por defecto:visualización de video
            self.lmain.after(1,self.actualizar)#reiniciando la función despues de 1 ms
            
        if self.run==1:#modo forzado:imagen estática
            pass
           
##############################################################################################
   #FUNCIONES PARA EL CAMBIO DE MODO ACTUALIZACIÓN
##############################################################################################   
    def capture(self):#Modo estático/tomar fotografía
      self.run=1 #cambiando el valor de la bandera
    def reint(self):#Modo video
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
##############################################################################################
   #FUNCIÓN PARA AJUSTAR EL CONTRASTE
##############################################################################################     
    def conts(self,gamma):
        self.gamma=self.slider.get()
        self.invgamma=1/self.gamma
        self.table=np.array([((self.i / 255.0) ** self.invgamma) * 255
		for self.i in np.arange(0, 256)]).astype("uint8")
        self.imagen=cv2.LUT(self.imagen,self.table)
##############################################################################################
   #FUNCIÓN PARA SUAVIZAR
##############################################################################################     
    def suaval(self,sigma):
        self.scolor=self.imagen
        self.iter=self.sigsli.get()
        for _ in range(self.iter):
            self.scolor=cv2.bilateralFilter(self.scolor,3,3,1)
        self.imagen=self.scolor
##############################################################################################
   #INVERTIR COLOR
##############################################################################################     
    def inv(self):
        if self.invflag==0:
            self.invflag=1
        elif self.invflag==1:
            self.invflag=0
##############################################################################################
  #ESCALA DE GRISES
##############################################################################################     
    def gray(self):
        if self.grayflag==0:
            self.grayflag=1
        elif self.grayflag==1:
            self.grayflag=0
##############################################################################################
  #B&W
##############################################################################################     
    def bw(self):
        if self.bwflag==0:
            self.bwflag=1
        elif self.bwflag==1:
            self.bwflag=0
##############################################################################################
  #CARICATURA
##############################################################################################     
    def cartoon(self):
       self.color=self.imagen
       self.down=2
       self.bildif=7
       for _ in range(self.down):
           self.color=cv2.pyrDown(self.color)
       for _ in range(self.bildif):
           self.color=cv2.bilateralFilter(self.color,5,5,3)
       for _ in range(self.down):
           self.color=cv2.pyrUp(self.color)   
       self.graysc=cv2.cvtColor(self.imagen, cv2.COLOR_BGR2GRAY)
       self.dif=cv2.medianBlur(self.graysc, 7)
       self.bordes=cv2.adaptiveThreshold(self.dif,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,blockSize=9,C=2)
       self.bordes=cv2.cvtColor(self.bordes, cv2.COLOR_GRAY2BGR)
       self.imagen=cv2.bitwise_and(self.color, self.bordes)
##############################################################################################
  #HABILITANDO CARICATURA
##############################################################################################     
    def cartoon_on(self):
       if self.cartoonflag==0:
            self.cartoonflag=1
       elif self.cartoonflag==1:
           self.cartoonflag=0
               
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

