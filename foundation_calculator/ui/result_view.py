#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
结果显示面板模块 - 显示计算结果
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
                            QLabel, QTextEdit, QTableWidget, QTableWidgetItem,
                            QHeaderView, QSplitter, QFrame, QGridLayout,
                            QPushButton, QGroupBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QPixmap


class MatplotlibCanvas(FigureCanvas):
    """Matplotlib画布类"""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MatplotlibCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.fig.tight_layout()


class ResultDisplayPanel(QWidget):
    """结果显示面板类"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.results_data = None
        
    def init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # 创建选项卡
        self.tabs = QTabWidget()
        
        # 创建总体结果选项卡
        self.summary_tab = QWidget()
        self.summary_layout = QVBoxLayout()
        self.summary_tab.setLayout(self.summary_layout)
        
        # 创建静力分析选项卡
        self.static_tab = QWidget()
        self.static_layout = QVBoxLayout()
        self.static_tab.setLayout(self.static_layout)
        
        # 创建动力分析选项卡
        self.dynamic_tab = QWidget()
        self.dynamic_layout = QVBoxLayout()
        self.dynamic_tab.setLayout(self.dynamic_layout)
        
        # 创建3D模型选项卡
        self.model_tab = QWidget()
        self.model_layout = QVBoxLayout()
        self.model_tab.setLayout(self.model_layout)
        
        # 添加选项卡到选项卡组件
        self.tabs.addTab(self.summary_tab, "总体结果")
        self.tabs.addTab(self.static_tab, "静力分析")
        self.tabs.addTab(self.dynamic_tab, "动力分析")
        self.tabs.addTab(self.model_tab, "3D模型")
        
        # 添加选项卡组件到主布局
        main_layout.addWidget(self.tabs)
        
        # 初始化各选项卡的内容
        self.init_summary_tab()
        self.init_static_tab()
        self.init_dynamic_tab()
        self.init_model_tab()
        
    def init_summary_tab(self):
        """初始化总体结果选项卡"""
        # 添加结果标签
        self.summary_label = QLabel("请点击\"开始计算\"按钮进行计算")
        self.summary_label.setAlignment(Qt.AlignCenter)
        self.summary_label.setFont(QFont("Arial", 12))
        self.summary_layout.addWidget(self.summary_label)
        # 创建结果表格
        self.summary_table = QTableWidget(0, 2)
        self.summary_table.setHorizontalHeaderLabels(["检验项目", "结果"])
        self.summary_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.summary_table.verticalHeader().setVisible(False)
        self.summary_layout.addWidget(self.summary_table)
        
        # 添加基础信息框
        info_group = QGroupBox("基础信息")
        info_layout = QGridLayout()
        info_group.setLayout(info_layout)
        
        # 基础几何信息
        self.foundation_info_label = QLabel("尺寸: - × - × - m")
        info_layout.addWidget(self.foundation_info_label, 0, 0)
        
        # 基础质量信息
        self.foundation_mass_label = QLabel("基础质量: - kg")
        info_layout.addWidget(self.foundation_mass_label, 1, 0)
        
        # 设备质量信息
        self.equipment_mass_label = QLabel("设备质量: - kg")
        info_layout.addWidget(self.equipment_mass_label, 1, 1)
        
        # 总质量信息
        self.total_mass_label = QLabel("总质量: - kg")
        info_layout.addWidget(self.total_mass_label, 2, 0)
        
        # 添加到布局
        self.summary_layout.addWidget(info_group)
        
    def init_static_tab(self):
        """初始化静力分析选项卡"""
        # 创建表格布局
        grid_layout = QGridLayout()
        
        # 添加抗滑移稳定性组
        sliding_group = QGroupBox("抗滑移稳定性验算")
        sliding_layout = QVBoxLayout()
        sliding_group.setLayout(sliding_layout)
        
        # 创建抗滑移结果表格
        self.sliding_table = QTableWidget(3, 2)
        self.sliding_table.setHorizontalHeaderLabels(["项目", "数值"])
        self.sliding_table.setVerticalHeaderLabels(["抗滑力", "滑动力", "安全系数"])
        self.sliding_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        sliding_layout.addWidget(self.sliding_table)
        
        # 添加判定结果标签
        self.sliding_result_label = QLabel("判定: 未计算")
        self.sliding_result_label.setAlignment(Qt.AlignCenter)
        sliding_layout.addWidget(self.sliding_result_label)
        
        # 添加抗倾覆稳定性组
        overturning_group = QGroupBox("抗倾覆稳定性验算")
        overturning_layout = QVBoxLayout()
        overturning_group.setLayout(overturning_layout)
        
        # 创建抗倾覆结果表格
        self.overturning_table = QTableWidget(3, 2)
        self.overturning_table.setHorizontalHeaderLabels(["项目", "数值"])
        self.overturning_table.setVerticalHeaderLabels(["抗倾覆力矩", "倾覆力矩", "安全系数"])
        self.overturning_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        overturning_layout.addWidget(self.overturning_table)
        
        # 添加判定结果标签
        self.overturning_result_label = QLabel("判定: 未计算")
        self.overturning_result_label.setAlignment(Qt.AlignCenter)
        overturning_layout.addWidget(self.overturning_result_label)
        
        # 添加地基承载力验算组
        bearing_group = QGroupBox("地基承载力验算")
        bearing_layout = QVBoxLayout()
        bearing_group.setLayout(bearing_layout)
        
        # 创建地基承载力结果表格
        self.bearing_table = QTableWidget(2, 2)
        self.bearing_table.setHorizontalHeaderLabels(["项目", "数值"])
        self.bearing_table.setVerticalHeaderLabels(["实际地基压力", "地基允许承载力"])
        self.bearing_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        bearing_layout.addWidget(self.bearing_table)
        
        # 添加判定结果标签
        self.bearing_result_label = QLabel("判定: 未计算")
        self.bearing_result_label.setAlignment(Qt.AlignCenter)
        bearing_layout.addWidget(self.bearing_result_label)
        
        # 添加到网格布局
        grid_layout.addWidget(sliding_group, 0, 0)
        grid_layout.addWidget(overturning_group, 0, 1)
        grid_layout.addWidget(bearing_group, 1, 0, 1, 2)
        
        # 添加到静力分析布局
        self.static_layout.addLayout(grid_layout)
        
    def init_dynamic_tab(self):
        """初始化动力分析选项卡"""
        # 创建动力分析结果组
        dynamic_group = QGroupBox("动力响应分析")
        dynamic_layout = QGridLayout()
        dynamic_group.setLayout(dynamic_layout)
        
        # 创建动力分析结果表格
        self.dynamic_table = QTableWidget(6, 2)
        self.dynamic_table.setHorizontalHeaderLabels(["项目", "数值"])
        self.dynamic_table.setVerticalHeaderLabels([
            "自然频率", "激励频率", "频率比", 
            "振动传递率", "振动幅值", "容许振幅"
        ])
        self.dynamic_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        dynamic_layout.addWidget(self.dynamic_table, 0, 0, 1, 2)
        
        # 添加判定结果标签
        self.dynamic_result_label = QLabel("判定: 未计算")
        self.dynamic_result_label.setAlignment(Qt.AlignCenter)
        dynamic_layout.addWidget(self.dynamic_result_label, 1, 0, 1, 2)
        
        # 共振风险提示
        self.resonance_label = QLabel("共振风险: 未计算")
        self.resonance_label.setAlignment(Qt.AlignCenter)
        dynamic_layout.addWidget(self.resonance_label, 2, 0, 1, 2)
        
        # 添加响应曲线绘图区
        self.response_canvas = MatplotlibCanvas(self, width=6, height=4, dpi=100)
        dynamic_layout.addWidget(self.response_canvas, 3, 0, 1, 2)
        
        # 添加到动力分析布局
        self.dynamic_layout.addWidget(dynamic_group)
        
    def init_model_tab(self):
        """初始化3D模型选项卡"""
        # 创建3D模型绘图区
        self.model_canvas = MatplotlibCanvas(self, width=6, height=5, dpi=100)
        self.model_layout.addWidget(self.model_canvas)
        
        # 添加导航工具栏
        self.model_toolbar = NavigationToolbar(self.model_canvas, self)
        self.model_layout.addWidget(self.model_toolbar)
        
    def display_results(self, results):
        """
        显示计算结果
        
        参数:
        results (dict): 计算结果字典
        """
        # 保存结果数据
        self.results_data = results
        
        # 提取参数和结果
        params = results["parameters"]
        static_results = results["static_results"]
        dynamic_results = results["dynamic_results"]
        foundation_mass = results["foundation_mass"]
        total_mass = results["total_mass"]
        response_curve = results["response_curve"]
        
        # 更新总体结果
        self.update_summary_tab(params, static_results, dynamic_results,
                              foundation_mass, total_mass)
        
        # 更新静力分析结果
        self.update_static_tab(static_results)
        
        # 更新动力分析结果
        self.update_dynamic_tab(dynamic_results, response_curve)
        
        # 更新3D模型
        self.update_model_tab(params)
        
    def update_summary_tab(self, params, static_results, dynamic_results,
                         foundation_mass, total_mass):
        """更新总体结果选项卡"""
        # 更新结果标签
        overall_safety = (static_results["overall_safety"] and 
                         dynamic_results["is_safe"])
        
        if overall_safety:
            self.summary_label.setText("计算结果：设计满足要求 ✓")
            self.summary_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.summary_label.setText("计算结果：设计不满足要求 ✗")
            self.summary_label.setStyleSheet("color: red; font-weight: bold;")
        
        # 更新结果表格
        self.summary_table.setRowCount(3)
        
        # 抗滑移稳定性
        item1 = QTableWidgetItem("抗滑移稳定性")
        self.summary_table.setItem(0, 0, item1)
        
        sliding_safe = static_results["sliding_stability"]["is_safe"]
        if sliding_safe:
            item2 = QTableWidgetItem("满足 ✓")
            item2.setForeground(QColor("green"))
        else:
            item2 = QTableWidgetItem("不满足 ✗")
            item2.setForeground(QColor("red"))
        self.summary_table.setItem(0, 1, item2)
        
        # 抗倾覆稳定性
        item3 = QTableWidgetItem("抗倾覆稳定性")
        self.summary_table.setItem(1, 0, item3)
        
        overturning_safe = static_results["overturning_stability"]["is_safe"]
        if overturning_safe:
            item4 = QTableWidgetItem("满足 ✓")
            item4.setForeground(QColor("green"))
        else:
            item4 = QTableWidgetItem("不满足 ✗")
            item4.setForeground(QColor("red"))
        self.summary_table.setItem(1, 1, item4)
        
        # 振动响应
        item5 = QTableWidgetItem("振动响应")
        self.summary_table.setItem(2, 0, item5)
        
        dynamic_safe = dynamic_results["is_safe"]
        if dynamic_safe:
            item6 = QTableWidgetItem("满足 ✓")
            item6.setForeground(QColor("green"))
        else:
            item6 = QTableWidgetItem("不满足 ✗")
            item6.setForeground(QColor("red"))
        self.summary_table.setItem(2, 1, item6)
        
        # 更新基础信息
        length = params["length"]
        width = params["width"]
        height = params["height"]
        buried_depth = params["buried_depth"]
        
        self.foundation_info_label.setText(f"尺寸: {length:.2f} × {width:.2f} × {height:.2f} m, 埋深: {buried_depth:.2f} m")
        self.foundation_mass_label.setText(f"基础质量: {foundation_mass:.0f} kg")
        self.equipment_mass_label.setText(f"设备质量: {params['equipment_mass']:.0f} kg")
        self.total_mass_label.setText(f"总质量: {total_mass:.0f} kg")
        
    def update_static_tab(self, static_results):
        """更新静力分析选项卡"""
        # 提取结果
        sliding = static_results["sliding_stability"]
        overturning = static_results["overturning_stability"]
        bearing = static_results["bearing_capacity"]
        
        # 更新抗滑移表格
        # 假定数据，实际应根据计算结果提供
        anti_sliding_force = sliding["safety_factor"] * 0.1 * static_results["total_weight"]
        sliding_force = 0.1 * static_results["total_weight"]
        
        self.sliding_table.setItem(0, 1, QTableWidgetItem(f"{anti_sliding_force:.2f} kN"))
        self.sliding_table.setItem(1, 1, QTableWidgetItem(f"{sliding_force:.2f} kN"))
        self.sliding_table.setItem(2, 1, QTableWidgetItem(f"{sliding['safety_factor']:.2f}"))
        
        # 更新判定结果
        if sliding["is_safe"]:
            self.sliding_result_label.setText(f"判定: 满足要求 ✓ (安全系数 > {sliding['required_factor']})")
            self.sliding_result_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.sliding_result_label.setText(f"判定: 不满足要求 ✗ (安全系数 < {sliding['required_factor']})")
            self.sliding_result_label.setStyleSheet("color: red; font-weight: bold;")
        
        # 更新抗倾覆表格
        # 假定数据，实际应根据计算结果提供
        stabilizing_moment = overturning["safety_factor"] * 0.1 * static_results["total_weight"] * 1.0
        overturning_moment = 0.1 * static_results["total_weight"] * 1.0
        
        self.overturning_table.setItem(0, 1, QTableWidgetItem(f"{stabilizing_moment:.2f} kN·m"))
        self.overturning_table.setItem(1, 1, QTableWidgetItem(f"{overturning_moment:.2f} kN·m"))
        self.overturning_table.setItem(2, 1, QTableWidgetItem(f"{overturning['safety_factor']:.2f}"))
        
        # 更新判定结果
        if overturning["is_safe"]:
            self.overturning_result_label.setText(f"判定: 满足要求 ✓ (安全系数 > {overturning['required_factor']})")
            self.overturning_result_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.overturning_result_label.setText(f"判定: 不满足要求 ✗ (安全系数 < {overturning['required_factor']})")
            self.overturning_result_label.setStyleSheet("color: red; font-weight: bold;")
        
        # 更新地基承载力表格
        self.bearing_table.setItem(0, 1, QTableWidgetItem(f"{bearing['actual_pressure']:.2f} kPa"))
        self.bearing_table.setItem(1, 1, QTableWidgetItem(f"{bearing['allowable_pressure']:.2f} kPa"))
        
        # 更新判定结果
        if bearing["is_safe"]:
            self.bearing_result_label.setText("判定: 满足要求 ✓ (实际压力 < 允许承载力)")
            self.bearing_result_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.bearing_result_label.setText("判定: 不满足要求 ✗ (实际压力 > 允许承载力)")
            self.bearing_result_label.setStyleSheet("color: red; font-weight: bold;")
        
    def update_dynamic_tab(self, dynamic_results, response_curve):
        """更新动力分析选项卡"""
        # 更新动力分析表格
        self.dynamic_table.setItem(0, 1, QTableWidgetItem(f"{dynamic_results['natural_frequency']:.2f} Hz"))
        self.dynamic_table.setItem(1, 1, QTableWidgetItem(f"{dynamic_results['frequency_ratio'] * dynamic_results['natural_frequency']:.2f} Hz"))
        self.dynamic_table.setItem(2, 1, QTableWidgetItem(f"{dynamic_results['frequency_ratio']:.2f}"))
        self.dynamic_table.setItem(3, 1, QTableWidgetItem(f"{dynamic_results['transmissibility']:.2f}"))
        self.dynamic_table.setItem(4, 1, QTableWidgetItem(f"{dynamic_results['amplitude']:.3f} mm"))
        self.dynamic_table.setItem(5, 1, QTableWidgetItem(f"{dynamic_results['allowable_amplitude']:.3f} mm"))
        
        # 更新判定结果
        if dynamic_results["is_safe"]:
            self.dynamic_result_label.setText("判定: 满足要求 ✓ (振幅 < 容许值)")
            self.dynamic_result_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.dynamic_result_label.setText("判定: 不满足要求 ✗ (振幅 > 容许值)")
            self.dynamic_result_label.setStyleSheet("color: red; font-weight: bold;")
        
        # 更新共振风险提示
        if dynamic_results["resonance_risk"]:
            self.resonance_label.setText(f"共振风险: 存在 ⚠ (频率比={dynamic_results['frequency_ratio']:.2f})")
            self.resonance_label.setStyleSheet("color: orange; font-weight: bold;")
        else:
            self.resonance_label.setText(f"共振风险: 无 ✓ (频率比={dynamic_results['frequency_ratio']:.2f})")
            self.resonance_label.setStyleSheet("color: green;")
        
        # 绘制响应曲线
        self.response_canvas.axes.clear()
        freqs = response_curve["frequencies"]
        amps = response_curve["amplitudes"]
        
        self.response_canvas.axes.plot(freqs, amps, 'b-')
        
        # 标记自然频率
        natural_freq = dynamic_results["natural_frequency"]
        self.response_canvas.axes.axvline(x=natural_freq, color='r', linestyle='--', alpha=0.7)
        
        # 标记当前频率
        current_freq = dynamic_results["frequency_ratio"] * natural_freq
        current_amp = dynamic_results["amplitude"]
        self.response_canvas.axes.plot(current_freq, current_amp, 'ro')
        
        # 添加容许振幅线
        allowable_amp = dynamic_results["allowable_amplitude"]
        self.response_canvas.axes.axhline(y=allowable_amp, color='g', linestyle='-.', alpha=0.7)
        
        # 设置标题和标签
        self.response_canvas.axes.set_title("频率响应曲线")
        self.response_canvas.axes.set_xlabel("频率 (Hz)")
        self.response_canvas.axes.set_ylabel("振幅 (mm)")
        self.response_canvas.axes.grid(True)
        
        # 添加图例
        self.response_canvas.axes.legend(["响应曲线", "自然频率", "当前工作点", "容许振幅"])
        
        # 更新画布
        self.response_canvas.fig.tight_layout()
        self.response_canvas.draw()
        
    def update_model_tab(self, params):
        """更新3D模型选项卡"""
        # 提取参数
        length = params["length"]
        width = params["width"]
        height = params["height"]
        buried_depth = params["buried_depth"]
        
        # 清除旧图形
        self.model_canvas.fig.clear()
        
        # 创建3D坐标轴
        ax = self.model_canvas.fig.add_subplot(111, projection='3d')
        
        # 设置视角
        ax.view_init(elev=30, azim=45)
        
        # 绘制地面
        x = np.linspace(-1, length + 1, 10)
        y = np.linspace(-1, width + 1, 10)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        ax.plot_surface(X, Y, Z, color='green', alpha=0.2)
        
        # 绘制基础
        # 底面顶点
        x1, y1, z1 = 0, 0, -buried_depth
        x2, y2, z2 = length, 0, -buried_depth
        x3, y3, z3 = length, width, -buried_depth
        x4, y4, z4 = 0, width, -buried_depth
        
        # 顶面顶点
        x5, y5, z5 = 0, 0, height - buried_depth
        x6, y6, z6 = length, 0, height - buried_depth
        x7, y7, z7 = length, width, height - buried_depth
        x8, y8, z8 = 0, width, height - buried_depth
        
        # 绘制底面
        ax.plot([x1, x2, x3, x4, x1], [y1, y2, y3, y4, y1], [z1, z2, z3, z4, z1], 'b-')
        
        # 绘制顶面
        ax.plot([x5, x6, x7, x8, x5], [y5, y6, y7, y8, y5], [z5, z6, z7, z8, z5], 'b-')
        
        # 绘制侧面
        ax.plot([x1, x5], [y1, y5], [z1, z5], 'b-')
        ax.plot([x2, x6], [y2, y6], [z2, z6], 'b-')
        ax.plot([x3, x7], [y3, y7], [z3, z7], 'b-')
        ax.plot([x4, x8], [y4, y8], [z4, z8], 'b-')
        
        # 填充表面 - 修改为使用plot_surface而不是fill3d
        # 绘制底面
        bottom_x = np.array([[x1, x2], [x4, x3]])
        bottom_y = np.array([[y1, y2], [y4, y3]])
        bottom_z = np.array([[z1, z2], [z4, z3]])
        ax.plot_surface(bottom_x, bottom_y, bottom_z, color='gray', alpha=0.3)
        
        # 绘制顶面
        top_x = np.array([[x5, x6], [x8, x7]])
        top_y = np.array([[y5, y6], [y8, y7]])
        top_z = np.array([[z5, z6], [z8, z7]])
        ax.plot_surface(top_x, top_y, top_z, color='lightgray', alpha=0.7)
        
        # 设置轴标签
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        
        # 设置标题
        ax.set_title("基础3D模型")
        
        # 设置坐标轴范围
        ax.set_xlim(-0.5, length + 0.5)
        ax.set_ylim(-0.5, width + 0.5)
        ax.set_zlim(-buried_depth - 0.5, height - buried_depth + 0.5)
        
        # 更新画布
        self.model_canvas.fig.tight_layout()
        self.model_canvas.draw()
        
    def clear_results(self):
        """清空结果显示"""
        # 重置结果数据
        self.results_data = None
        
        # 重置总体结果
        self.summary_label.setText("请点击\"开始计算\"按钮进行计算")
        self.summary_label.setStyleSheet("")
        self.summary_table.setRowCount(0)
        self.foundation_info_label.setText("尺寸: - × - × - m")
        self.foundation_mass_label.setText("基础质量: - kg")
        self.equipment_mass_label.setText("设备质量: - kg")
        self.total_mass_label.setText("总质量: - kg")
        
        # 重置静力分析结果
        for table in [self.sliding_table, self.overturning_table, self.bearing_table]:
            for row in range(table.rowCount()):
                table.setItem(row, 1, QTableWidgetItem("-"))
                
        self.sliding_result_label.setText("判定: 未计算")
        self.sliding_result_label.setStyleSheet("")
        self.overturning_result_label.setText("判定: 未计算")
        self.overturning_result_label.setStyleSheet("")
        self.bearing_result_label.setText("判定: 未计算")
        self.bearing_result_label.setStyleSheet("")
        
        # 重置动力分析结果
        for row in range(self.dynamic_table.rowCount()):
            self.dynamic_table.setItem(row, 1, QTableWidgetItem("-"))
            
        self.dynamic_result_label.setText("判定: 未计算")
        self.dynamic_result_label.setStyleSheet("")
        self.resonance_label.setText("共振风险: 未计算")
        self.resonance_label.setStyleSheet("")
        
        # 清除图表
        self.response_canvas.axes.clear()
        self.response_canvas.draw()
        
        # 清除3D模型
        self.model_canvas.fig.clear()
        self.model_canvas.draw()
        
    def get_results_data(self):
        """获取结果数据，用于报告生成"""
        return self.results_data 