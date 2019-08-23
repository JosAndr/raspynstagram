import numpy
import PIL
from tkinter import *
from PIL import ImageTk,Image 
from tkinter import ttk
import cv2
#Creando ventana principal
mainwin=Tk()
mainwin.geometry("711x528+100+100")
mainwin.title('Raspynstagram')
mainwin.resizable(0,0)
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
visor=Canvas(mainwin,width=460,height=460)
visor.place(x=21, y=29)
imorig=cv2.cvtColor(cv2.imread("VLA.jpg"),cv2.COLOR_BGR2RGB)
resim=cv2.resize(imorig,(460,460))
dispim= PIL.ImageTk.PhotoImage(PIL.Image.fromarray(resim))
visor.create_image(0,0, anchor=NW, image=dispim)
#Creando Lienzo adicional
visor2=Canvas(mainwin,width=200,height=200)
visor2.place(x=501, y=29)
imorig2=cv2.cvtColor(cv2.imread("VLA.jpg"),cv2.COLOR_BGR2GRAY)
resim2=cv2.resize(imorig2,(200,200))
dispim2= PIL.ImageTk.PhotoImage(PIL.Image.fromarray(resim2))
visor2.create_image(0,0, anchor=NW, image=dispim2)

mainwin.mainloop()
