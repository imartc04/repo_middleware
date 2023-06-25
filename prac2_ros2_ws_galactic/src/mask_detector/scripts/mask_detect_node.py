#!/usr/bin/python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
from keras.models import load_model
import time
model = load_model("/masterRSI/middleware/repo_middleware/prac2_ros2_ws_galactic/src/mask_detector/scripts/mask_detector_train/model2-007.model")

labels_dict = {0: "without mask", 1: "mask"}
color_dict = {0: (0, 0, 255), 1: (0, 255, 0)}

size = 4

# Create a CvBridge object
bridge = CvBridge()

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.subscription = self.create_subscription(
            Image,
            '/usb_cam/image_raw',
            self.image_callback,
            10
        )
        self.subscription

    def detect_mask(self, f_img):
    
        classifier = cv2.CascadeClassifier( "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")

        im = f_img
        im = cv2.flip(im, 1, 1)  # Flip to act as a mirror

        # Resize the image to speed up detection
        mini = cv2.resize(im, (im.shape[1] // size, im.shape[0] // size))
        # print("****** mini: ", mini.shape)
        # print("****** mini values: ", mini)

        if mini.any():
            # detect MultiScale / faces
            faces = classifier.detectMultiScale(mini)

            # Draw rectangles around each face
            for f in faces:
                (x, y, w, h) = [v * size for v in f]  # Scale the shapesize backup
                # Save just the rectangle faces in SubRecFaces
                face_img = im[y:y+h, x:x+w]
                resized = cv2.resize(face_img, (150, 150))
                normalized = resized/255.0
                reshaped = np.reshape(normalized, (1, 150, 150, 3))
                reshaped = np.vstack([reshaped])
                result = model.predict(reshaped)
                # print(result)

                label = np.argmax(result, axis=1)[0]

                cv2.rectangle(im, (x, y), (x+w, y+h), color_dict[label], 2)
                cv2.rectangle(im, (x, y-40), (x+w, y), color_dict[label], -1)
                cv2.putText(im, labels_dict[label], (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            # Show the image
            cv2.imshow("LIVE",   im)
            # time.sleep(0.01)
            key = cv2.waitKey(10)

    def image_callback(self, msg):
        # Image callback function
        # Process the received image data here
        # For example, you can access the image data as follows:
        # image_data = msg.data
        # image_width = msg.width
        # image_height = msg.height
        # Process the image data as needed
        print("ROS2 data received")
        # print("msg.data", msg.data)
        # print("type(msg.data)", type(msg.data))
        # Convert the ROS Image message to a OpenCV image
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        print("cv_image", type(cv_image))
        # self.detect_mask(numpy_array)
        self.detect_mask(cv_image)

def main(args=None):
    rclpy.init(args=args)
    image_subscriber = ImageSubscriber()
    rclpy.spin(image_subscriber)
    image_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
