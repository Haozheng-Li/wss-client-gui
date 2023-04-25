# ============================================
# wss-client-gui
# Author: Haozheng Li
# Created: 2023/4/20
#
# A PyQt-based GUI library for WSS projects
# ============================================
#
# Licensed under the MIT License.
# You may obtain a copy of the License at
#
#     https://opensource.org/licenses/MIT
#
# Copyright (c) 2023 Haozheng Li. All rights reserved.

from wss.core import launch

if __name__ == '__main__':
	launch_manager = launch.LaunchManager()
	launch_manager.launch_wss()
