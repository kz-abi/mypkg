#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 kz-abi
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class Controller(Node):
    def __init__(self):
        super().__init__('controller')
        # 制御入力をパブリッシュ
        self.pub = self.create_publisher(Float32, 'control_input', 10)
        # 現在の値をサブスクライブ
        self.create_subscription(Float32, 'current_val', self.cb, 10)
        
        self.target = 50.0 # 目標値
        self.p_gain = 2.0  # Pゲイン（比例ゲイン）

    def cb(self, msg):
        current_val = msg.data
        
        # P制御（目標値との差分にゲインを掛ける）
        error = self.target - current_val
        control_input = error * self.p_gain

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
