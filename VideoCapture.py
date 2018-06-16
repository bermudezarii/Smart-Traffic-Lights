# -*- coding: utf-8 -*-
"""
Created on Wed May 23 12:28:40 2018

@author: jorge
"""

import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
from random import randrange, randint #Solo para pruebas, se puede quitar despues (Testing)

class App:
    def __init__(self, window, window_title, video_source=0, video_source2=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.video_source2 = video_source2
        
        self.vid = cv2.VideoCapture(video_source)
        self.vid2 = cv2.VideoCapture(video_source2)
        ########################## Cambios que realice (solo toque posiciones) ##################################
        self.canvas = tkinter.Canvas(window, width = self.vid.get(3), height = self.vid.get(4))
        self.canvas.grid(row = 3, column = 0)
        
        self.canvas2 = tkinter.Canvas(window, width = self.vid2.get(3), height = self.vid2.get(4))
        self.canvas2.grid(row = 3, column = 1)
        
        self.exitbutton = tkinter.Button(window, text='Quit', bg = "beige", fg="black", command = root.destroy, height = 5, width = int(self.vid.get(3)) // 7).grid(row = 0, column = 0)
        
        #Informacion necesaria, pero no se modifica
        tkinter.Label(window, text = "Number of vehicles: ").grid(row = 1, column = 0, sticky = tkinter.W)
        tkinter.Label(window, text = "Number of vehicles: ").grid(row = 1, column = 1, sticky = tkinter.W)
        
        tkinter.Label(window, text = "Vehicles in motion: ").grid(row = 2, column = 0, sticky = tkinter.W)
        tkinter.Label(window, text = "Vehicles in motion: ").grid(row = 2, column = 1, sticky = tkinter.W)
        
        tkinter.Label(window, text = "Semaphore status: ").place(x = 170, y = 95)
        tkinter.Label(window, text = "Semaphore status: ").place(x = self.vid.get(3) + 170, y = 95)
        
        #Informacion que se modifica constantemente con las funciones
        
        #Cantidad total de vehiculos
        self.total_vehicles_1 = tkinter.Label(window, text = "")
        self.total_vehicles_1.place(x = 110, y = 86)
        
        self.total_vehicles_2 = tkinter.Label(window, text = "")
        self.total_vehicles_2.place(x = self.vid.get(3) + 118, y = 86)
        
        #Total de vehiculos en movimiento        
        self.motion_vehicles_1 = tkinter.Label(window, text = "")
        self.motion_vehicles_1.place(x = 110, y = 107)
        
        self.motion_vehicles_2 = tkinter.Label(window, text = "")
        self.motion_vehicles_2.place(x = self.vid.get(3) + 118, y = 107)
        
        #Estados de los semaforos
        self.status_semaphore_1 = tkinter.Label(window, width = 2)
        self.status_semaphore_1.place(x = 275, y = 95)
        
        self.status_semaphore_2 = tkinter.Label(window, width = 2)
        self.status_semaphore_2.place(x = self.vid.get(3) + 275, y = 95)
        
        ########################## Termina Cambios que realice ###################################3
        self.delay = 15
        self.delay2 = 2000 #Este delay es solo para pruebas (Testing)
        self.update()
        
        #Solo para realizar pruebas (Testing)
        self.test_set_total_vehicles()
        self.test_set_motion_vehicles()
        self.test_set_status_semaphore()
        
        
        self.window.mainloop()
        self.vid.release()
        self.vid2.release()
        
    
    def update(self):
        ret, frame = self.get_frame(self.vid)
        ret2, frame2 = self.get_frame(self.vid2)
        if ret and ret2:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
            
            self.photo2 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame2))
            self.canvas2.create_image(0,0, image = self.photo2, anchor = tkinter.NW)
        
        self.window.after(self.delay, self.update)
    
    
    ############################# Nuevos metodos #############################################
    
    #Metodos para realizar pruebas (No se deben usar en la progra)(Testing)
    def test_set_total_vehicles(self):
        self.total_vehicles_1.config(text = randrange(10, 20))
        self.total_vehicles_2.config(text = randrange(10, 20))
        self.window.after(self.delay2, self.test_set_total_vehicles)

    def test_set_motion_vehicles(self):
        self.motion_vehicles_1.config(text = randrange(10))
        self.motion_vehicles_2.config(text = randrange(10))
        self.window.after(self.delay2, self.test_set_motion_vehicles)
        
    def test_set_status_semaphore(self):
        winner = randint(0,1)
        if(winner == 0):
            self.status_semaphore_1.config(bg = "green")
            self.status_semaphore_2.config(bg = "red")
            
        else:
            self.status_semaphore_1.config(bg = "red")
            self.status_semaphore_2.config(bg = "green")
            
        self.window.after(self.delay2, self.test_set_status_semaphore)
        
    #Metodos que se deben usar
    
    #Funcion para modificar cantidad total de vehiculos
    def set_total_vehicles(self, total_1, total_2):
        self.total_vehicles_1.config(text = total_1)
        self.total_vehicles_2.config(text = total_2)
    
    #Funcion para modificar cantidad de vehiculos en movimiento
    def set_motion_vehicles(self, total_motion_1, total_motion_2):
        self.motion_vehicles_1.config(text = total_motion_1)
        self.motion_vehicles_2.config(text = total_motion_2)
    
    #Funcion para modificar estados de los semaforos
    def set_status_semaphore(self, winner):
        if(winner == 0):
            self.status_semaphore_1.config(bg = "green")
            self.status_semaphore_2.config(bg = "red")
            
        else:
            self.status_semaphore_1.config(bg = "red")
            self.status_semaphore_2.config(bg = "green")
    
    ############################# Terminan nuevos metodos #############################################
        
    def get_frame(self, video):
        if video.isOpened():
            ret, frame = video.read()
            
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return (ret, None)
        

    
root = tkinter.Tk()
root.withdraw()
top = tkinter.Toplevel(root)
App(top, "Tkinter and OpenCV", "videoplayback.mp4", "videoplayback.mp4")
