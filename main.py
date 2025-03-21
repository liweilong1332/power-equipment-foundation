#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
大块式设备基础计算程序 - 主程序入口
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

# 添加当前目录到系统路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# 导入自定义模块
from ui.main_window import MainWindow

def main():
    """程序入口函数"""
    # 创建应用程序实例
    app = QApplication(sys.argv)
    app.setApplicationName("大块式设备基础计算程序")
    
    # 设置应用程序图标（如果有）
    # app.setWindowIcon(QIcon('icon.png'))
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 