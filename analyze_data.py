#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

def analyze_stepfamily_data():
    """分析继家庭研究数据"""
    
    # 读取Excel文件
    print("正在读取数据文件...")
    df = pd.read_excel('assets/data.xlsx')
    
    print(f"\n=== 数据文件基本信息 ===")
    print(f"数据形状: {df.shape}")
    print(f"总行数: {df.shape[0]} (参与者)")
    print(f"总列数: {df.shape[1]} (问题/变量)")
    
    print(f"\n=== 所有列名 ===")
    for i, col in enumerate(df.columns, 1):
        print(f"{i:3d}. {col}")
    
    # 保存列名到文件
    with open('column_names.txt', 'w', encoding='utf-8') as f:
        f.write("继家庭研究数据 - 列名清单\n")
        f.write("="*50 + "\n\n")
        f.write(f"数据形状: {df.shape}\n")
        f.write(f"总行数: {df.shape[0]} (参与者)\n")
        f.write(f"总列数: {df.shape[1]} (问题/变量)\n\n")
        
        for i, col in enumerate(df.columns, 1):
            f.write(f"{i:3d}. {col}\n")
    
    print(f"\n列名已保存到 column_names.txt 文件")
    
    # 显示前几行数据的概览
    print(f"\n=== 数据前5行概览 ===")
    print(df.head())
    
    return df

if __name__ == "__main__":
    df = analyze_stepfamily_data() 