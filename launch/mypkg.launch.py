#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 kz-abi
# SPDX-License-Identifier: BSD-3-Clause

import launch
import launch.actions
import launch.substitutions
import launch_ros.actions


def generate_launch_description():

    plant = launch_ros.actions.Node(
        package='mypkg',
        executable='plant',
        )

    controller = launch_ros.actions.Node(
        package='mypkg',
        executable='controller',
        )

    return launch.LaunchDescription([
        plant,
        controller,
    ])
