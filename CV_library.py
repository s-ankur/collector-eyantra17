"""
* Team Id : CB#756
* Author List :[Ankur_Sonawane,Pratik_Kale]
* Filename: task4.py
* Theme: Collector_bot
* Classes:
    Video
        read
        set_roi
"""
from __future__ import print_function, division
from Matutils_library import *
import cv2

class Video:
    bbox = None
    
    def __init__(self, video, show = False,save=None,resolution =[1280,720]):
        try:
            print("Starting VideoCapture")
            self.input_video = cv2.VideoCapture(video)
            print("VideoCapture Started")
        except:
            raise HardwareError("Video Not Connected")

        self.save = save
        self.show = show

        if resolution is not None or isinstance(video,str):
            self.input_video.set(3,resolution[0])
            self.input_video.set(4,resolution[1])
        
        if self.save is not None:
            self.save_video = cv2.VideoWriter(save, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))
            print("Saving VideoFile: "  +save)
        self.input_video.grab()

    def set_roi(self,bbox=None):
        print("Setting ROI")
        if bbox is None:
            _,img=self.input_video.read()
            img,bbox=imcrop(img)
        self.bbox=bbox
        print("Roi set as",bbox )

    def read(self):
        ret, img = self.input_video.read()
        if self.show:
            imshow(img,window_name='video',hold=True)
        if not ret:
            raise HardwareError("Camera Wire Pulled")
        if self.bbox is not None:
            img,bbox=imcrop(img,bbox=self.bbox)
        if self.save is not None:
            self.save_video.write(img)
        return img

    def __del__(self):
        self.input_video.release()
        print("Video Capture Released")
        if self.save is not None:
            self.save_video.release()
            print("VideoFile Saved")
        if self.show:
            destroy_window('video')


#class Video(Video):
    """
    Dummy Video
    """
    #def __init__(self,*args):
        #print("Dummy Video")
        #super().__init__('input_video.avi')
    


