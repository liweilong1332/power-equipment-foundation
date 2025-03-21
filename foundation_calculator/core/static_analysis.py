#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
静力分析模块 - 用于计算大块式设备基础的静力参数
包括：抗滑移稳定性、抗倾覆稳定性、地基承载力验算等
"""

import numpy as np


class StaticAnalysis:
    """静力分析类"""
    
    def __init__(self, length, width, height, buried_depth,
                 concrete_strength, elastic_modulus, soil_bearing_capacity,
                 static_load, load_eccentricity=(0, 0), friction_coefficient=0.45):
        """
        初始化静力分析参数
        
        参数:
        length (float): 基础长度(m)
        width (float): 基础宽度(m)
        height (float): 基础高度(m)
        buried_depth (float): 埋深(m)
        concrete_strength (float): 混凝土强度(MPa)
        elastic_modulus (float): 弹性模量(MPa)
        soil_bearing_capacity (float): 地基承载力(kPa)
        static_load (float): 静荷载(kN)
        load_eccentricity (tuple): 荷载偏心距(m, m)
        friction_coefficient (float): 摩擦系数
        """
        self.length = length
        self.width = width
        self.height = height
        self.buried_depth = buried_depth
        self.concrete_strength = concrete_strength
        self.elastic_modulus = elastic_modulus
        self.soil_bearing_capacity = soil_bearing_capacity
        self.static_load = static_load
        self.load_eccentricity = load_eccentricity
        self.friction_coefficient = friction_coefficient
        
        # 计算自重
        self.concrete_density = 25  # kN/m³ (标准钢筋混凝土密度)
        self.soil_density = 18      # kN/m³ (一般土壤密度)
        self.self_weight = self.calculate_self_weight()
        
    def calculate_self_weight(self):
        """计算基础自重(kN)"""
        foundation_volume = self.length * self.width * self.height
        foundation_weight = foundation_volume * self.concrete_density
        
        # 计算填土重量
        if self.buried_depth > self.height:
            soil_volume = self.length * self.width * (self.buried_depth - self.height)
            soil_weight = soil_volume * self.soil_density
        else:
            soil_weight = 0
            
        return foundation_weight + soil_weight
    
    def sliding_stability(self):
        """
        计算抗滑移稳定性
        
        返回:
        tuple: (抗滑移安全系数, 是否满足要求)
        """
        # 水平荷载 (假设为静荷载的10%，实际工程中应根据具体情况计算)
        horizontal_load = self.static_load * 0.1
        
        # 抗滑力
        anti_sliding_force = (self.self_weight + self.static_load) * self.friction_coefficient
        
        # 抗滑移安全系数
        safety_factor = anti_sliding_force / horizontal_load if horizontal_load > 0 else float('inf')
        
        # 安全系数应大于1.3
        is_safe = safety_factor >= 1.3
        
        return safety_factor, is_safe
    
    def overturning_stability(self):
        """
        计算抗倾覆稳定性
        
        返回:
        tuple: (抗倾覆安全系数, 是否满足要求)
        """
        # 倾覆力矩
        # 假设水平力作用点在基础顶面
        horizontal_load = self.static_load * 0.1
        overturning_moment = horizontal_load * (self.height + self.buried_depth - self.height)
        
        # 抗倾覆力矩
        # 自重作用线通过基础中心
        stabilizing_moment = self.self_weight * (self.length / 2)
        
        # 考虑静荷载偏心
        ex, ey = self.load_eccentricity
        if abs(ex) < self.length / 2:  # 确保偏心距在基础范围内
            stabilizing_moment += self.static_load * (self.length / 2 - abs(ex))
        
        # 抗倾覆安全系数
        safety_factor = stabilizing_moment / overturning_moment if overturning_moment > 0 else float('inf')
        
        # 安全系数应大于1.5
        is_safe = safety_factor >= 1.5
        
        return safety_factor, is_safe
    
    def bearing_capacity(self):
        """
        计算地基承载力验算
        
        返回:
        tuple: (地基压力, 最大允许承载力, 是否满足要求)
        """
        # 总荷载
        total_load = self.self_weight + self.static_load
        
        # 基础底面积
        base_area = self.length * self.width
        
        # 计算偏心距影响下的有效面积
        ex, ey = self.load_eccentricity
        effective_length = self.length - 2 * abs(ex)
        effective_width = self.width - 2 * abs(ey)
        effective_area = effective_length * effective_width
        
        # 实际地基压力
        actual_pressure = total_load / effective_area if effective_area > 0 else float('inf')
        
        # 是否满足要求
        is_safe = actual_pressure <= self.soil_bearing_capacity
        
        return actual_pressure, self.soil_bearing_capacity, is_safe
    
    def run_analysis(self):
        """
        运行完整的静力分析
        
        返回:
        dict: 计算结果
        """
        sliding_factor, sliding_safe = self.sliding_stability()
        overturning_factor, overturning_safe = self.overturning_stability()
        actual_pressure, allowable_pressure, bearing_safe = self.bearing_capacity()
        
        results = {
            "self_weight": self.self_weight,
            "total_weight": self.self_weight + self.static_load,
            "sliding_stability": {
                "safety_factor": sliding_factor,
                "is_safe": sliding_safe,
                "required_factor": 1.3
            },
            "overturning_stability": {
                "safety_factor": overturning_factor,
                "is_safe": overturning_safe,
                "required_factor": 1.5
            },
            "bearing_capacity": {
                "actual_pressure": actual_pressure,
                "allowable_pressure": allowable_pressure,
                "is_safe": bearing_safe
            },
            "overall_safety": sliding_safe and overturning_safe and bearing_safe
        }
        
        return results 