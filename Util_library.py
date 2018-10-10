"""
* Team Id : CB#756
* Author List :[Ankur_Sonawane]
* Filename: Vrep_library.py
* Theme: Collector_bot
* Functions:  
    dist
    closest
    angle
    try_to
* classes
    HardwareError
"""
from __future__ import print_function, division

import math,cmath
from collections import defaultdict,namedtuple
import numpy as np

def dist(a, b=[0,0]):
    """
    find the eucledian distance between two points
    """
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def closest(points, source,key=lambda x:x):
    """
    Find the 'closest' point to a given source in a list of points and then Remove it 
    'closeness' is determined by applying a key function to the points to get a position'
    """
    points.sort(key=lambda x: dist(key(x), source))
    return points.pop(0)

def angle(v1,v2=(1,0)):
    """
    Find angle between two vectors in 2d space
    """
    v1=complex(*v1)
    v2=complex(*v2)
    try:
        return math.degrees(cmath.polar(v2/v1)[1])
    except ZeroDivisionError:
        return 0
def try_to(f, args=None, kwargs=None, max_try='inf', exceptions=(KeyError,ValueError), raises=True):
    """
    Try to keep doing f until you succeed or exceed the max_try 
    f fails by raising an exception which is in exceptions (if it isnt,it is raised as is)
    """
    if max_try == 'inf':
        max_try = -1
    if args is None:
        args=[]
    if kwargs is None:
        kwargs ={}
    while True:
        try:
            return f(*args, **kwargs)
        except Exception as e:
            if max_try != 0 and any(map(lambda x: isinstance(e, x), exceptions)):
                max_try -= 1
                print(isinstance(e,exceptions[0]))
            else:
                if not raises:
                    print(e)
                raise

class HardwareError(Exception):
    """
    Custom Exception raised when External Hardware fails
    """
    pass


class SoftwareError(Exception):
    """
    Custom Exception raised when External Software fails
    """
    pass
