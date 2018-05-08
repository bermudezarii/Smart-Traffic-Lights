# -*- coding: utf-8 -*-
"""
Created on Sun May  6 18:46:08 2018

@author: bermu

 'threshold': 0.3,
    'gpu': 1.0

"""

from darkflow.net.build import TFNet
from queue import Queue 
import numpy as np
import threading 
import time
import cv2
#'threshold': 0.35,
config = {
    'model': 'cfg/tiny-yolo.cfg',
    'load': 'bin/yolov2-tiny.weights', 
    'threshold': 0.4,
    'gpu': 1.0
}

tfnet = TFNet(config)

def using_camera():  
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
    
    colors = [tuple(255 * np.random.rand(3)) for i in range(10)]
    print(colors)
    c=0
    while(1):
        c+=1
        if c%3!=0:
            pass
    
        stime = time.time()
        ret, frame = cam.read()
    
        results = tfnet.return_predict(frame)
    
        if ret:
            for color, result in zip(colors, results):
                tl = (result['topleft']['x'], result['topleft']['y'])
                br = (result['bottomright']['x'], result['bottomright']['y'])
    
                label = result['label']
                confidence = result['confidence']
                text = '{}: {:0f}%'.format(label, confidence * 100)
                frame = cv2.rectangle(frame, tl, br, color, 5)
                ##frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.putText(frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2)
                ## aqui puede ser que en vez de mostrar los cuadros se mande esa info a analizar
                print(result)
                print(stime)
            cv2.imshow('frame', frame)
            ##print('FPS {:.0f}%'.format(1/(time.time()-stime)))
    
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
    
        else:
            cam.release()
            cv2.destroyAllWindows()
            break
        
def using_video():    
    capture = cv2.VideoCapture('videoplayback.mp4')
    colors = [tuple(255 * np.random.rand(3)) for i in range(5)]
    cars = 0 
    frames= 0 
    while (capture.isOpened()):
        frames+=1
        if frames%29!=0:
            capture.read()
            pass
        else: 
            stime = time.time()
            ret, frame = capture.read()
            if ret:
                #print(frame.shape)
                results = tfnet.return_predict(frame)
                
                print(results)
                for color, result in zip(colors, results):
                    if(result['label'] == 'car'): 
                        cars += 1 
                    tl = (result['topleft']['x'], result['topleft']['y'])
                    br = (result['bottomright']['x'], result['bottomright']['y'])
                    label = result['label']
                    #print(label,'shape',br[0]-tl[0],br[1]-tl[1])
                    #print(stime)
                    # if (label == 'bus'):
                    #frame = cv2.rectangle(frame, tl, br, color, 7)
                    #frame = cv2.putText(frame, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
                    
                print("cars: " + str(cars))
                #cv2.imshow('frame', frame)
                #print('FPS {:.1f}'.format(1 / (time.time() - stime)))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
            else:
                capture.release()
                cv2.destroyAllWindows()
                break
            

print_lock = threading.Lock()


        

def threader():
    while True: 
        worker = q.get()
        using_video(worker)
        q.task_done()
        
        
def start(): 
    q = Queue() 
    for x in range(1): 
        t = threading.Thread(target = threader) ## para params poner args(i , ) f.e
        t.daemon = True 
        t.start()
    
    start = time.time()
    for worker in range(1): 
        q.put(worker)
    
    q.join()
    print("time: " , time.time()-start)

##using_camera()
using_video()
"""
imgcv = cv2.imread("2.jpg")
result = tfnet.return_predict(imgcv)
print(result)
print("quak")
imgcv = cv2.imread("1.jpg")
result = tfnet.return_predict(imgcv)
print(result)
"""