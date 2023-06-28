#!/usr/bin/python3
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from custom_nav_interfaces.action import CustomNavAction
import time
from rclpy.action import GoalResponse
from std_srvs.srv import SetBool
import threading


class CustomNavActionServer(Node):

    def __init__(self):
        super().__init__('CustomNavAction_server')
        self._action_server = ActionServer(
            self,
            CustomNavAction,
            'custom_nav_action',
            self.execute_callback,
            cancel_callback = self.cancel_callback)

        self.canceled = False
        self.cancel_mt = threading.Lock()
        self.curr_goal = None

        self.cancel_srv = self.create_service(
            SetBool, 'custom_nav_cancel', self.cancel_service_callback)

        # Declare a parameter
        self.declare_parameter('init_pos', "-2.0, -0.23, 0.01, 0.99")
        self.nav_init = False
        self.navigator = BasicNavigator()

        self.init_navigator()
    
    def getCanceled(self):
        with self.cancel_mt:
            return self.canceled

    def setCanceled(self, f_value):
        with self.cancel_mt:
            self.canceled = f_value


    def cancel_service_callback(self, request, response):
        with self.cancel_mt:

            print("request.data", request.data)
            self.canceled = request.data
            
            if self.canceled:
                self.get_logger().info('Cancelling task in server')
                self.navigator.cancelTask()

        return {}

    

    def init_navigator(self):

        init_pos_param = self.get_parameter('init_pos').get_parameter_value().string_value.split(",")
        init_pos_param = [float(i) for i in init_pos_param]

        # Wait for navigation to fully activate, since autostarting nav2
        self.navigator.waitUntilNav2Active()

        if len(init_pos_param) >= 4:

            print("------------------ SET INIT POSE")

            # Set our demo's initial pose
            initial_pose = PoseStamped()
            initial_pose.header.frame_id = 'map'
            initial_pose.header.stamp = self.navigator.get_clock().now().to_msg()
            initial_pose.pose.position.x = init_pos_param[0]
            initial_pose.pose.position.y = init_pos_param[1]
            initial_pose.pose.orientation.z = init_pos_param[2]
            initial_pose.pose.orientation.w = init_pos_param[3]
            self.navigator.setInitialPose(initial_pose)

        else:
            self.get_logger().info('init_pos parameter must be set in the custom action server node')

       
        self.nav_init = True

    def execute_callback(self, goal_handle):

        if not self.getCanceled():

            #Create position to go
            pos = goal_handle.request.point.split(",")
            pos = [float(i) for i in pos]

            goal_pose = PoseStamped()
            goal_pose.header.frame_id = 'map'
            goal_pose.header.stamp = self.navigator.get_clock().now().to_msg()
            goal_pose.pose.position.x = pos[0]
            goal_pose.pose.position.y = pos[1]
            goal_pose.pose.orientation.w = pos[2]

            self.navigator.goToPose(goal_pose)

            feedback_msg = CustomNavAction.Feedback()
            #feedback_msg.dummy = 10
            while not self.navigator.isTaskComplete():
                time.sleep(0.5)
                #print("Navigating ...")
                goal_handle.publish_feedback(feedback_msg)
            
            # Do something depending on the return code
            result = self.navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                print('Goal succeeded!')
                goal_handle.succeed()
            elif result == TaskResult.CANCELED:
                print('Goal was canceled!')
                goal_handle.cancel()
            elif result == TaskResult.FAILED:
                print('Goal failed!')
                goal_handle.abort()
            else:
                print('Goal has an invalid return status!')
        
        else:
            self.get_logger().info('Goal execution is cancelled')


        ret = CustomNavAction.Result()  # Create an instance of the Result message type
        #ret.result = 0

        #time.sleep(10)

        return ret


    def cancel_callback(self, goal_handle):
        self.navigator.cancelTask()
        # Return a CancelResponse object indicating that the goal was successfully cancelled
        return GoalResponse.REJECT

def main(args=None):
    rclpy.init(args=args)

    action_server = CustomNavActionServer()

    rclpy.spin(action_server)


if __name__ == '__main__':
    main()