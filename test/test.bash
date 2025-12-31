#!/bin/bash
# SPDX-FileCopyrightText: 2025 kz-abi
# SPDX-License-Identifier: BSD-3-Clause

dir=~
[ "$1" != "" ] && dir="$1"

cd $dir/ros2_ws
colcon build
source $dir/.bashrc

ros2 launch mypkg mypkg.launch.py > /dev/null 2>&1 &

sleep 5

timeout 15 ros2 topic echo /current_val > /tmp/mypkg_log.txt

if grep -q "49.0" /tmp/mypkg_log.txt; then
    echo "Test Passed: Target 50.0 reached!"
    exit 0
else
    echo "Test Failed: Target 50.0 not reached."
    exit 1
fi
