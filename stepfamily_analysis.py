#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
继家庭关系研究 - 继子女对继父母vs生身父母看法分析
研究问题：继子女在过去和现在对继父母和亲生父母是否有不同看法？
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
from datetime import datetime

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class StepfamilyRelationshipAnalyzer:
    """继家庭关系分析器"""
    
    def __init__(self, data_path='assets/data.xlsx', output_dir='output'):
        self.data_path = data_path
        self.output_dir = output_dir
        self.df = None
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 定义关键列索引（基于column_names.txt）
        self.define_column_groups()
    
    def define_column_groups(self):
        """定义各类变量的列索引"""
        
        # 基本信息
        self.basic_info = {
            'gender': 9,  # 性别
            'age': 10,    # 年龄
            'stepparent_count': 11,  # 继父母数量
            'stepparent_gender': 12, # 继父母性别
            'cohabitation_duration': 13, # 同住时长
            'start_age': 15,  # 开始同住年龄
            'education': 23   # 教育水平
        }
        
        # 继父母关系评估 - 过去 (18岁前)
        self.stepparent_past = list(range(24, 52))  # 列25-52
        
        # 继父母关系评估 - 现在
        self.stepparent_current = list(range(52, 80))  # 列53-80
        
        # 生身父母关系评估 - 过去
        self.bioparent_past = list(range(136, 152))  # 列137-152
        
        # 生身父母关系评估 - 现在  
        self.bioparent_current = list(range(152, 168))  # 列153-168
        
        # 创伤经历
        self.trauma = {
            'stepparent_abuse': list(range(201, 207)),  # 继父母施暴
            'bioparent_abuse': list(range(207, 213)),   # 生身父母施暴
            'stepparent_sexual': 213,  # 继父母性侵
            'bioparent_sexual': 214    # 生身父母性侵
        }
        
        # 心理健康
        self.mental_health = {
            'self_esteem': list(range(215, 225)),      # 自尊
            'self_blame': list(range(225, 232)),       # 自责
            'anxiety': list(range(261, 268)),          # 焦虑
            'depression': list(range(268, 277))        # 抑郁
        }
    
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
    
    def calculate_relationship_scores(self):
        """计算关系质量得分"""
        print("计算关系质量得分...")
        
        # 获取列名
        cols = self.df.columns
        
        # 计算继父母关系得分
        stepparent_past_cols = [cols[i] for i in self.stepparent_past if i < len(cols)]
        stepparent_current_cols = [cols[i] for i in self.stepparent_current if i < len(cols)]
        
        # 计算生身父母关系得分
        bioparent_past_cols = [cols[i] for i in self.bioparent_past if i < len(cols)]
        bioparent_current_cols = [cols[i] for i in self.bioparent_current if i < len(cols)]
        
        # 计算平均得分（需要处理反向计分题）
        self.df['stepparent_past_score'] = self.df[stepparent_past_cols].mean(axis=1, skipna=True)
        self.df['stepparent_current_score'] = self.df[stepparent_current_cols].mean(axis=1, skipna=True)
        self.df['bioparent_past_score'] = self.df[bioparent_past_cols].mean(axis=1, skipna=True)
        self.df['bioparent_current_score'] = self.df[bioparent_current_cols].mean(axis=1, skipna=True)
        
        # 计算变化得分
        self.df['stepparent_change'] = self.df['stepparent_current_score'] - self.df['stepparent_past_score']
        self.df['bioparent_change'] = self.df['bioparent_current_score'] - self.df['bioparent_past_score']
        
        print("关系质量得分计算完成")
    
    def descriptive_analysis(self):
        """描述性统计分析"""
        print("进行描述性统计分析...")
        
        output_file = os.path.join(self.output_dir, f'relationship_descriptive_{self.timestamp}.txt')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("继家庭关系研究 - 描述性统计分析\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # 基本信息统计
            f.write("【基本信息统计】\n")
            f.write(f"总参与者数: {len(self.df)}\n")
            
            # 性别分布
            if self.df.columns[self.basic_info['gender']] in self.df.columns:
                gender_col = self.df.columns[self.basic_info['gender']]
                gender_dist = self.df[gender_col].value_counts()
                f.write(f"\n性别分布:\n{gender_dist}\n")
            
            # 年龄分布
            if self.df.columns[self.basic_info['age']] in self.df.columns:
                age_col = self.df.columns[self.basic_info['age']]
                f.write(f"\n年龄统计:\n{self.df[age_col].describe()}\n")
            
            # 关系质量得分统计
            f.write("\n【关系质量得分统计】\n")
            relationship_scores = ['stepparent_past_score', 'stepparent_current_score', 
                                 'bioparent_past_score', 'bioparent_current_score']
            
            for score in relationship_scores:
                if score in self.df.columns:
                    f.write(f"\n{score}:\n{self.df[score].describe()}\n")
            
            # 关系质量变化
            f.write("\n【关系质量变化】\n")
            if 'stepparent_change' in self.df.columns:
                f.write(f"继父母关系变化:\n{self.df['stepparent_change'].describe()}\n")
            if 'bioparent_change' in self.df.columns:
                f.write(f"生身父母关系变化:\n{self.df['bioparent_change'].describe()}\n")
        
        print(f"描述性统计分析已保存到: {output_file}")
        return output_file
    
    def comparative_analysis(self):
        """对比分析：继父母vs生身父母"""
        print("进行对比分析...")
        
        output_file = os.path.join(self.output_dir, f'relationship_comparison_{self.timestamp}.txt')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("继家庭关系研究 - 继父母vs生身父母对比分析\n")
            f.write("=" * 60 + "\n\n")
            
            # 1. 过去时期对比
            f.write("【过去时期（18岁前）关系质量对比】\n")
            if all(col in self.df.columns for col in ['stepparent_past_score', 'bioparent_past_score']):
                # 配对t检验
                past_data = self.df[['stepparent_past_score', 'bioparent_past_score']].dropna()
                if len(past_data) > 0:
                    t_stat, p_value = stats.ttest_rel(past_data['stepparent_past_score'], 
                                                    past_data['bioparent_past_score'])
                    
                    f.write(f"继父母关系得分均值: {past_data['stepparent_past_score'].mean():.3f}\n")
                    f.write(f"生身父母关系得分均值: {past_data['bioparent_past_score'].mean():.3f}\n")
                    f.write(f"配对t检验: t={t_stat:.3f}, p={p_value:.3f}\n")
                    f.write(f"显著性: {'显著' if p_value < 0.05 else '不显著'}\n\n")
            
            # 2. 现在时期对比
            f.write("【现在时期关系质量对比】\n")
            if all(col in self.df.columns for col in ['stepparent_current_score', 'bioparent_current_score']):
                current_data = self.df[['stepparent_current_score', 'bioparent_current_score']].dropna()
                if len(current_data) > 0:
                    t_stat, p_value = stats.ttest_rel(current_data['stepparent_current_score'], 
                                                    current_data['bioparent_current_score'])
                    
                    f.write(f"继父母关系得分均值: {current_data['stepparent_current_score'].mean():.3f}\n")
                    f.write(f"生身父母关系得分均值: {current_data['bioparent_current_score'].mean():.3f}\n")
                    f.write(f"配对t检验: t={t_stat:.3f}, p={p_value:.3f}\n")
                    f.write(f"显著性: {'显著' if p_value < 0.05 else '不显著'}\n\n")
            
            # 3. 时间变化对比
            f.write("【时间变化对比】\n")
            if all(col in self.df.columns for col in ['stepparent_change', 'bioparent_change']):
                change_data = self.df[['stepparent_change', 'bioparent_change']].dropna()
                if len(change_data) > 0:
                    t_stat, p_value = stats.ttest_rel(change_data['stepparent_change'], 
                                                    change_data['bioparent_change'])
                    
                    f.write(f"继父母关系变化均值: {change_data['stepparent_change'].mean():.3f}\n")
                    f.write(f"生身父母关系变化均值: {change_data['bioparent_change'].mean():.3f}\n")
                    f.write(f"配对t检验: t={t_stat:.3f}, p={p_value:.3f}\n")
                    f.write(f"显著性: {'显著' if p_value < 0.05 else '不显著'}\n\n")
        
        print(f"对比分析已保存到: {output_file}")
        return output_file
    
    def create_visualizations(self):
        """创建可视化图表"""
        print("创建可视化图表...")
        
        # 设置图表样式
        plt.style.use('default')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('继家庭关系质量分析', fontsize=16, fontweight='bold')
        
        # 1. 关系质量得分对比（箱线图）
        if all(col in self.df.columns for col in ['stepparent_past_score', 'stepparent_current_score', 
                                                 'bioparent_past_score', 'bioparent_current_score']):
            
            # 准备数据
            plot_data = []
            labels = []
            
            for col, label in [('stepparent_past_score', '继父母-过去'),
                              ('stepparent_current_score', '继父母-现在'),
                              ('bioparent_past_score', '生身父母-过去'),
                              ('bioparent_current_score', '生身父母-现在')]:
                if col in self.df.columns:
                    plot_data.append(self.df[col].dropna())
                    labels.append(label)
            
            axes[0,0].boxplot(plot_data, labels=labels)
            axes[0,0].set_title('关系质量得分对比')
            axes[0,0].set_ylabel('关系质量得分')
            axes[0,0].tick_params(axis='x', rotation=45)
        
        # 2. 关系质量变化对比
        if all(col in self.df.columns for col in ['stepparent_change', 'bioparent_change']):
            change_data = [self.df['stepparent_change'].dropna(), 
                          self.df['bioparent_change'].dropna()]
            axes[0,1].boxplot(change_data, labels=['继父母关系变化', '生身父母关系变化'])
            axes[0,1].set_title('关系质量变化对比')
            axes[0,1].set_ylabel('变化得分')
            axes[0,1].axhline(y=0, color='red', linestyle='--', alpha=0.7)
        
        # 3. 散点图：过去vs现在关系质量
        if all(col in self.df.columns for col in ['stepparent_past_score', 'stepparent_current_score']):
            axes[1,0].scatter(self.df['stepparent_past_score'], self.df['stepparent_current_score'], 
                            alpha=0.6, label='继父母关系')
            
        if all(col in self.df.columns for col in ['bioparent_past_score', 'bioparent_current_score']):
            axes[1,0].scatter(self.df['bioparent_past_score'], self.df['bioparent_current_score'], 
                            alpha=0.6, label='生身父母关系')
            
        axes[1,0].plot([1, 5], [1, 5], 'r--', alpha=0.7, label='无变化线')
        axes[1,0].set_xlabel('过去关系质量')
        axes[1,0].set_ylabel('现在关系质量')
        axes[1,0].set_title('关系质量：过去vs现在')
        axes[1,0].legend()
        
        # 4. 关系质量分布直方图
        if 'stepparent_current_score' in self.df.columns and 'bioparent_current_score' in self.df.columns:
            axes[1,1].hist(self.df['stepparent_current_score'].dropna(), alpha=0.7, 
                          label='继父母关系', bins=20)
            axes[1,1].hist(self.df['bioparent_current_score'].dropna(), alpha=0.7, 
                          label='生身父母关系', bins=20)
            axes[1,1].set_xlabel('关系质量得分')
            axes[1,1].set_ylabel('频数')
            axes[1,1].set_title('当前关系质量分布')
            axes[1,1].legend()
        
        plt.tight_layout()
        
        # 保存图表
        plot_file = os.path.join(self.output_dir, f'relationship_plots_{self.timestamp}.png')
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"可视化图表已保存到: {plot_file}")
        return plot_file
    
    def run_complete_analysis(self):
        """运行完整分析"""
        print("开始继家庭关系完整分析...")
        print("=" * 60)
        
        # 1. 加载数据
        if not self.load_data():
            return
        
        # 2. 计算关系质量得分
        self.calculate_relationship_scores()
        
        # 3. 描述性统计
        desc_file = self.descriptive_analysis()
        
        # 4. 对比分析
        comp_file = self.comparative_analysis()
        
        # 5. 可视化
        plot_file = self.create_visualizations()
        
        # 6. 生成总结报告
        self.generate_summary_report([desc_file, comp_file, plot_file])
        
        print("\n分析完成！所有输出文件已保存到 output/ 目录")
        print("=" * 60)
    
    def generate_summary_report(self, file_list):
        """生成总结报告"""
        summary_file = os.path.join(self.output_dir, f'analysis_summary_{self.timestamp}.txt')
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("继家庭关系研究 - 分析总结报告\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("【研究问题】\n")
            f.write("继子女在过去和现在对继父母和生身父母是否有不同看法？\n\n")
            
            f.write("【数据概况】\n")
            f.write(f"参与者数量: {len(self.df)}\n")
            f.write(f"变量数量: {len(self.df.columns)}\n\n")
            
            f.write("【主要发现】\n")
            f.write("1. 时间维度分析：比较了18岁前和现在的关系质量\n")
            f.write("2. 父母类型对比：比较了继父母和生身父母的关系质量\n")
            f.write("3. 变化趋势：分析了关系质量随时间的变化\n\n")
            
            f.write("【生成文件】\n")
            for i, file_path in enumerate(file_list, 1):
                f.write(f"{i}. {os.path.basename(file_path)}\n")
            
            f.write(f"\n【建议后续分析】\n")
            f.write("1. 影响因素分析：探索年龄、性别、同住时长等因素的影响\n")
            f.write("2. 创伤经历分析：分析暴力或性侵经历对关系质量的影响\n")
            f.write("3. 心理健康关联：分析关系质量与心理健康指标的关系\n")
            f.write("4. 聚类分析：识别不同的关系模式类型\n")
        
        print(f"总结报告已保存到: {summary_file}")

def main():
    """主函数"""
    analyzer = StepfamilyRelationshipAnalyzer()
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main() 