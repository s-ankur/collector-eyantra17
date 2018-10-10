
from __future__ import print_function, division
from CV_library import *
import cv2.aruco as aruco

"""
* Team Id : CB#756
* Author List :[Ankur_Sonawane]
* Filename: task4.py
* Theme: Collector_bot
* Classes:
    ArucoVideo
        get_markers

"""

class ArucoVideo(Video):
    id_to_name={
        0:'CB',
        1:'TRUCK',
        2:'FreshFruit1',
        3:'FreshFruit2',
        4:'FreshFruit3',
        5:'FreshFruit4',
        6:'DamagedFruit1',
        7:'DamagedFruit2',
        8:'DamagedFruit3',
        9:'DamagedFruit4',
        10:'Corner1',
        11:'Corner2'}

    Marker=namedtuple('Marker',['pos','vec'])
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
    parameters = aruco.DetectorParameters_create()        
    arena_size=[1,2.5] # meters
    callback=None

    def get_markers(self,):
        aruco_markers = {}
        for i in range(5):
            img=self.read()
            scaling_factor=img.shape[1]/self.arena_size[1]
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            corners, ids, _ = aruco.detectMarkers(gray, dictionary=self.aruco_dict, parameters=self.parameters)    
            for index,value in enumerate(corners):
                v=value[0]
                if self.bbox is not None:
                    v=v/scaling_factor
                center = np.average(v,0)
                line_end=np.average(v[:2,:],0);
                vector=100*(center-line_end)
                aruco_markers[self.id_to_name.get(ids.item(index))] = ArucoVideo.Marker(center,-vector)   
        aruco_markers.pop(None,None) #delete error marker
        if self.callback is not None:
            self.callback(aruco_markers)
        return aruco_markers

    def find_marker(self,marker_name,):
        print("Finding ",marker_name)
        marker=None
        while not marker:
            marker=self.get_markers().get(marker_name)
        return marker


if __name__ =="__main__":
    v=ArucoVideo(0)    
    #v.set_roi()
    #test_markers()
    #v.find_marker('TRUCK')
