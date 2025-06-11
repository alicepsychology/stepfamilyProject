#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03_visualize_results.py
- 加载相关性矩阵和处理后的数据
- 创建并保存相关性热力图
- 创建并保存关键变量的散点图
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def visualize_results(matrix_path='output/correlation_matrix.csv', 
                      data_path='output/processed_data.csv', 
                      output_dir='output'):
    """
    执行结果可视化
    """
    print("--- 开始结果可视化 ---")

    # --- 1. 创建相关性热力图 ---
    if not os.path.exists(matrix_path):
        print(f"错误: 未找到相关性矩阵文件 {matrix_path}")
        print("请先运行 02_correlation_analysis.py")
        return

    print(f"加载相关性矩阵: {matrix_path}")
    corr_matrix = pd.read_csv(matrix_path, index_col=0)

    plt.figure(figsize=(12, 10))
    # Use 'coolwarm' colormap, centered at 0
    # annot=True will display values on the cells
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title('Correlation Heatmap of Key Variables', fontsize=16, pad=20)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    
    heatmap_path = os.path.join(output_dir, 'correlation_heatmap.png')
    print(f"保存热力图到: {heatmap_path}")
    plt.savefig(heatmap_path, dpi=300, bbox_inches='tight')
    plt.close()

    # --- 2. 创建关键散点图 ---
    if not os.path.exists(data_path):
        print(f"错误: 未找到预处理数据文件 {data_path}")
        return
        
    print(f"加载预处理数据进行散点图绘制: {data_path}")
    df = pd.read_csv(data_path)
    
    # Define scatter plots to generate
    scatter_plots = [
        ('rel_stepparent_current', 'mental_depression', 'Current Stepparent Relationship vs. Depression'),
        ('rel_stepparent_current', 'mental_anxiety', 'Current Stepparent Relationship vs. Anxiety'),
        ('rel_stepparent_current', 'mental_self_esteem', 'Current Stepparent Relationship vs. Self-Esteem'),
        ('demo_start_age_cohab', 'rel_stepparent_current', 'Cohabitation Start Age vs. Current Stepparent Relationship')
    ]

    print("生成并保存散点图...")
    for x_col, y_col, title in scatter_plots:
        plt.figure(figsize=(8, 6))
        # reg_line=True adds a linear regression fit line
        sns.regplot(x=x_col, y=y_col, data=df,
                    scatter_kws={'alpha':0.5},
                    line_kws={"color": "red"})
        plt.title(title, fontsize=14)
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        
        plot_path = os.path.join(output_dir, f'scatter_{x_col}_vs_{y_col}.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  - 已保存: {plot_path}")

    print("--- 结果可视化完成 ---")

if __name__ == "__main__":
    visualize_results() 