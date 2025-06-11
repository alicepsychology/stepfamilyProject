#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02_correlation_analysis.py
- 加载预处理后的数据
- 计算关键变量之间的相关性矩阵
- 保存相关性矩阵为 CSV 和可读的 TXT 文件
"""

import pandas as pd
import os

def analyze_correlations(input_path='output/processed_data.csv', output_dir='output'):
    """
    执行相关性分析
    """
    print("--- 开始相关性分析 ---")

    # 1. 加载数据
    if not os.path.exists(input_path):
        print(f"错误: 未找到预处理后的数据文件 {input_path}")
        print("请先运行 01_preprocess_data.py")
        return
        
    print(f"加载预处理数据: {input_path}")
    df = pd.read_csv(input_path)

    # 2. 计算相关性矩阵
    print("计算相关性矩阵...")
    
    # 直接使用英文列名计算相关性
    corr_matrix = df.corr(method='pearson')

    # 3. 保存结果
    # a) 保存为 CSV 文件
    csv_path = os.path.join(output_dir, 'correlation_matrix.csv')
    print(f"保存相关性矩阵 (CSV) 到: {csv_path}")
    corr_matrix.to_csv(csv_path, encoding='utf-8-sig')

    # b) 保存为格式化的 TXT 报告
    report_path = os.path.join(output_dir, 'correlation_report.txt')
    print(f"保存格式化的相关性报告 (TXT) 到: {report_path}")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("Stepfamily Relationship Data - Correlation Analysis Report\n")
        f.write("=" * 50 + "\n\n")
        f.write("This report shows the Pearson correlation coefficient between key variables.\n")
        f.write("The correlation coefficient ranges from -1 to +1:\n")
        f.write("  - Close to +1 indicates a strong positive correlation\n")
        f.write("  - Close to -1 indicates a strong negative correlation\n")
        f.write("  - Close to 0 indicates no linear correlation\n\n")
        
        f.write(corr_matrix.to_string(float_format="%.3f"))
    
    print("--- 相关性分析完成 ---")
    return csv_path, report_path

if __name__ == "__main__":
    analyze_correlations() 