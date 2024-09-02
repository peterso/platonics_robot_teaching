from feedback import Feedback
import typing
import panda_py
import rospkg
import yaml
class FeedbackButtons(Feedback):
    def __init__(self):
        super().__init__()
        self.pause=False
        self.spiral_flag = False
        self.spiral_feedback_correction = False
        self.stiff_rotation = False
        self.img_feedback_flag = False
        self.gripper_closed = False
        self.blocked = False

        # Connect to the Desk
        ros_pack = rospkg.RosPack()
        self._package_path = ros_pack.get_path('skills_manager')
        with open(self._package_path + '/config/login.yaml', 'rb') as f:
            login_info = yaml.safe_load(f)
        hostname = login_info['robot_ip']
        username = login_info['username']
        password = login_info['password']
        self.desk = panda_py.Desk(hostname, username, password)
        self.desk.listen(self.on_press)

    def on_press(self, event: typing.Dict) -> None:
        # print(event)
        read_events=list(event.keys())
        for i in range(len(read_events)):
            if read_events[i] == 'up':
                if event[read_events[i]] == True and not self.blocked:
                    self.pause=not(self.pause)
                    if self.pause==True:
                        print("Recording paused")    
                    else:
                        print("Recording started again")
                elif event[read_events[i]] == False:    
                    self.blocked = False        
            if read_events[i] == 'down':
                if event[read_events[i]] == True and not self.blocked:
                    self.blocked = True
                    if self.spiral_flag:
                        print("spiral disabled")
                        self.spiral_flag = False
                        self.spiral_feedback_correction = True
                    else:
                        print("spiral enabled")
                        self.spiral_flag = True
                        self.spiral_feedback_correction = True
                elif event[read_events[i]] == False:
                    self.blocked = False

            if read_events[i] == 'right':
                if event[read_events[i]] == True:
                    feedback_y = 1
            if read_events[i] == 'left':
                if event[read_events[i]] == True:
                    feedback_y = -1
            if read_events[i] == 'circle':
                if event[read_events[i]] == True and not self.blocked:
                    self.blocked = True
                    if self.gripper_closed:  
                        print("Gripper open")
                        self.gripper_closed = False
                    else:
                        self.gripper_closed =True
                        print("Gripper closed")
                elif event[read_events[i]] == False:
                    self.blocked = False
            if read_events[i] == 'cross':
                if event[read_events[i]] == True and not self.blocked:
                    self.blocked = True
                    self.end = True
                    print("Esc pressed. Stopping...")
                    # Stop listening
                    self.desk._listening = False
                elif event[read_events[i]] == False:
                    self.blocked = False
            if read_events[i] == 'check':
                if event[read_events[i]] == True and not self.blocked:
                    self.blocked = True
                    if self.img_feedback_flag:
                        print("camera feedback disabled")
                        self.img_feedback_flag = False
                        self.img_feedback_correction = True
                    else:
                        print("camera feedback enabled")
                        self.img_feedback_flag = True
                        self.img_feedback_correction = True
                elif event[read_events[i]] == False:
                    self.blocked = False
                    