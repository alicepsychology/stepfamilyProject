#!/bin/bash

# run_analysis.sh
# 按照顺序执行整个数据分析流程

# 设置 -e 选项，如果任何命令返回非零退出状态，则立即退出脚本
set -e

echo "========================================="
echo "===   开始执行继家庭关系数据分析流程   ==="
echo "========================================="
echo

# 步骤 1: 数据预处理
echo "--- 步骤 1: 执行数据预处理脚本 ---"
python3 scripts/01_preprocess_data.py
echo "--- 数据预处理完成 ---"
echo

# 步骤 2: 相关性分析
echo "--- 步骤 2: 执行相关性分析脚本 ---"
python3 scripts/02_correlation_analysis.py
echo "--- 相关性分析完成 ---"
echo

# 步骤 3: 结果可视化
echo "--- 步骤 3: 执行结果可视化脚本 ---"
python3 scripts/03_visualize_results.py
echo "--- 结果可视化完成 ---"
echo

echo "========================================"
echo "===   所有分析流程已成功执行！        ==="
echo "===   请查看 'output' 文件夹获取结果。  ==="
echo "========================================" 