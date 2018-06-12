# -*- coding: utf-8 -*-
"""
Created on Wed May 23 12:28:40 2018

@author: jorge
"""

import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import threading

class App(threading.Thread):
    def __init__(self, sector):
        threading.Thread.__init__(self)
        self.start()
        self.sector = sector

    def run(self):
        self.root = tkinter.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.window = self.root
        
        self.video_source =  (self.sector.get_traffic_lights()[0]).get_video_link()
        self.video_source2 =  (self.sector.get_traffic_lights()[1]).get_video_link()
        
        self.vid = cv2.VideoCapture(self.video_source)
        self.vid2 = cv2.VideoCapture(self.video_source2)
        self.canvas = tkinter.Canvas(self.root, width = self.vid.get(3), height = self.vid.get(4))
        self.canvas.grid(row = 0, column = 0)
        
        self.canvas2 = tkinter.Canvas(self.root, width = self.vid2.get(3), height = self.vid2.get(4))
        self.canvas2.grid(row = 0, column = 1)
        
        self.exitbutton = tkinter.Button(self.root, text='Quit', bg = "beige", fg="black", command = self.root.destroy, height = 5, width = int(self.vid.get(3)) // 7).grid(row = 1, column = 0)
        
        #self.btn_snapshot = tkinter.Button(window, text = "Snapshot", width=50, command=self.snapshot)
        #self.btn_snapshot.pack(anchor=tkinter.CENTER, expand= True)
        
        self.delay = 15
        self.update()
        
        self.window.mainloop()
        self.vid.release()
        self.vid2.release()
        
    
    def update(self):   
        frame = self.sector.get_traffic_lights()[0].last_image
        frame2 = self.sector.get_traffic_lights()[1].last_image
        
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        
        self.photo2 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame2))
        self.canvas2.create_image(0,0, image = self.photo2, anchor = tkinter.NW)
        
        self.window.after(self.delay, self.update)
        
    def callback(self):
        self.root.quit()

        
    def get_frame(self, video):
        if video.isOpened():
            ret, frame = video.read()
            
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return (ret, None)
        
    def snapshot(self):
        ret, frame = self.vid.get_frame()
        
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        
class VideoCapture:
    
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
            
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
    
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            
        self.window.mainloop()
        
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return (ret, None)
"""
root = tkinter.Tk()
root.withdraw()
top = tkinter.Toplevel(root)
app = App(top, "Tkinter and OpenCV", "videoplayback.mp4", "videoplayback.mp4", root)

"""