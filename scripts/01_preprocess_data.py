#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_preprocess_data.py
- 加载原始数据
- 将文本答案转换为数值
- 处理反向计分题
- 计算各量表综合得分
- 保存处理后的数据
"""

import pandas as pd
import numpy as np
import os
import re

def clean_demographic_column(series):
    """
    清洗包含年龄范围或文本的列，将其转换为数值。
    例如 '1-3年' -> 2, '小于1年' -> 0.5, '18' -> 18
    """
    def convert_value(val):
        if pd.isna(val):
            return np.nan
        
        # 如果已经是数字，直接返回
        if isinstance(val, (int, float)):
            return float(val)

        val_str = str(val)
        
        # 处理 "X-Y年" 格式
        match = re.search(r'(\d+)-(\d+)', val_str)
        if match:
            return (float(match.group(1)) + float(match.group(2))) / 2
        
        # 处理 "大于X年" 格式
        match = re.search(r'大于(\d+)', val_str)
        if match:
            return float(match.group(1)) + 5 # 假设一个开放区间的增量

        # 处理 "小于X年" 格式
        match = re.search(r'小于(\d+)', val_str)
        if match:
            return float(match.group(1)) / 2

        # 处理单个数字
        match = re.search(r'(\d+)', val_str)
        if match:
            return float(match.group(1))
            
        return np.nan # 如果没有匹配，返回NaN

    return series.apply(convert_value)

def preprocess_data(input_path='assets/data.xlsx', output_dir='output'):
    """
    执行完整的数据预处理流程
    """
    print("--- 开始数据预处理 ---")

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. 加载数据
    print(f"加载原始数据: {input_path}")
    df = pd.read_excel(input_path, header=0)
    print(f"原始数据形状: {df.shape}")

    # 2. 定义文本到数值的映射
    # 这是根据常见的李克特5点量表进行的假设，可能需要根据实际问卷调整
    likert_5_point_mapping = {
        '几乎从不或从不': 1,
        '很少如此': 2,
        '有时如此': 3,
        '通常如此': 4,
        '几乎总是或总是如此': 5
    }
    
    # 3. 定义需要处理的列和反向计分题
    # 列索引从0开始 (pandas iloc)
    
    # 关系质量 (继父母 - 过去)
    stepparent_past_cols = list(range(24, 52)) # 对应Excel列 Y(25) 到 AZ(52)
    # 反向题: 3, 5, 7, 9, 10, 11, 12, 15, 18, 19, 22, 25, 27
    stepparent_past_reverse = [2, 4, 6, 8, 9, 10, 11, 14, 17, 18, 21, 24, 26] 

    # 关系质量 (继父母 - 现在)
    stepparent_current_cols = list(range(52, 80))
    # 假设反向题结构与过去相同
    stepparent_current_reverse = [2, 4, 6, 8, 9, 10, 11, 14, 17, 18, 21, 24, 26] 

    # 关系质量 (生身父母 - 过去)
    bioparent_past_cols = list(range(136, 152))
    # 反向题: 1, 4, 6, 7, 9, 10, 15, 16
    bioparent_past_reverse = [0, 3, 5, 6, 8, 9, 14, 15]

    # 关系质量 (生身父母 - 现在)
    bioparent_current_cols = list(range(152, 168))
    # 假设反向题结构与过去相同
    bioparent_current_reverse = [0, 3, 5, 6, 8, 9, 14, 15]

    # 自尊量表
    self_esteem_cols = list(range(215, 225))
    # 反向题: 2, 5, 6, 8, 9
    self_esteem_reverse = [1, 4, 5, 7, 8]

    # 焦虑 (GAD-7)
    anxiety_cols = list(range(261, 268))

    # 抑郁 (PHQ-9)
    depression_cols = list(range(268, 277))
    
    # --- 开始数据转换 ---
    
    all_scale_cols = (stepparent_past_cols + stepparent_current_cols +
                      bioparent_past_cols + bioparent_current_cols +
                      self_esteem_cols + anxiety_cols + depression_cols)
    
    # 获取唯一的列索引
    unique_cols_indices = sorted(list(set(all_scale_cols)))

    # 统一应用映射
    print("将文本答案转换为数值...")
    df_columns_to_process = df.iloc[:, unique_cols_indices].columns
    for col in df_columns_to_process:
        # 使用 .loc 避免 SettingWithCopyWarning
        df.loc[:, col] = df[col].map(likert_5_point_mapping).fillna(df[col])
        # 将无法映射的值（可能是数字）强制转换为数值，无效的设为NaN
        df.loc[:, col] = pd.to_numeric(df[col], errors='coerce')

    # 4. 处理反向计分题
    print("处理反向计分题...")
    def reverse_code(df, cols, reverse_indices, scale_max=5):
        for idx in reverse_indices:
            if idx < len(cols):
                col_name = df.columns[cols[idx]]
                print(f"  - 反向计分: {col_name}")
                df[col_name] = (scale_max + 1) - df[col_name]
    
    reverse_code(df, stepparent_past_cols, stepparent_past_reverse)
    reverse_code(df, stepparent_current_cols, stepparent_current_reverse)
    reverse_code(df, bioparent_past_cols, bioparent_past_reverse)
    reverse_code(df, bioparent_current_cols, bioparent_current_reverse)
    reverse_code(df, self_esteem_cols, self_esteem_reverse)

    # 5. 计算综合得分 (使用处理后的数值列)
    print("计算各量表综合得分...")
    def calculate_score(df, cols, new_col_name):
        col_names = [df.columns[i] for i in cols if i < len(df.columns)]
        df[new_col_name] = df[col_names].mean(axis=1, skipna=True)
        print(f"  - 已计算: {new_col_name}")

    calculate_score(df, stepparent_past_cols, 'rel_stepparent_past')
    calculate_score(df, stepparent_current_cols, 'rel_stepparent_current')
    calculate_score(df, bioparent_past_cols, 'rel_bioparent_past')
    calculate_score(df, bioparent_current_cols, 'rel_bioparent_current')
    calculate_score(df, self_esteem_cols, 'mental_self_esteem')
    calculate_score(df, anxiety_cols, 'mental_anxiety')
    calculate_score(df, depression_cols, 'mental_depression')

    # 提取关键人口学变量
    print("提取关键人口学变量...")
    
    # 使用 iloc 按精确的列位置索引，避免KeyError
    # 年龄 -> 第11列 (索引10)
    # 同住时长 -> 第14列 (索引13)
    # 开始同住年龄 -> 第16列 (索引15)
    df_processed = df.iloc[:, [10, 13, 15]].copy()
    
    # 为列重命名以提高可读性
    df_processed.columns = ['demo_age', 'demo_cohab_duration', 'demo_start_age_cohab']
    
    # 清洗新提取的人口学列
    print("清洗人口学数据...")
    for col in df_processed.columns:
        print(f"  - 清洗列: {col}")
        df_processed[col] = clean_demographic_column(df_processed[col])

    # 合并得分
    score_cols = [
        'rel_stepparent_past', 'rel_stepparent_current',
        'rel_bioparent_past', 'rel_bioparent_current',
        'mental_self_esteem', 'mental_anxiety', 'mental_depression'
    ]
    df_processed = pd.concat([df_processed, df[score_cols]], axis=1)

    # 6. 保存处理后的数据
    output_path = os.path.join(output_dir, 'processed_data.csv')
    print(f"保存处理后的数据到: {output_path}")
    df_processed.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"处理后的数据形状: {df_processed.shape}")
    print("--- 数据预处理完成 ---")
    return output_path

if __name__ == "__main__":
    preprocess_data() 