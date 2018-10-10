"""
* Team Id : CB#756
* Author List :[Ankur_Sonawane]
* Filename: Matutils_library.py
* Theme: Collector_bot
* Functions: 
    imread
    imwrite
    destroy_window
    imshow
    imtool
    imcrop
    imdilate
    imerode
    imopen
    imclose
    centroid
    polylines
    rectangle
    Color
        threshold
    find_shapes
    
"""
from Util_library import *
import cv2
from warnings import warn

_imread_modes={
    'color':cv2.IMREAD_COLOR,
    'gray':cv2.IMREAD_GRAYSCALE,
    }

def imread(img_name,mode='color'):
    img=cv2.imread(img_name,_imread_modes[mode])
    if img is None:
        raise IOError(img_name)
    return img

imwrite=cv2.imwrite

def destroy_window(*args,**kwargs):
    cv2.destroyWindow(*args,**kwargs)
    cv2.waitKey(1)
    cv2.waitKey(1)
    cv2.waitKey(1)
    cv2.waitKey(1)      
    
def imshow(img,window_name='image',hold=False,):
    if not hold:
        cv2.namedWindow( window_name )
    # if img.shape[0]>700:
    #     warn("Image size too large, resizing to fit")
    #     img = cv2.resize(img, (0,0), fx=700/img.shape[0], fy=700/img.shape[0])  
    # if img.shape[1]>700:
    #     warn("Image size too large, resizing to fit")        
    #     img = cv2.resize(img, (0,0), fx=700/img.shape[1], fy=700/img.shape[1])     
    cv2.imshow(window_name,img)
    key = cv2.waitKey(int(hold)) & 0xFF 
    if not hold:
        destroy_window(window_name)
    return chr(key)

class imtool:
    """
    MATLAB like imtool with very limited functionality
    Show color values and position at a given point in an image, interactively
    some problems when resizing
    """
    def __init__(self,img):
        self.img=img
        self.pos=(0,0)
        cv2.namedWindow( 'imtool' )
        cv2.setMouseCallback('imtool', self.on_click)    
        font=cv2.FONT_HERSHEY_SIMPLEX
        while True:
            img=np.zeros_like(self.img)
            x,y=self.pos
            cols=self.img[y,x]
            text="%d %d: "%(y,x)+str(cols)
            cv2.putText(img,text,self.pos,font,.5, 255)
            key = imshow(cv2.bitwise_xor(img,self.img),window_name='imtool',hold=True)
            if key == 'q':
                break
            try:
                cv2.getWindowProperty('imtool', 0)
            except cv2.error:
                break   
        destroy_window('imtool')
        
    def on_click(self, event, x, y, flags, param):           
        self.pos=(x,y)

        
class imcrop:
    """
    MATLAB-like imcrop utility
    Drag mouse over area to select
    Lift to complete selection
    Doubleclick or close window to finish choosing the crop
    Rightclick to retry
    
    Example:
        >>> cropped_img,bounding_box = imcrop(img)  # cropped_img is the cropped part of the img
    
        >>> crp_obj=imcrop(img,'img_name')          # asks for interactive crop and returns an imcrop object
        <imcrop object at ...>
        
        >>> crp_obj.bounding_box                    # the bounding_box of the crop
        [[12, 15] , [134 , 232]]
        
        >>> img,bbox=imcrop(img,bbox)               # without interactive cropping
        
    """
    modes = {
        'standby': 0,
        'cropping': 1,
        'crop_finished': 2,
        'done_exit': 3}

    def __init__(self, img,bbox=None, window_name='image',):
        self.window_name =  window_name
        self.img=img
        if  bbox is None:
            self.bounding_box = []
            self.mode = 0
            self.crop()
        else:
            self.bounding_box=bbox

    def crop(self):
        cv2.namedWindow( self.window_name);
        cv2.setMouseCallback(self.window_name, self.on_click)
        while True:
            img2 = self.img.copy()
            if self.mode > 0:
                cv2.rectangle(img2, self.bounding_box[0], self.current_pos, (0, 255, 0), 1)
            key = imshow(img2,window_name=self.window_name,hold=True)
            try:
                cv2.getWindowProperty(self.window_name, 0)
            except cv2.error:
                break
            if self.mode == 3:
                break
        destroy_window(self.window_name)
        if len(self.bounding_box) != 2 or self.bounding_box[0][0] == self.bounding_box[1][0] or self.bounding_box[0][1] == self.bounding_box[1][1]:
            raise ValueError("Insufficient Points selected")

    def __iter__(self):
        bbox=self.bounding_box
        if bbox[0][0] > bbox[1][0]:
            bbox[1][0], bbox[0][0] = bbox[0][0], bbox[1][0]
        if bbox[0][1] > bbox[1][1]:
            bbox[1][1], bbox[0][1] = bbox[0][1], bbox[1][1]
        yield self.img[int(bbox[0][1]):int(bbox[1][1]), int(bbox[0][0]):int(bbox[1][0])]
        yield bbox

    def on_click(self, event, x, y, flags, param):
        if self.mode == 0 and event == cv2.EVENT_LBUTTONDOWN:
            self.mode = 1
            self.current_pos = (x, y)
            self.bounding_box = [(x, y)]
        elif self.mode == 1 and event == cv2.EVENT_LBUTTONUP:
            self.mode = 2
            self.bounding_box.append((x, y))
            self.current_pos = (x, y)
        elif self.mode == 1 and event == cv2.EVENT_MOUSEMOVE:
            self.current_pos = (x, y)
        elif self.mode == 2 and event == cv2.EVENT_RBUTTONDOWN:
            self.mode = 0
        elif self.mode == 2 and event == cv2.EVENT_LBUTTONDBLCLK:
            self.mode = 3

