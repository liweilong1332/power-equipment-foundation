#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
动力分析模块 - 用于计算大块式设备基础的动力参数
包括：振动响应、传递率计算等
"""

import numpy as np
from scipy import signal


class DynamicAnalysis:
    """动力分析类"""
    
    def __init__(self, length, width, height, buried_depth,
                 concrete_strength, elastic_modulus, soil_coefficient,
                 dynamic_load, frequency, total_mass, damping_ratio=0.05):
        """
        初始化动力分析参数
        
        参数:
        length (float): 基础长度(m)
        width (float): 基础宽度(m)
        height (float): 基础高度(m)
        buried_depth (float): 埋深(m)
        concrete_strength (float): 混凝土强度(MPa)
        elastic_modulus (float): 弹性模量(MPa)
        soil_coefficient (float): 地基系数(kN/m³)
        dynamic_load (float): 动力荷载幅值(kN)
        frequency (float): 动力荷载频率(Hz)
        total_mass (float): 总质量(kg) - 包括设备和基础
        damping_ratio (float): 阻尼比
        """
        self.length = length
        self.width = width
        self.height = height
        self.buried_depth = buried_depth
        self.concrete_strength = concrete_strength
        self.elastic_modulus = elastic_modulus * 1000  # 转换为kPa
        self.soil_coefficient = soil_coefficient
        self.dynamic_load = dynamic_load
        self.frequency = frequency
        self.total_mass = total_mass
        self.damping_ratio = damping_ratio
        
        # 计算固有参数
        self.spring_constant = self.calculate_spring_constant()
        self.natural_frequency = self.calculate_natural_frequency()
        
    def calculate_spring_constant(self):
        """
        计算地基弹簧刚度(kN/m)
        
        返回:
        float: 等效弹簧刚度
        """
        # 基础底面积
        base_area = self.length * self.width
        
        # 等效弹簧刚度 k = C_s * A
        # 其中 C_s 为地基系数，A 为接触面积
        k = self.soil_coefficient * base_area
        
        return k
    
    def calculate_natural_frequency(self):
        """
        计算系统自然频率(Hz)
        
        返回:
        float: 自然频率
        """
        # ω² = k/m
        # f = ω/(2π)
        omega_squared = self.spring_constant / self.total_mass
        natural_freq = np.sqrt(omega_squared) / (2 * np.pi)
        
        return natural_freq
    
    def calculate_frequency_ratio(self):
        """
        计算频率比
        
        返回:
        float: 频率比 (激励频率/自然频率)
        """
        return self.frequency / self.natural_frequency if self.natural_frequency > 0 else float('inf')
    
    def calculate_transmissibility(self):
        """
        计算振动传递率
        
        返回:
        float: 振动传递率
        """
        r = self.calculate_frequency_ratio()
        zeta = self.damping_ratio
        
        # 计算传递率
        if r == 0:
            return 1.0
        
        numerator = np.sqrt(1 + (2 * zeta * r)**2)
        denominator = np.sqrt((1 - r**2)**2 + (2 * zeta * r)**2)
        
        tr = numerator / denominator
        
        return tr
    
    def calculate_amplitude(self):
        """
        计算振动幅值
        
        返回:
        float: 振动幅值(mm)
        """
        r = self.calculate_frequency_ratio()
        zeta = self.damping_ratio
        
        # 力传递函数
        if r == 0:
            force_tf = 1.0
        else:
            force_tf = 1 / np.sqrt((1 - r**2)**2 + (2 * zeta * r)**2)
        
        # 振动幅值 (F0/k) * 力传递函数
        static_deflection = self.dynamic_load / self.spring_constant
        amplitude = static_deflection * force_tf
        
        # 转换为mm
        amplitude_mm = amplitude * 1000
        
        return amplitude_mm
    
    def is_resonance_risk(self):
        """
        判断是否存在共振风险
        
        返回:
        tuple: (是否存在共振风险, 频率比)
        """
        r = self.calculate_frequency_ratio()
        
        # 一般认为频率比在0.8-1.2之间存在共振风险
        is_risk = 0.8 <= r <= 1.2
        
        return is_risk, r
    
    def calculate_response_curve(self, freq_range=None):
        """
        计算响应曲线
        
        参数:
        freq_range (tuple): 频率范围(Hz)，默认为0.1到自然频率的3倍
        
        返回:
        tuple: (频率数组, 幅值数组)
        """
        if freq_range is None:
            start_freq = 0.1
            end_freq = self.natural_frequency * 3
            if end_freq <= start_freq:
                end_freq = start_freq + 50
        else:
            start_freq, end_freq = freq_range
        
        # 创建频率数组
        frequencies = np.linspace(start_freq, end_freq, 1000)
        amplitudes = []
        
        # 保存当前频率
        original_freq = self.frequency
        
        # 计算每个频率下的幅值
        for freq in frequencies:
            self.frequency = freq
            amplitudes.append(self.calculate_amplitude())
        
        # 恢复原始频率
        self.frequency = original_freq
        
        return frequencies, np.array(amplitudes)
    
    def run_analysis(self):
        """
        运行完整的动力分析
        
        返回:
        dict: 计算结果
        """
        freq_ratio = self.calculate_frequency_ratio()
        transmissibility = self.calculate_transmissibility()
        amplitude = self.calculate_amplitude()
        resonance_risk, _ = self.is_resonance_risk()
        
        # 振动容许值 (根据GB 50040-2020)
        allowable_amplitude = 0.15  # mm (假设为0.15mm，实际应按设备要求确定)
        is_safe = amplitude <= allowable_amplitude
        
        results = {
            "natural_frequency": self.natural_frequency,
            "frequency_ratio": freq_ratio,
            "transmissibility": transmissibility,
            "amplitude": amplitude,
            "allowable_amplitude": allowable_amplitude,
            "is_safe": is_safe,
            "resonance_risk": resonance_risk
        }
        
        return results 