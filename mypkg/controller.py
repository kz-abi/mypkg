#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 kz-abi
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class Controller(Node):
    def __init__(self):
        super().__init__('controller')
        self.pub = self.create_publisher(Float32, 'control_input', 10)
        self.create_subscription(Float32, 'current_val', self.cb, 10)
        
        self.target = 50.0
        self.p_gain = 6.0
        self.i_gain = 0.08
        self.d_gain = 0.2
        self.err_sum = 0.0
        self.prev_error = 0.0

    def cb(self, msg):
        current_val = msg.data
        
        error = self.target - current_val
        self.err_sum += error
        
        d_term = error - self.prev_error
        
        # PID制御
        control_input = (
            error * self.p_gain + 
            self.err_sum * self.i_gain + 
            d_term * self.d_gain
        )

        # 今回の誤差を「前回」として保存
        self.prev_error = error

        msg = Float32()
        msg.data = control_input
        self.pub.publish(msg)

def main():
    rclpy.init()
    node = Controller()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
