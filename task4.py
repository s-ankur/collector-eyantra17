"""
* Team Id : CB#756
* Author List :[Ankur_Sonawane,Pratik_Kale]
* Filename: task4.py
* Theme: Collector_bot
* Classes:
    Task4
        main
        shadow
        test
        go
        reach_goal
        get_markers
        find_marker
"""
from __future__ import print_function, division
from ArucoVideo_library import *
from Vrep_library import *
from Robot_library import *
from pprint import pprint


class Task4:
    fruits = ['FreshFruit1', 'FreshFruit3', 'FreshFruit4']

    def __init__(self):
        self.robot = Robot(0)
        self.video = ArucoVideo(0, show=True)
        self.vrep = Vrep()
        self.vrep.init_models()
        self.set_roi()
        self.video.callback = self.vrep.update_models
        self.video.get_markers()

    def set_roi(self):
        print("Setting ROI")
        img = self.video.read()

        corner1 = self.video.find_marker('Corner1').pos - 30
        corner2 = self.video.find_marker('Corner2').pos + 30
        bbox = [list(corner1), list(corner2)]
        print(bbox)
        i2, _ = imcrop(img, bbox)
        self.video.set_roi(bbox)

    def find_truck(self):
        return self.video.find_marker('TRUCK').pos

    def find_closest_fruit(self):
        fruit_pos = {}
        bot_pos = self.video.find_marker('CB').pos
        for fruit_name in self.fruits:
            fruit_pos[fruit_name] = self.video.find_marker(fruit_name).pos
        goal_fruit = closest(self.fruits, bot_pos, key=fruit_pos.get)
        print("Closest: ", goal_fruit)
        return fruit_pos[goal_fruit]

    def go(self, point=None, marker=None, err=.15):
        print("going to ", point if point is not None else marker)
        while True:
            if marker:
                point = self.video.find_marker(marker).pos
            bot_pos, bot_vector = self.video.find_marker('CB')
            goal_vector = (point - bot_pos)
            phi = angle(goal_vector, bot_vector)
            self.robot.turn(phi)
            dis = dist(bot_pos, point)
            if dis < err:
                break
            self.robot.move(.3)
        print("Reached")

    def reach_goal(self, goal_pos, err=.15):
        self.go(goal_pos, err=200)
        bot_pos = self.video.find_marker('CB').pos
        self.vrep.update_models(self.video.get_markers())
        goal_vector = goal_pos - bot_pos
        goal_vector = .2 * (goal_vector / dist(goal_vector))
        self.vrep.update_models({'Goal': (goal_pos - goal_vector, goal_vector)})
        path = self.vrep.get_path()
        # path=self.vrep.filter_path(path)
        pprint(path)
        for point in path:
            self.go(point, err=0.15)
        self.go(goal_pos, err=err)

    def main(self):
        while self.fruits:
            fruit = self.find_closest_fruit()
            self.reach_goal(fruit, err=.30)
            # self.go(fruit)
            self.robot.pick()
            truck = self.find_truck()
            # self.reach_goal(truck,err=.6)
            self.go(marker='TRUCK', err=.45)
            self.robot.drop()

    def shadow(self):
        try:
            while True:
                markers = self.video.get_markers()
                self.vrep.update_models(markers)
        except KeyboardInterrupt:
            pass

    def test(self):
        while True:
            img = self.video.read()
            print(self.video.get_markers(img))
            imshow(img, window_name='test', hold=True)


if __name__ == "__main__":
    t = Task4()
    t.main()
    # t.go(np.array([0,0]))
