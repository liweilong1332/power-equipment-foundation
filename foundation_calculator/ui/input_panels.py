#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
输入面板模块 - 各类输入界面组件
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                            QLabel, QLineEdit, QGroupBox, QComboBox,
                            QDoubleSpinBox, QSpinBox, QCheckBox, QSlider,
                            QSizePolicy)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator, QFont


class InputPanelBase(QWidget):
    """输入面板基类"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        # 子类实现
        pass
    
    def get_parameters(self):
        """获取面板参数"""
        # 子类实现
        return {}
    
    def set_parameters(self, params):
        """设置面板参数"""
        # 子类实现
        pass


class GeometryInputPanel(InputPanelBase):
    """几何参数输入面板"""
    
    def init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # 创建表单布局
        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        
        # 长度输入
        self.length_input = QDoubleSpinBox()
        self.length_input.setRange(0.1, 100.0)
        self.length_input.setSingleStep(0.1)
        self.length_input.setValue(3.0)
        self.length_input.setSuffix(" m")
        form_layout.addRow("基础长度:", self.length_input)
        
        # 宽度输入
        self.width_input = QDoubleSpinBox()
        self.width_input.setRange(0.1, 100.0)
        self.width_input.setSingleStep(0.1)
        self.width_input.setValue(2.0)
        self.width_input.setSuffix(" m")
        form_layout.addRow("基础宽度:", self.width_input)
        
        # 高度输入
        self.height_input = QDoubleSpinBox()
        self.height_input.setRange(0.1, 20.0)
        self.height_input.setSingleStep(0.1)
        self.height_input.setValue(1.0)
        self.height_input.setSuffix(" m")
        form_layout.addRow("基础高度:", self.height_input)
        
        # 埋深输入
        self.buried_depth_input = QDoubleSpinBox()
        self.buried_depth_input.setRange(0.0, 20.0)
        self.buried_depth_input.setSingleStep(0.1)
        self.buried_depth_input.setValue(0.5)
        self.buried_depth_input.setSuffix(" m")
        form_layout.addRow("埋深:", self.buried_depth_input)
        
        # 创建几何尺寸说明
        info_label = QLabel("注：基础长度指设备运行方向的尺寸")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: gray;")
        
        # 添加到主布局
        main_layout.addLayout(form_layout)
        main_layout.addWidget(info_label)
        main_layout.addStretch(1)  # 添加弹性空间
    
    def get_parameters(self):
        """获取几何参数"""
        return {
            "length": self.length_input.value(),
            "width": self.width_input.value(),
            "height": self.height_input.value(),
            "buried_depth": self.buried_depth_input.value()
        }
    
    def set_parameters(self, params):
        """设置几何参数"""
        if "length" in params:
            self.length_input.setValue(float(params["length"]))
        if "width" in params:
            self.width_input.setValue(float(params["width"]))
        if "height" in params:
            self.height_input.setValue(float(params["height"]))
        if "buried_depth" in params:
            self.buried_depth_input.setValue(float(params["buried_depth"]))


class MaterialInputPanel(InputPanelBase):
    """材料参数输入面板"""
    
    def init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # 创建混凝土参数组
        concrete_group = QGroupBox("混凝土参数")
        concrete_layout = QFormLayout()
        concrete_group.setLayout(concrete_layout)
        
        # 混凝土强度等级
        self.concrete_strength_input = QDoubleSpinBox()
        self.concrete_strength_input.setRange(10.0, 60.0)
        self.concrete_strength_input.setSingleStep(5.0)
        self.concrete_strength_input.setValue(30.0)
        self.concrete_strength_input.setSuffix(" MPa")
        concrete_layout.addRow("混凝土强度:", self.concrete_strength_input)
        
        # 弹性模量
        self.elastic_modulus_input = QSpinBox()
        self.elastic_modulus_input.setRange(10000, 50000)
        self.elastic_modulus_input.setSingleStep(1000)
        self.elastic_modulus_input.setValue(30000)
        self.elastic_modulus_input.setSuffix(" MPa")
        concrete_layout.addRow("弹性模量:", self.elastic_modulus_input)
        
        # 创建地基参数组
        soil_group = QGroupBox("地基参数")
        soil_layout = QFormLayout()
        soil_group.setLayout(soil_layout)
        
        # 地基承载力
        self.soil_bearing_capacity_input = QDoubleSpinBox()
        self.soil_bearing_capacity_input.setRange(50.0, 1000.0)
        self.soil_bearing_capacity_input.setSingleStep(10.0)
        self.soil_bearing_capacity_input.setValue(200.0)
        self.soil_bearing_capacity_input.setSuffix(" kPa")
        soil_layout.addRow("地基承载力:", self.soil_bearing_capacity_input)
        
        # 地基系数
        self.soil_coefficient_input = QSpinBox()
        self.soil_coefficient_input.setRange(10000, 200000)
        self.soil_coefficient_input.setSingleStep(5000)
        self.soil_coefficient_input.setValue(80000)
        self.soil_coefficient_input.setSuffix(" kN/m³")
        soil_layout.addRow("地基系数:", self.soil_coefficient_input)
        
        # 添加到主布局
        main_layout.addWidget(concrete_group)
        main_layout.addWidget(soil_group)
        main_layout.addStretch(1)  # 添加弹性空间
    
    def get_parameters(self):
        """获取材料参数"""
        return {
            "concrete_strength": self.concrete_strength_input.value(),
            "elastic_modulus": self.elastic_modulus_input.value(),
            "soil_bearing_capacity": self.soil_bearing_capacity_input.value(),
            "soil_coefficient": self.soil_coefficient_input.value()
        }
    
    def set_parameters(self, params):
        """设置材料参数"""
        if "concrete_strength" in params:
            self.concrete_strength_input.setValue(float(params["concrete_strength"]))
        if "elastic_modulus" in params:
            self.elastic_modulus_input.setValue(int(float(params["elastic_modulus"])))
        if "soil_bearing_capacity" in params:
            self.soil_bearing_capacity_input.setValue(float(params["soil_bearing_capacity"]))
        if "soil_coefficient" in params:
            self.soil_coefficient_input.setValue(int(float(params["soil_coefficient"])))


class LoadInputPanel(InputPanelBase):
    """荷载参数输入面板"""
    
    def init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # 创建静荷载参数组
        static_group = QGroupBox("静荷载参数")
        static_layout = QFormLayout()
        static_group.setLayout(static_layout)
        
        # 静荷载
        self.static_load_input = QDoubleSpinBox()
        self.static_load_input.setRange(0.0, 10000.0)
        self.static_load_input.setSingleStep(10.0)
        self.static_load_input.setValue(500.0)
        self.static_load_input.setSuffix(" kN")
        static_layout.addRow("静荷载:", self.static_load_input)
        
        # 荷载偏心X
        self.load_eccentricity_x_input = QDoubleSpinBox()
        self.load_eccentricity_x_input.setRange(-10.0, 10.0)
        self.load_eccentricity_x_input.setSingleStep(0.1)
        self.load_eccentricity_x_input.setValue(0.0)
        self.load_eccentricity_x_input.setSuffix(" m")
        static_layout.addRow("荷载偏心X:", self.load_eccentricity_x_input)
        
        # 荷载偏心Y
        self.load_eccentricity_y_input = QDoubleSpinBox()
        self.load_eccentricity_y_input.setRange(-10.0, 10.0)
        self.load_eccentricity_y_input.setSingleStep(0.1)
        self.load_eccentricity_y_input.setValue(0.0)
        self.load_eccentricity_y_input.setSuffix(" m")
        static_layout.addRow("荷载偏心Y:", self.load_eccentricity_y_input)
        
        # 创建动荷载参数组
        dynamic_group = QGroupBox("动荷载参数")
        dynamic_layout = QFormLayout()
        dynamic_group.setLayout(dynamic_layout)
        
        # 动力荷载幅值
        self.dynamic_load_input = QDoubleSpinBox()
        self.dynamic_load_input.setRange(0.0, 1000.0)
        self.dynamic_load_input.setSingleStep(5.0)
        self.dynamic_load_input.setValue(50.0)
        self.dynamic_load_input.setSuffix(" kN")
        dynamic_layout.addRow("动力荷载幅值:", self.dynamic_load_input)
        
        # 频率
        self.frequency_input = QDoubleSpinBox()
        self.frequency_input.setRange(0.1, 100.0)
        self.frequency_input.setSingleStep(1.0)
        self.frequency_input.setValue(10.0)
        self.frequency_input.setSuffix(" Hz")
        dynamic_layout.addRow("频率:", self.frequency_input)
        
        # 设备质量
        self.equipment_mass_input = QSpinBox()
        self.equipment_mass_input.setRange(100, 100000)
        self.equipment_mass_input.setSingleStep(100)
        self.equipment_mass_input.setValue(20000)
        self.equipment_mass_input.setSuffix(" kg")
        dynamic_layout.addRow("设备质量:", self.equipment_mass_input)
        
        # 添加到主布局
        main_layout.addWidget(static_group)
        main_layout.addWidget(dynamic_group)
        main_layout.addStretch(1)  # 添加弹性空间
    
    def get_parameters(self):
        """获取荷载参数"""
        return {
            "static_load": self.static_load_input.value(),
            "load_eccentricity_x": self.load_eccentricity_x_input.value(),
            "load_eccentricity_y": self.load_eccentricity_y_input.value(),
            "dynamic_load": self.dynamic_load_input.value(),
            "frequency": self.frequency_input.value(),
            "equipment_mass": self.equipment_mass_input.value()
        }
    
    def set_parameters(self, params):
        """设置荷载参数"""
        if "static_load" in params:
            self.static_load_input.setValue(float(params["static_load"]))
        if "load_eccentricity_x" in params:
            self.load_eccentricity_x_input.setValue(float(params["load_eccentricity_x"]))
        if "load_eccentricity_y" in params:
            self.load_eccentricity_y_input.setValue(float(params["load_eccentricity_y"]))
        if "dynamic_load" in params:
            self.dynamic_load_input.setValue(float(params["dynamic_load"]))
        if "frequency" in params:
            self.frequency_input.setValue(float(params["frequency"]))
        if "equipment_mass" in params:
            self.equipment_mass_input.setValue(int(float(params["equipment_mass"])))


class BoundaryInputPanel(InputPanelBase):
    """边界条件输入面板"""
    
    def init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # 创建边界参数组
        boundary_group = QGroupBox("边界参数")
        boundary_layout = QFormLayout()
        boundary_group.setLayout(boundary_layout)
        
        # 摩擦系数
        self.friction_coefficient_input = QDoubleSpinBox()
        self.friction_coefficient_input.setRange(0.1, 1.0)
        self.friction_coefficient_input.setSingleStep(0.05)
        self.friction_coefficient_input.setValue(0.45)
        self.friction_coefficient_input.setDecimals(2)
        boundary_layout.addRow("摩擦系数:", self.friction_coefficient_input)
        
        # 阻尼比
        self.damping_ratio_input = QDoubleSpinBox()
        self.damping_ratio_input.setRange(0.01, 0.2)
        self.damping_ratio_input.setSingleStep(0.01)
        self.damping_ratio_input.setValue(0.05)
        self.damping_ratio_input.setDecimals(2)
        boundary_layout.addRow("阻尼比:", self.damping_ratio_input)
        
        # 添加说明文字
        info_label = QLabel("注：摩擦系数取决于基础与地基接触面的材料特性，常规混凝土与土壤间取0.4-0.5")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: gray;")
        
        # 添加到主布局
        main_layout.addWidget(boundary_group)
        main_layout.addWidget(info_label)
        main_layout.addStretch(1)  # 添加弹性空间
    
    def get_parameters(self):
        """获取边界参数"""
        return {
            "friction_coefficient": self.friction_coefficient_input.value(),
            "damping_ratio": self.damping_ratio_input.value()
        }
    
    def set_parameters(self, params):
        """设置边界参数"""
        if "friction_coefficient" in params:
            self.friction_coefficient_input.setValue(float(params["friction_coefficient"]))
        if "damping_ratio" in params:
            self.damping_ratio_input.setValue(float(params["damping_ratio"])) 