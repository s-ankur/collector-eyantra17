"""
TODO:
Path Lib
Techilal
LED?
shapes implement as bw img
"""
from __future__ import print_function, division
from Util_library import *
from Robot_library import *
from CV_library import *
from Path_library import get_path


class Pixelate:
    color_names = {'red1','red2', 'yellow1','yellow2', 'green', 'white', 'brown', 'black', 'blue',}
    colors = {}

    def __init__(self):
        print("Starting Initialization")
        self.input_video = Video(1)
        self.input_video.set_view()
        self.robot=Robot('/dev/ttyUSB0')
        self.masks=None
        self.coords=None

    def init_colors(self):
        img=self.input_video.get_img()
        for color_name in self.color_names:
            try_to(self.get_color,args=[img,color_name])
        print("Initialization Done")        

    def init_statics(self):
        print("Initializing Statics")
        user_satisfied=False
        while not user_satisfied:
            img = self.input_video.get_img()

            """
            Get All Parts of the image according to the colors by threshold
            """
            black_part = self.colors['black'].threshold(img)            


            red_part1 = self.colors['red1'].threshold(img)  
            red_part2 = self.colors['red1'].threshold(img)            
            red_part= cv2.bitwise_or(red_part1 , red_part2)
            red_shapes=find_shapes(cv2.bitwise_and(red_part,black_part))
            self.cones = red_shapes.values() #list of circle shapes
            #self.ships = red_shapes #remaining red shapes

            blue_part = self.colors['blue'].threshold(img)            
            blue_shapes=find_shapes(blue_part)
            self.holes = blue_shapes.values() #list of circle shapes


        def get_color(self,img,color_name):
            self.colors[color_name] = Color(img,color_name,colorspace='lab')
            key=imshow(self.colors[color_name].threshold(img),color_name)
                if key =='r': 
                    raise ValueError("Redo Color Picking")


        def get_bot(self):
            return try_to(lambda:get_aruco_markers(self.input_video.get_img())['CB'])


                def go(self, point, kp=.5 ):
                    print("Going to point ", point)
                    while True:
                        bot_pos, bot_vector = self.get_bot()
                        dis = dist(bot_pos, point)
                        if dis < 0.4: break
                        self.align(point)
                        self.robot.forward(step=0.5)
                    print("Reached point ", point)

                def align(self, point, err=.1):
                    while True:
                        bot_pos,bot_vector = self.get_bot()
                        dest_vector=complex(bot_pos-point)
                        _,phi=cmath.polar(bot_vector/dest_vector)
                        phi=math.degrees(phi)
                        if phi < err:
                            break
                        self.bot.turn(phi)

                def task1(self):
                    print("Starting Task1")
                    self.masks['other_arena']=self.masks['arena2']
                    img = self.input_video.get_img()

                    cones=self.cones
                    holes=self.holes

                    for i in range(2):
                        bot = self.get_bot()            
                        cone = closest(cones, bot,key=centroid)
                        self.go(centroid(cone))
                        self.robot.pick()

                        bot = self.get_bot()
                        hole = closest( holes, bot,key=centroid)
                        self.go(centroid(hole))
                        self.robot.drop()

                    self.robot.glow_led('blue',delay=2)                
                    print("Completed Task1")

                def goto(self, source, dest):
                    print("Final Destination point ", dest)
                    obstacles = self.get_obstacles(excluding=[source,dest])
                    try:
                        path = get_path(obstacles, source, dest)
                    except:
                        path=[source,dest]
                    print(path)
                    for point in path[1:]:
                        go(point)
                    print("Reached Destination")


        def init2(self):
            green_part = self.colors['green'].threshold(img)            
            base_zone = imclose(green_part,kernel='square',size=125)
            imshow(base_zone,window_name='base_zone')            

            yellow1_part = self.colors['yellow1'].threshold(img)
            yellow2_part = self.colors['yellow2'].threshold(img)
            yellow_part = yellow1_part | yellow2_part
            station_zone= cv2.bitwise_and(yellow_part , base_zone)
            stations =  find_shapes(station_zone)      
            priority_zone = cv2.bitwise_and(yellow_part , cv2.bitwise_not(base_zone))
            orders = find_shapes(priority_zone) 
            orders= self.priority_order(orders)   

            black_part = self.colors['black'].threshold(img)            
            arena1 =  black_part
            imshow(arena1)

            white_part = self.colors['white'].threshold(img)            
            arena2 =  white_part 
            imshow(arena2)

            brown_part = self.colors['brown'].threshold(img)            
            obstacles= brown_part | priority_zone
            imshow(obstacles,window_name='obstacles')
            nonobstacles = cv2.bitwise_not(switch | base_zone)
            imshow(nonobstacles,window_name='nonobstacles')
            self.masks={
                'obstacles':obstacles,
                'nonobstacles':nonobstacles,
                'arena1':arena1,
                'arena2':arena2
            }
            user_satisfied = raw_input("Satisfied ? y/n").lower() in ('y', 'yes', 'ahoy')


    def _get_bot(self):
        img=self.input_video.get_img()
        botc1=centroid(self.colors['bot_color1'].threshold(img))
        botc2=centroid(self.colors['bot_color2'].threshold(img))
        return (botc1+botc2)/2,complex(*(botc1-botc2))

    def get_obstacles(self,excluding=()):
        masks=self.masks
        obstacles=(masks['obstacles'] | masks['other_arena']) & cv2.bitwise_not(masks['nonobstacles'])
        size=np.array([25,25])
        for i in excluding:
            cv2.rectangle(obstacles,i-size,i+size)
        return 

    def get_gate(self):    
        img = self.input_video.get_img()
        black_part=self.colors['black'].threshold(img)
        return centroid(find_shapes(black_part)['triangle'][0])

    def priority_order(self,shapes):
        return list(sorted(shapes.keys(),key=lambda x:centroid(shapes[x][0])[0]))    



    """
    BEGIN TASKS
    """



    def task2(self):
        print("Starting Task2")  

        switch = centroid(self.shapes['switch'])
        self.goto(switch)

        gate=try_to(self.get_gate)
        self.robot.glow_led('green',delay=3)        
        self.goto(gate)
        print("Completed Task2")

    def task3(self):
        print("Starting Task3")  

        self.masks['other_arena']=self.masks['arena2']        
        img=self.input_video.get_img()

        for shape_name in order_shapes :
            ship=centroid(ships[shape_name])
            station=centroid(stations[shape_name])
            self.goto(ship)
            self.robot.pick()
            self.goto(station)
            self.robot.drop()
        print("Completed Task3")




if __name__ == "__main__":
    pix = Pixelate() 
    #pix.init_colors()
    #pix.init_statics()
    #pix.task1()
    #pix.task2()
    #pix.task3()    

