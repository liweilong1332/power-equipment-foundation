#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
工具函数模块 - 用于提供各种辅助功能
"""

import json
import os
import numpy as np
from datetime import datetime


def save_parameters(params, filename):
    """
    保存计算参数到JSON文件
    
    参数:
    params (dict): 计算参数字典
    filename (str): 文件名
    
    返回:
    bool: 保存成功返回True，否则返回False
    """
    try:
        # 确保扩展名为.json
        if not filename.endswith('.json'):
            filename += '.json'
            
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(params, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"保存参数失败: {str(e)}")
        return False


def load_parameters(filename):
    """
    从JSON文件加载计算参数
    
    参数:
    filename (str): 文件名
    
    返回:
    dict: 计算参数字典，加载失败返回None
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            params = json.load(f)
        return params
    except Exception as e:
        print(f"加载参数失败: {str(e)}")
        return None


def validate_parameters(params, required_fields):
    """
    验证参数是否有效
    
    参数:
    params (dict): 计算参数字典
    required_fields (list): 必须的字段列表
    
    返回:
    tuple: (是否有效, 错误信息)
    """
    # 检查必须字段
    for field in required_fields:
        if field not in params:
            return False, f"缺少必要参数: {field}"
        
    # 检查数值有效性
    for key, value in params.items():
        # 跳过非数值字段
        if key in ['name', 'description', 'date', 'unit']:
            continue
            
        try:
            val = float(value)
            # 大多数参数不能为负
            if val < 0 and key not in ['load_eccentricity_x', 'load_eccentricity_y']:
                return False, f"参数 {key} 不能为负值"
        except ValueError:
            return False, f"参数 {key} 不是有效的数值"
            
    return True, ""


def convert_units(value, from_unit, to_unit):
    """
    单位转换函数
    
    参数:
    value (float): 要转换的值
    from_unit (str): 原始单位
    to_unit (str): 目标单位
    
    返回:
    float: 转换后的值
    """
    # 长度单位转换
    length_units = {
        'm': 1,
        'cm': 0.01,
        'mm': 0.001
    }
    
    # 力单位转换
    force_units = {
        'kN': 1,
        'N': 0.001,
        'tf': 9.8,  # 吨力
        'kgf': 0.00981  # 千克力
    }
    
    # 压力单位转换
    pressure_units = {
        'kPa': 1,
        'MPa': 1000,
        'Pa': 0.001,
        'kgf/cm²': 98.0665  # 千克力/平方厘米
    }
    
    # 根据单位类型进行转换
    if from_unit in length_units and to_unit in length_units:
        return value * length_units[from_unit] / length_units[to_unit]
    elif from_unit in force_units and to_unit in force_units:
        return value * force_units[from_unit] / force_units[to_unit]
    elif from_unit in pressure_units and to_unit in pressure_units:
        return value * pressure_units[from_unit] / pressure_units[to_unit]
    else:
        # 单位类型不匹配或不支持的单位
        raise ValueError(f"不支持从 {from_unit} 到 {to_unit} 的转换")


def get_default_parameters():
    """
    获取默认计算参数
    
    返回:
    dict: 默认参数字典
    """
    return {
        "name": "新计算",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": "大块式设备基础计算",
        
        # 几何参数
        "length": 3.0,  # m
        "width": 2.0,   # m
        "height": 1.0,  # m
        "buried_depth": 0.5,  # m
        
        # 材料参数
        "concrete_strength": 30,  # MPa
        "elastic_modulus": 30000,  # MPa
        "soil_bearing_capacity": 200,  # kPa
        "soil_coefficient": 80000,  # kN/m³
        
        # 荷载参数
        "static_load": 500,  # kN
        "dynamic_load": 50,  # kN
        "frequency": 10,  # Hz
        "load_eccentricity_x": 0,  # m
        "load_eccentricity_y": 0,  # m
        
        # 其他参数
        "friction_coefficient": 0.45,
        "damping_ratio": 0.05,
        "equipment_mass": 20000  # kg
    }


def get_example_cases():
    """
    获取示例案例
    
    返回:
    list: 示例案例列表
    """
    return [
        {
            "name": "水泵基础",
            "description": "离心泵设备基础示例",
            "length": 2.0,
            "width": 1.2,
            "height": 0.8,
            "buried_depth": 0.4,
            "concrete_strength": 25,
            "elastic_modulus": 28000,
            "soil_bearing_capacity": 180,
            "soil_coefficient": 60000,
            "static_load": 120,
            "dynamic_load": 15,
            "frequency": 25,
            "load_eccentricity_x": 0.1,
            "load_eccentricity_y": 0,
            "friction_coefficient": 0.4,
            "damping_ratio": 0.05,
            "equipment_mass": 5000
        },
        {
            "name": "压缩机基础",
            "description": "往复式压缩机基础示例",
            "length": 4.0,
            "width": 2.5,
            "height": 1.5,
            "buried_depth": 0.8,
            "concrete_strength": 30,
            "elastic_modulus": 30000,
            "soil_bearing_capacity": 250,
            "soil_coefficient": 90000,
            "static_load": 800,
            "dynamic_load": 120,
            "frequency": 8,
            "load_eccentricity_x": 0.2,
            "load_eccentricity_y": 0.1,
            "friction_coefficient": 0.45,
            "damping_ratio": 0.08,
            "equipment_mass": 30000
        }
    ] 