_kernel_shapes={
    'rectangle':cv2.MORPH_RECT,
    'square':   cv2.MORPH_RECT,
    'circle':   cv2.MORPH_ELLIPSE,
    'ellipse':   cv2.MORPH_ELLIPSE,
    'cross':    cv2.MORPH_CROSS
    } 

def _kernel(kernel_name,size):
    return cv2.getStructuringElement(_kernel_shapes[kernel_name],size)

def imdilate(img,kernel='circle',size=5,iterations=1):
    return cv2.dilate(img.copy(),_kernel(kernel,(size,size)),iterations = iterations)

def imerode(img,kernel='circle',size=5,iterations=1):
    return cv2.erode(img.copy(),_kernel(kernel,(size,size)),iterations = iterations)

def imopen(img,kernel='circle',size=5):
    return cv2.morphologyEx(img.copy(), cv2.MORPH_OPEN, _kernel(kernel,(size,size)))

def imclose(img,kernel='circle',size=5):
    return cv2.morphologyEx(img.copy(), cv2.MORPH_CLOSE, _kernel(kernel,(size,size)))

def centroid(contour):
    m = cv2.moments(contour)
    cx = int(m["m10"] / m["m00"]) 
    cy = int(m["m01"] / m["m00"])
    return np.array((cy,cx))     

def polylines(img,points,closed=False,color=(0,255,0),show_points=True):
    img=img.copy()
    if show_points:
        for point in points:
            point=tuple(map(int,point))
            cv2.circle(img,point, 2, (0,0,255), -1)
    pts = np.array(points, np.int32); 
    pts = pts.reshape((-1,1,2));
    return cv2.polylines(img,[pts],closed,color)
    
def rectangle(img,corner1,corner2,color=(255,255,255),linewidth=-1):
    cv2.rectangle(img,corner1,corner2,color,linewidth)

def find_shapes(img,show=True):
    shapes=defaultdict(list)
    contours = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[1]
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.1 * peri, True)
        if len(approx) == 3:
            shape_name = "triangle"
        elif len(approx) == 4:
            shape_name = "square"
        elif len(approx) == 5:
            shape_name = "pentagon"
        elif len(approx) == 6:
            shape_name = "hexagon"
        else:
            shape_name = "circle"
        shape=cv2.fillPoly(np.zeros_like(img), pts =[approx], color=(255,255,255))
        if show:
            imshow(shape,window_name=shape_name)
        shapes[shape_name].append(shape) 
    return shapes

class Color:
    """
    interactive Color picker and threshold images using them
    Theshold images according to a Color
    
    Example:
    >>> color=Color(img,color_name='red')              # asks for interactive crop to extract color
    Color red is initialized
    
    >>> color = Color(img,crop=False,colorspace='hsv')  # use hsv colorspace and dont crop
    
    >>> r,g,b = color                                   # unpack rgb vals of a color
    """
    colorspaces={
        'hsv':cv2.COLOR_BGR2HSV,
        'lab':cv2.COLOR_BGR2LAB,
        'yrb':cv2.COLOR_BGR2YCrCb
        }
    
    def __init__(self, img,color_name='color',colorspace=None,crop=True):
        if crop:
            img, bbox = try_to(imcrop, args=[img, color_name])
        self.color = np.zeros((2, 3))
        self.colorspace = colorspace
        if self.colorspace:
            img = cv2.cvtColor(img, Color.colorspaces[colorspace])
        for i in range(3):
            self.color[0, i] = img[:, :, i].max()
            self.color[1, i] = img[:, :, i].min()
        print("Color %s initialized" % (color_name,))        
        

    def threshold(self, img, err=np.array([35,5,5])):
        if self.colorspace:
            img = cv2.cvtColor(img, Color.colorspaces[self.colorspace])
        img=cv2.inRange(img, self.color[1, :] - err, self.color[0, :] + err)
        img=imopen(imclose(img),size=2)
        return img
    
    def __repr__(self):
        if not self.colorspace:
            colorspace='rgb'
        else:
            colorspace = self.colorspace
        return ("Mode :  "+ colorspace +'\n'+ str(self.color))

    def __iter__(self):
        for i in np.mean(self.color):
            yield i


if __name__ == "__main__":
    img=imread('1.jpeg')
    