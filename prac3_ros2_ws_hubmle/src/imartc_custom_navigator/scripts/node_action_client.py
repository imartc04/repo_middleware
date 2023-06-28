#!/usr/bin/python3
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from custom_nav_interfaces.action import CustomNavAction
import time
from rclpy.action import GoalResponse
import re
import yaml
from std_srvs.srv import Empty
import threading

class CustonNavActionClient(Node):

    def __init__(self):
        super().__init__('CustomNavAction_client')
        self._action_client = ActionClient(
            self, CustomNavAction, 'custom_nav_action')

        self.declare_parameter('point_yaml', "")

    def send_goal(self, order, f_id):

        goal_msg = CustomNavAction.Goal()
        goal_msg.point = order

        self.get_logger().info("Waiting for custom nav server to be active")
        self._action_client.wait_for_server()

        self.get_logger().info("Done")

        # print("sffdfsfsff")
        ret = self._action_client.send_goal(
            goal_msg)
    
      
    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result.sequence))
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(
            'Received feedback: {0}'.format(feedback.partial_sequence))


def parse_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    points = []
    for point_data in data:
        point = {
            'ID': point_data['ID'],
            'position': {
                'x': point_data['position']['x'],
                'y': point_data['position']['y']
            },
            'orientation': {
                'z': point_data['orientation']['z'],
                'w': point_data['orientation']['w']
            }
        }
        points.append(point)

    return points


def spinNode(f_node):
    rclpy.spin(f_node)

if __name__ == '__main__':

    rclpy.init(args=None)

    ac_client = CustonNavActionClient()

    param_yaml = ac_client.get_parameter(
        'point_yaml').get_parameter_value().string_value
    print("************ param_yaml ", param_yaml)

    my_thread = threading.Thread(target=spinNode, args=(ac_client,))

    # Start the thread
    my_thread.start()

    goals_sent = False
    while True:

        if re.match(".*\.yaml", param_yaml) and not goals_sent:
            points = parse_yaml(param_yaml)

            # Send each point to navigate
            for point in points:
                point_str = str(point["position"]["x"]) + "," + str(point["position"]["y"]) + "," + str(
                    point["orientation"]["z"]) + "," + str(point["orientation"]["w"])

                point_id = str(point["ID"])
                ac_client.send_goal(point_str, point_id)

            goals_sent = True

        else:
            param_yaml = input(
                "No point_yaml parameter set. Press some key here after setting it \n ")
            goals_sent = True
