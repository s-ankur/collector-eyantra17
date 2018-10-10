"""
* Team Id : CB#756
* Author List :[Ankur_Sonawane,Pratik_Kale]
* Filename: Vrep_library.py
* Theme: Collector_bot
* Classes: 
    Vrep
        init_models
        update_models
        get_handle
        get_position
        get_path
        filter_path
        set_angle
        set_position
        call_function
"""

from __future__ import division,print_function
import math,sys
from collections import namedtuple
import numpy as np
import vrep
from Util_library import *


class Vrep:
    """
    A Simplified Interface to the Vrep Remote APi
    """
    Model=namedtuple('Model',['handle','z'])   
    models={}    
    model_names=['Path',
                 'TRUCK',
                 'CB',
                 "Corner1",
                 "Corner2",
                 "FreshFruit1",
                 "FreshFruit2",
                 "FreshFruit3",
                 "FreshFruit4",
                 "DamagedFruit1",
                 "DamagedFruit2",
                 "DamagedFruit3",
                 "DamagedFruit4",
                 'Goal']
    emptyBuff = bytearray()
    
    def __init__(self):
        print("Connecting to Vrep")
        vrep.simxFinish(-1)
        self.clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
        if self.clientID==-1:
            raise SoftwareError("Vrep not On")
        else:
            print ('Vrep connection successful')

    def init_models(self):
        for model_name in self.model_names:
            handle=self.get_handle(model_name)
            if handle and not self.models.get(model_name,None):
                print("Model "+model_name+" initialized")
                self.models[model_name]=Vrep.Model(handle=handle,z=self.get_position(handle)[2])
            else:
                print("Model "+model_name+" does not exist in Vrep")

    def update_models(self,model_dict):
        for model_name,(pos,vec) in model_dict.items():
            self.set_position(model_name,*pos)
            self.set_angle(model_name,angle(vec))


    def get_path(self,num_points=4):
        path=[]
        try:
            self.call_function('update_path')
            for i in range( 1,num_points+1):
                pos_on_path=i/ num_points
                _,_,floats,_,_=self.call_function('get_path_pos',floats=[pos_on_path])
                x,y=floats[:2]
                path.append(np.array([x,2-y]))            
        except:
            pass
        return path

    def filter_path(self,path,error=12):
        updated_path=[]
        for i in range(1,len(path)-1):
            m1 = angle(path[i],path[i-1])
            m2 = angle(path[i+1],path[i])
            if m1-m2 > error:
                updated_path.append(path[i])
        updated_path.append(path[-1])
        return updated_path

    def relative_path_pos(self,path_pos):
        return self.call_function('relative_path_pos',floats=[path_pos])[2][:2]

    def get_handle(self,name):
        return vrep.simxGetObjectHandle(self.clientID,name,vrep.simx_opmode_oneshot_wait)[1]

    def get_position(self,handle):
        return vrep.simxGetObjectPosition(self.clientID, handle, -1, vrep.simx_opmode_oneshot_wait)[1]

    def set_position(self,name,x,y):
        try:
            vrep.simxSetObjectPosition(self.clientID, self.models[name].handle, -1, (x,2-y,self.models[name].z) ,vrep.simx_opmode_oneshot_wait)
        except KeyError:
            print("Could not set Poistion for ",name)    

    def set_angle(self,name,phi):
        try:
            vrep.simxSetObjectOrientation(self.clientID,  self.models[name].handle,-1, [0,0,math.radians(phi)],vrep.simx_opmode_oneshot_wait)      
        except KeyError:
            print("Could not set Poistion for ",name) 

    def call_function(self,function_name,ints=[],floats=[],strings=[]):
        return vrep.simxCallScriptFunction(self.clientID,'LuaFunctions',vrep.sim_scripttype_childscript,function_name,ints,floats,strings,self.emptyBuff,vrep.simx_opmode_oneshot_wait)

    def s__del__(self):
        print("Vrep Simulation Stopped")
        vrep.simxStopSimulation(self.clientID,vrep.simx_opmode_oneshot_wait)

if __name__ =='__main__':
    import time,random
    v=Vrep()
    v.init_models()

