# -*- coding: utf-8 -*-
"""
Created on Sun May  6 18:46:08 2018

@author: bermu

"""

from darkflow.net.build import TFNet
from moviepy.editor import VideoFileClip
from Model import Traffic_light, Sector
from queue import Queue 
import numpy as np
import threading 
import subprocess
import time
import cv2
from VideoCapture import App, VideoCapture

black_pixel = np.array([0,0,0])
config = {
    'model': 'cfg/tiny-yolo.cfg',
    'load': 'bin/yolov2-tiny.weights', 
    'threshold': 0.4,
    'gpu': 1.0
}

def getCenterSquare(result):
    mid = [0,0]
    mid[0] = (int(result['topleft']['x'])+ int(result['bottomright']['x'])) / 2;
    mid[1] = (int(result['topleft']['y'])+ int(result['bottomright']['y'])) / 2;
    return mid
tfnet = TFNet(config)


def getLength(filename):
  result = subprocess.Popen(["ffprobe", filename],
    stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
  return [x for x in result.stdout.readlines() if "Duration" in x]

def using_video(worker, tf):    
    capture = cv2.VideoCapture(tf.video_link)
    colors = [tuple(254 * np.random.rand(3)) for i in range(5)]
    frames= 0 
    frame1 = tf.get_last_image()
    prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[...,1] = 255
    total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    car_list = [] 
    moving_list = [] 
    processed_frames = 0 
    noFrame = tf.get_last_sec()
    success = capture.set(cv2.CAP_PROP_POS_FRAMES, noFrame)
    while (capture.isOpened()):
        frames+=1
        if (frames%15!=0):
            capture.read()
            pass
        if (processed_frames == 20):
            break
        elif(frames%15==0): 
            processed_frames += 1
            ret, frame = capture.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            next = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
            
            flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            
            mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
            hsv[...,0] = ang*180/np.pi/2
            hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
            rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR) # este es el frame final que tiene el calculo del optical flow en colores
            #ret, rgb = cv2.threshold(rgb, 10, 255, cv2.THRESH_BINARY) da problemas

            if ret:
                

                results = tfnet.return_predict(frame)
                cars = 0 
                cars_moving = 0 
                
                #print(results)
                for color, result in zip(colors, results):
                    if(result['label'] == 'car'): 
                        cars += 1 
                        mid = getCenterSquare(result)
                        pixel = rgb[int(mid[1]), int(mid[0])]
                        #print("pixel:" + str(pixel))
                        if(pixel.any()!=black_pixel.any()):
                            #print("car mooooving  quak")
                            cars_moving += 1  
                        else:
                            #print(str(color))
                            color = (255,255,255)
                        tl = (result['topleft']['x'], result['topleft']['y'])
                        br = (result['bottomright']['x'], result['bottomright']['y'])
                        label = result['label']
                        frame = cv2.rectangle(frame, tl, br, color, 7)
                        frame = cv2.putText(frame, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)    
                car_list.append(cars)
                moving_list.append(cars_moving) 
                tf.set_last_image(frame)
                with print_lock:    
                    print("|| cars: " + str(cars) + "|| video: " + tf.video_link + " || frame_no: " + str(noFrame+frames))
                    print(threading.current_thread().name, worker)
                #cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
            else:
                capture.release()
                cv2.destroyAllWindows()
                break
    #principal modificacion 
    tf.current_value = car_list
    tf.set_last_sec(noFrame + 20*15)
    print("using_video car list:" + str(car_list))
    print("using_video mov list:" + str(moving_list))
    return car_list
            


    
def threader(tf): 
    while True: 
        worker = q.get()
        print(using_video(worker, tf))
        print("no se cuando termina")
        q.task_done()
        
def start(sector):
    global app 
    until = sector.get_min_time()
    sec = 0 
    while(until > sec): 
        start = time.time() 
        for worker in range(len(sector.get_traffic_lights())): 
            q.put(worker)
        q.join()
        sec += 20
        print("time: " , time.time()-start)
        time.sleep(2)
        tf_win = sector.get_more_cars()
        sector.append_sequence(tf_win)
        print("winner traffic light: " + str(tf_win))
        if(sector.traffic_lights[tf_win].state == 0):
            print("was red, changing")
            sector.traffic_lights[tf_win].state = 2    
            sector.set_others_red(tf_win)
            time.sleep(8)
        print("the whole state:" + sector.view_state())
    for x in range(len(sector.get_traffic_lights())): 
        print(sector.get_traffic_lights()[x].current_value)
        

print_lock = threading.Lock()       
  
q = Queue() 

videos = ['videoplayback.mp4', 'videofile.avi']   
tf1 = Traffic_light("Tf1 norte-sur", 100, 100, videos[0], 0, [])
tf2 = Traffic_light("Tf2 este-oeste", 0, 0, videos[1], 2, [])
#sector = Sector("Barrio Amon - TEC", [tf1, tf2], [1])
sector = Sector("Desconocido", [tf1, tf2], [1])
app = App(sector)
for x in range(2): 
    tf = sector.get_traffic_lights()[x]
    t = threading.Thread(target = threader,  args = (tf,))
    t.daemon = True 
    t.start() 


start(sector) 


"""
#example_video()  
##using_camera()
#using_video()
##start()

imgcv = cv2.imread("2.jpg")
result = tfnet.return_predict(imgcv)
print(result)
print("quak")
imgcv = cv2.imread("1.jpg")
result = tfnet.return_predict(imgcv)
print(result)


def example_video():    
    capture = cv2.VideoCapture('videoplayback.mp4')
    colors = [tuple(255 * np.random.rand(3)) for i in range(5)]
    frames= 0 
    while (capture.isOpened()):
        frames+=1
        if frames%29!=0:
            capture.read()
            pass
        else: 
            
            ret, frame = capture.read()
            if ret:
                results = tfnet.return_predict(frame)
                cars = 0 
                print(results)
                for color, result in zip(colors, results):
                    if(result['label'] == 'car'): 
                        cars += 1 
                    tl = (result['topleft']['x'], result['topleft']['y'])
                    br = (result['bottomright']['x'], result['bottomright']['y'])
                    label = result['label']
                    frame = cv2.rectangle(frame, tl, br, color, 7)
                    frame = cv2.putText(frame, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)    
                print( " || cars: " + str(cars))
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
            else:
                capture.release()
                cv2.destroyAllWindows()
                break
            



def using_camera():  
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
    
    colors = [tuple(255 * np.random.rand(3)) for i in range(10)]

    frames=0
    while(1):
        frames+=1
        if frames%3!=0:
            pass
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
                frame = cv2.putText(frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2)
                ## aqui puede ser que en vez de mostrar los cuadros se mande esa info a analizar
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
    
        else:
            cam.release()
            cv2.destroyAllWindows()
            break
        



"""