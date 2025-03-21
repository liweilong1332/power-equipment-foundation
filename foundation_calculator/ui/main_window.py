#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主窗口模块 - 程序的主界面
"""

import os
import sys
from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QAction, QFileDialog, 
                            QMessageBox, QMenu, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QWidget, QSplitter, QStatusBar)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QIcon

# 导入自定义模块
from .input_panels import (GeometryInputPanel, MaterialInputPanel, 
                          LoadInputPanel, BoundaryInputPanel)
from .result_view import ResultDisplayPanel

# 导入核心模块
from core.static_analysis import StaticAnalysis
from core.dynamic_analysis import DynamicAnalysis
from core.utils import save_parameters, load_parameters, get_default_parameters


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        
        # 初始化界面
        self.init_ui()
        
        # 加载默认参数
        self.current_parameters = get_default_parameters()
        
        # 设置窗口标题
        self.setWindowTitle("大块式设备基础计算程序")
        
        # 状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("就绪")
        
    def init_ui(self):
        """初始化用户界面"""
        # 设置窗口大小和位置
        self.resize(1024, 768)
        self.center_window()
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建主布局
        main_layout = QVBoxLayout()
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # 创建分割窗口
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 创建左侧输入面板
        input_widget = QWidget()
        input_layout = QVBoxLayout()
        input_widget.setLayout(input_layout)
        
        # 创建输入选项卡
        self.input_tabs = QTabWidget()
        
        # 创建各个输入面板
        self.geometry_panel = GeometryInputPanel()
        self.material_panel = MaterialInputPanel()
        self.load_panel = LoadInputPanel()
        self.boundary_panel = BoundaryInputPanel()
        
        # 添加选项卡
        self.input_tabs.addTab(self.geometry_panel, "基础尺寸")
        self.input_tabs.addTab(self.material_panel, "材料参数")
        self.input_tabs.addTab(self.load_panel, "荷载参数")
        self.input_tabs.addTab(self.boundary_panel, "边界条件")
        
        # 添加到输入布局
        input_layout.addWidget(self.input_tabs)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        
        # 创建计算按钮
        self.calculate_button = QPushButton("开始计算")
        self.calculate_button.clicked.connect(self.run_calculation)
        
        # 创建清空按钮
        self.clear_button = QPushButton("清空输入")
        self.clear_button.clicked.connect(self.clear_inputs)
        
        # 创建导出报告按钮
        self.export_button = QPushButton("导出报告")
        self.export_button.clicked.connect(self.export_report)
        self.export_button.setEnabled(False)  # 初始禁用
        
        # 创建导出计算书按钮
        self.export_calc_button = QPushButton("导出计算书")
        self.export_calc_button.clicked.connect(self.export_calculation_book)
        self.export_calc_button.setEnabled(False)  # 初始禁用
        
        # 添加按钮到布局
        button_layout.addWidget(self.calculate_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.export_calc_button)
        
        # 添加按钮布局到输入布局
        input_layout.addLayout(button_layout)
        
        # 创建右侧结果显示面板
        self.result_panel = ResultDisplayPanel()
        
        # 添加面板到分割窗口
        splitter.addWidget(input_widget)
        splitter.addWidget(self.result_panel)
        
        # 设置分割比例
        splitter.setSizes([400, 600])
        
    def center_window(self):
        """将窗口居中显示在屏幕上"""
        frame_geometry = self.frameGeometry()
        screen = self.screen()
        center_point = screen.availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())
        
    def create_menu_bar(self):
        """创建菜单栏"""
        # 文件菜单
        file_menu = self.menuBar().addMenu("文件")
        
        # 新建项目
        new_action = QAction("新建", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        # 打开项目
        open_action = QAction("打开", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)
        
        # 保存项目
        save_action = QAction("保存", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        
        # 分隔线
        file_menu.addSeparator()
        
        # 示例项目子菜单
        example_menu = QMenu("示例项目", self)
        file_menu.addMenu(example_menu)
        
        # 示例1
        example1_action = QAction("水泵基础", self)
        example1_action.triggered.connect(lambda: self.load_example(0))
        example_menu.addAction(example1_action)
        
        # 示例2
        example2_action = QAction("压缩机基础", self)
        example2_action.triggered.connect(lambda: self.load_example(1))
        example_menu.addAction(example2_action)
        
        # 分隔线
        file_menu.addSeparator()
        
        # 退出
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 计算菜单
        calc_menu = self.menuBar().addMenu("计算")
        
        # 开始计算
        run_action = QAction("开始计算", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(self.run_calculation)
        calc_menu.addAction(run_action)
        
        # 导出报告
        export_action = QAction("导出报告", self)
        export_action.triggered.connect(self.export_report)
        calc_menu.addAction(export_action)
        
        # 帮助菜单
        help_menu = self.menuBar().addMenu("帮助")
        
        # 关于
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def new_project(self):
        """新建项目"""
        # 确认对话框
        reply = QMessageBox.question(self, "新建项目", 
                                     "确定要新建项目吗？当前未保存的数据将丢失。",
                                     QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # 重置为默认参数
            self.current_parameters = get_default_parameters()
            self.update_ui_from_parameters()
            self.result_panel.clear_results()
            self.export_button.setEnabled(False)
            self.export_calc_button.setEnabled(False)
            self.statusBar.showMessage("已创建新项目")
    
    def open_project(self):
        """打开项目"""
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(
            self, "打开项目", "", "JSON文件 (*.json);;所有文件 (*)", 
            options=options
        )
        
        if filename:
            params = load_parameters(filename)
            if params:
                self.current_parameters = params
                self.update_ui_from_parameters()
                self.statusBar.showMessage(f"已加载项目: {os.path.basename(filename)}")
            else:
                QMessageBox.critical(self, "错误", "无法加载项目文件！")
    
    def save_project(self):
        """保存项目"""
        # 获取当前参数
        self.update_parameters_from_ui()
        
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            self, "保存项目", "", "JSON文件 (*.json);;所有文件 (*)", 
            options=options
        )
        
        if filename:
            success = save_parameters(self.current_parameters, filename)
            if success:
                self.statusBar.showMessage(f"项目已保存: {os.path.basename(filename)}")
            else:
                QMessageBox.critical(self, "错误", "无法保存项目文件！")
    
    def load_example(self, example_index):
        """加载示例项目"""
        from core.utils import get_example_cases
        examples = get_example_cases()
        
        if 0 <= example_index < len(examples):
            self.current_parameters = examples[example_index]
            self.update_ui_from_parameters()
            self.statusBar.showMessage(f"已加载示例项目: {examples[example_index]['name']}")
    
    def update_parameters_from_ui(self):
        """从UI获取参数更新到当前参数字典"""
        # 从各个面板获取参数
        geometry_params = self.geometry_panel.get_parameters()
        material_params = self.material_panel.get_parameters()
        load_params = self.load_panel.get_parameters()
        boundary_params = self.boundary_panel.get_parameters()
        
        # 更新当前参数
        self.current_parameters.update(geometry_params)
        self.current_parameters.update(material_params)
        self.current_parameters.update(load_params)
        self.current_parameters.update(boundary_params)
    
    def update_ui_from_parameters(self):
        """从当前参数更新UI"""
        # 更新各个面板
        self.geometry_panel.set_parameters(self.current_parameters)
        self.material_panel.set_parameters(self.current_parameters)
        self.load_panel.set_parameters(self.current_parameters)
        self.boundary_panel.set_parameters(self.current_parameters)
    
    def run_calculation(self):
        """运行计算"""
        # 从UI获取最新参数
        self.update_parameters_from_ui()
        
        try:
            # 准备参数
            params = self.current_parameters
            
            # 计算参数准备
            length = float(params["length"])
            width = float(params["width"])
            height = float(params["height"])
            buried_depth = float(params["buried_depth"])
            concrete_strength = float(params["concrete_strength"])
            elastic_modulus = float(params["elastic_modulus"])
            soil_bearing_capacity = float(params["soil_bearing_capacity"])
            soil_coefficient = float(params["soil_coefficient"])
            static_load = float(params["static_load"])
            dynamic_load = float(params["dynamic_load"])
            frequency = float(params["frequency"])
            load_eccentricity = (float(params["load_eccentricity_x"]), 
                                float(params["load_eccentricity_y"]))
            friction_coefficient = float(params["friction_coefficient"])
            damping_ratio = float(params["damping_ratio"])
            equipment_mass = float(params["equipment_mass"])
            
            # 计算基础自重和总质量
            concrete_density = 25  # kN/m³
            foundation_volume = length * width * height
            foundation_weight = foundation_volume * concrete_density  # kN
            foundation_mass = foundation_weight * 1000 / 9.81  # kg
            total_mass = foundation_mass + equipment_mass  # kg
            
            # 运行静力分析
            static_calculator = StaticAnalysis(
                length, width, height, buried_depth,
                concrete_strength, elastic_modulus, soil_bearing_capacity,
                static_load, load_eccentricity, friction_coefficient
            )
            static_results = static_calculator.run_analysis()
            
            # 运行动力分析
            dynamic_calculator = DynamicAnalysis(
                length, width, height, buried_depth,
                concrete_strength, elastic_modulus, soil_coefficient,
                dynamic_load, frequency, total_mass, damping_ratio
            )
            dynamic_results = dynamic_calculator.run_analysis()
            
            # 计算频率响应曲线数据
            freq_data, amp_data = dynamic_calculator.calculate_response_curve()
            
            # 构建完整结果
            results = {
                "parameters": self.current_parameters,
                "foundation_mass": foundation_mass,
                "total_mass": total_mass,
                "static_results": static_results,
                "dynamic_results": dynamic_results,
                "response_curve": {
                    "frequencies": freq_data.tolist(),
                    "amplitudes": amp_data.tolist()
                }
            }
            
            # 更新结果面板
            self.result_panel.display_results(results)
            
            # 启用导出报告按钮
            self.export_button.setEnabled(True)
            self.export_calc_button.setEnabled(True)
            
            # 更新状态栏
            overall_safety = (static_results["overall_safety"] and 
                            dynamic_results["is_safe"])
            
            if overall_safety:
                self.statusBar.showMessage("计算完成：设计满足要求")
            else:
                self.statusBar.showMessage("计算完成：设计不满足要求，请检查")
                
        except Exception as e:
            QMessageBox.critical(self, "计算错误", f"计算过程中出错：{str(e)}")
            import traceback
            traceback.print_exc()
    
    def clear_inputs(self):
        """清空输入"""
        reply = QMessageBox.question(self, "清空输入", 
                                    "确定要清空所有输入吗？",
                                    QMessageBox.Yes | QMessageBox.No, 
                                    QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # 重置为默认参数
            self.current_parameters = get_default_parameters()
            self.update_ui_from_parameters()
            self.statusBar.showMessage("输入已清空")
    
    def export_report(self):
        """导出计算报告"""
        from report.report_generator import generate_report
        
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            self, "导出报告", "", "PDF文件 (*.pdf);;Word文件 (*.docx)", 
            options=options
        )
        
        if filename:
            try:
                # 更新最新参数
                self.update_parameters_from_ui()
                
                # 获取结果数据
                results_data = self.result_panel.get_results_data()
                
                if results_data:
                    # 生成报告
                    success = generate_report(filename, self.current_parameters, results_data)
                    
                    if success:
                        self.statusBar.showMessage(f"报告已导出: {os.path.basename(filename)}")
                        # 打开报告
                        try:
                            os.startfile(filename)
                        except:
                            pass
                    else:
                        QMessageBox.critical(self, "错误", "无法生成报告！")
                else:
                    QMessageBox.warning(self, "警告", "请先进行计算后再导出报告！")
            except Exception as e:
                QMessageBox.critical(self, "导出错误", f"导出报告时出错：{str(e)}")
    
    def export_calculation_book(self):
        """导出详细计算书"""
        from report.report_generator import generate_report
        
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            self, "导出计算书", "", "PDF计算书 (*.pdf);;Word计算书 (*.docx)", 
            options=options
        )
        
        if filename:
            try:
                # 更新最新参数
                self.update_parameters_from_ui()
                
                # 获取结果数据
                results_data = self.result_panel.get_results_data()
                
                if results_data:
                    # 添加计算书标记
                    results_data["is_calculation_book"] = True
                    
                    # 生成计算书
                    success = generate_report(filename, self.current_parameters, results_data)
                    
                    if success:
                        self.statusBar.showMessage(f"计算书已导出: {os.path.basename(filename)}")
                        # 打开计算书
                        try:
                            os.startfile(filename)
                        except:
                            pass
                    else:
                        QMessageBox.critical(self, "错误", "无法生成计算书！")
                else:
                    QMessageBox.warning(self, "警告", "请先进行计算后再导出计算书！")
            except Exception as e:
                QMessageBox.critical(self, "导出错误", f"导出计算书时出错：{str(e)}")
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(self, "关于", 
                          "大块式设备基础计算程序\n\n"
                          "版本: 1.0.0\n"
                          "基于《动力机器基础设计标准》(GB 50040-2020)\n\n"
                          "Copyright © 2025 All Rights Reserved") 