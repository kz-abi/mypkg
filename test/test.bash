#!/bin/bash
# SPDX-FileCopyrightText: 2025 kz-abi
# SPDX-License-Identifier: BSD-3-Clause

dir=~
[ "$1" != "" ] && dir="$1"

cd $dir/ros2_ws
colcon build
source $dir/ros2_ws/install/setup.bash

timeout 15 ros2 launch mypkg mypkg.launch.py > /tmp/mypkg_log.txt

# ログの中に期待する値が含まれているかチェック
# (grepの戻り値がそのままスクリプトの終了コード)
cat /tmp/mypkg_log.txt | grep 'Data: 49.0'
