#!/bin/bash
# SPDX-FileCopyrightText: 2025 kz-abi
# SPDX-License-Identifier: BSD-3-Clause

dir=~
[ "$1" != "" ] && dir="$1"

cd $dir/ros2_ws
colcon build
source $dir/ros2_ws/install/setup.bash 

#1. バックグラウンドでノードを起動
ros2 launch mypkg mypkg.launch.py > /dev/null 2>&1 &
PID=$! # プロセスIDを控える

# 2. 起動待ち
sleep 5

# 3. トピックの値を15秒間監視してファイルに保存
timeout 15 ros2 topic echo /current_val > /tmp/mypkg_log.txt

# テスト終了後にノードをキルする
kill $PID

# 4. ログの中に "49.0" が含まれているかチェック
if grep -q "49.0" /tmp/mypkg_log.txt; then
    echo "Test Passed: Target 50.0 reached!"
    exit 0
else
    echo "Test Failed: Target 50.0 not reached."
    cat /tmp/mypkg_log.txt # ログの中身を表示（デバッグ用）
    exit 1
fi
