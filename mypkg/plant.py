#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 kz-abi
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class Plant(Node):
    def __init__(self):
        super().__init__('plant')
        # 現在の値をパブリッシュ
        self.pub = self.create_publisher(Float32, 'current_val', 10)
        # 制御入力をサブスクライブ
        self.create_subscription(Float32, 'control_input', self.cb, 10)
        
        self.tmr = self.create_timer(0.05, self.timer_cb) # 0.05秒ごとに実行
        self.val = 0.0
        self.prev_val = 0.0
        self.input_val = 0.0

    def cb(self, msg):
        self.input_val = msg.data

    def timer_cb(self):
        # 簡易的な物理モデル (一次遅れ系のような挙動)
        # 入力値に近づこうとする動き
        self.val = self.prev_val + 0.1 * (self.input_val - self.prev_val)
        self.prev_val = self.val

        msg = Float32()
        msg.data = self.val
        self.pub.publish(msg)

def main():
    rclpy.init()
    node = Plant()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
