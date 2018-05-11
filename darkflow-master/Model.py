# -*- coding: utf-8 -*-
"""

@author: bermu
"""
from moviepy.editor import VideoFileClip


class Traffic_light: 
    def __init__(self, name, x_gps=0, y_gps=0, link='', stat=0, current_val=[]):
        self.name = name 
        self.gps_cords = [x_gps, y_gps]
        self.video_link = link 
        self.state = stat 
        self.current_value = current_val
        self.last_sec = 0 

    def get_name(self):
        return self.name 

    def get_gps_cords(self):
        return self.gps_cords
    
    def get_video_link(self): 
        return self.video_link 
    
    def get_state(self):
        return self.state
    
    def get_current_value(self):
        return self.current_value 
    
    def get_last_sec(self): 
        return self.last_sec
    
    def set_name(self, name):
        self.name = name

    def set_gps_cords(self, x, y):
        self.gps_cords = [x,y]
    
    def set_video_link(self, link): 
        self.video_link = link
    
    def set_state(self, state):
        self.state = state
    
    def set_current_value(self, val):
        self.current_value = val
    
    def set_last_sec(self, sec):
        self.last_sec = sec
    
class Sector: 
    def __init__(self, name, tf=[], seq=[]):
        self.name = name 
        self.traffic_lights = tf 
        self.sequence = seq
      
    def get_name(self):
        return self.name 
    
    def get_traffic_lights(self): 
        return self.traffic_lights
    
    def get_sequence(self): 
        return self.sequence 
    
    def set_name(self,name):
        self.name = name
        
    def set_traffic_lights(self, tf):
        self.traffic_lights = tf
        
    def set_sequence(self, sequence):
        self.sequence = sequence
        
    def get_min_time(self): 
        mini_time = 0
        times = []
        for x in range(len(self.traffic_lights)): 
            clip = VideoFileClip(self.traffic_lights[x].video_link)
            times.append(clip.duration)
            clip.reader.close()
            clip.audio.reader.close_proc()
        mini_time = min(times)
        return mini_time
    
    def get_more_cars(self): 
        results = []
        for x in range(len(self.traffic_lights)):
            tf_results = self.traffic_lights[x].current_value
            results.append(sum(tf_results))
        return results.index(max(results))
            
    def set_others_red(self, tf_win):
        for x in range(len(self.traffic_lights)):
            tf = self.traffic_lights[x] 
            if(tf != tf_win): 
                self.traffic_lights[x].state = 0
    
    def view_state(self): 
        string = ""
        for x in range(len(self.traffic_lights)):
            string += "name of tf: "+ self.traffic_lights[x].name + "  ** state: ** " + str(self.traffic_lights[x].state) + "\n"
        return string 
            
            