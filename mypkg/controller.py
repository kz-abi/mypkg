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
        self.p_gain = 2.0
        self.i_gain = 0.02 
        self.err_sum = 0.0

    def cb(self, msg):
        current_val = msg.data
        
        # 偏差（目標 - 現在）を計算
        error = self.target - current_val
        
        # 誤差を積分（蓄積）
        self.err_sum += error

        # P制御 + I制御
        control_input = error * self.p_gain + self.err_sum * self.i_gain

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
