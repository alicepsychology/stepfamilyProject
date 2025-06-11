#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
继家庭关系研究数据分析主程序
作者: AI助手
日期: 2024
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class StepfamilyDataAnalyzer:
    """继家庭数据分析器"""
    
    def __init__(self, data_path='assets/data.xlsx', output_dir='output'):
        """
        初始化分析器
        
        Args:
            data_path: 数据文件路径
            output_dir: 输出目录
        """
        self.data_path = data_path
        self.output_dir = output_dir
        self.df = None
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 创建时间戳用于文件命名
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def load_data(self):
        """加载数据"""
        print("正在加载数据...")
        try:
            self.df = pd.read_excel(self.data_path)
            print(f"数据加载成功！形状: {self.df.shape}")
            return True
        except Exception as e:
            print(f"数据加载失败: {e}")
            return False
    
    def generate_column_overview(self):
        """生成列概览文档"""
        if self.df is None:
            print("请先加载数据")
            return
        
        output_file = os.path.join(self.output_dir, f'column_overview_{self.timestamp}.txt')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("继家庭研究数据 - 列概览\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"数据文件: {self.data_path}\n")
            f.write(f"数据形状: {self.df.shape}\n")
            f.write(f"总参与者数: {self.df.shape[0]}\n")
            f.write(f"总变量数: {self.df.shape[1]}\n\n")
            
            # 按类别分组列名
            f.write("=" * 50 + "\n")
            f.write("列名分类概览\n")
            f.write("=" * 50 + "\n\n")
            
            # 基本信息类
            f.write("【基本信息类】\n")
            basic_cols = []
            for i, col in enumerate(self.df.columns):
                if any(keyword in col for keyword in ['序号', '时间', '来源', 'IP', '电话', '性别', '年龄', '教育']):
                    basic_cols.append(f"{i+1:3d}. {col}")
            for col in basic_cols[:10]:  # 限制显示数量
                f.write(f"  {col}\n")
            if len(basic_cols) > 10:
                f.write(f"  ... 还有 {len(basic_cols)-10} 个基本信息列\n")
            f.write("\n")
            
            # 继父母关系评估类
            f.write("【继父母关系评估类】\n")
            stepparent_cols = []
            for i, col in enumerate(self.df.columns):
                if any(keyword in col for keyword in ['继父', '继母', '我未满18岁时的感受', '我现在的感受']):
                    stepparent_cols.append(f"{i+1:3d}. {col}")
            for col in stepparent_cols[:15]:  # 显示前15个
                f.write(f"  {col}\n")
            if len(stepparent_cols) > 15:
                f.write(f"  ... 还有 {len(stepparent_cols)-15} 个继父母关系评估列\n")
            f.write("\n")
            
            # 心理健康评估类
            f.write("【心理健康评估类】\n")
            mental_health_cols = []
            for i, col in enumerate(self.df.columns):
                if any(keyword in col for keyword in ['自己感到满意', '一无是处', '优点', '失败者', '积极态度']):
                    mental_health_cols.append(f"{i+1:3d}. {col}")
            for col in mental_health_cols:
                f.write(f"  {col}\n")
            f.write("\n")
            
            # 创伤经历类
            f.write("【创伤经历类】\n")
            trauma_cols = []
            for i, col in enumerate(self.df.columns):
                if any(keyword in col for keyword in ['打击', '拳打', '脚踢', '烧灼', '受伤', '性经历']):
                    trauma_cols.append(f"{i+1:3d}. {col}")
            for col in trauma_cols:
                f.write(f"  {col}\n")
            f.write("\n")
            
            # 完整列名列表
            f.write("=" * 50 + "\n")
            f.write("完整列名列表\n")
            f.write("=" * 50 + "\n\n")
            
            for i, col in enumerate(self.df.columns, 1):
                f.write(f"{i:3d}. {col}\n")
        
        print(f"列概览已保存到: {output_file}")
        return output_file
    
    def basic_statistics(self):
        """生成基本统计信息"""
        if self.df is None:
            print("请先加载数据")
            return
        
        output_file = os.path.join(self.output_dir, f'basic_statistics_{self.timestamp}.txt')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("继家庭研究数据 - 基本统计信息\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # 数据基本信息
            f.write("【数据基本信息】\n")
            f.write(f"总参与者数: {self.df.shape[0]}\n")
            f.write(f"总变量数: {self.df.shape[1]}\n")
            f.write(f"缺失值总数: {self.df.isnull().sum().sum()}\n")
            f.write(f"缺失值比例: {self.df.isnull().sum().sum() / (self.df.shape[0] * self.df.shape[1]) * 100:.2f}%\n\n")
            
            # 数值型变量统计
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                f.write("【数值型变量统计】\n")
                f.write(f"数值型变量数量: {len(numeric_cols)}\n")
                f.write("主要统计量:\n")
                f.write(str(self.df[numeric_cols].describe()))
                f.write("\n\n")
        
        print(f"基本统计信息已保存到: {output_file}")
        return output_file
    
    def run_analysis(self):
        """运行完整分析"""
        print("开始继家庭关系研究数据分析...")
        print("=" * 50)
        
        # 加载数据
        if not self.load_data():
            return
        
        # 生成分析报告
        print("\n1. 生成列概览...")
        self.generate_column_overview()
        
        print("\n2. 生成基本统计信息...")
        self.basic_statistics()
        
        print("\n分析完成！所有输出文件已保存到 output/ 目录")
        print("=" * 50)

def main():
    """主函数"""
    analyzer = StepfamilyDataAnalyzer()
    analyzer.run_analysis()

if __name__ == "__main__":
    main()
