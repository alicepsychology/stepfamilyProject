# 继子女关系研究数据分析项目

## 项目概述

本项目对继子女与继父母、生父母关系的研究数据进行深入的相关性分析。研究数据来源于一项关于继子女在继家庭中的关系质量及其对心理健康影响的调查研究。

### 研究背景
- **研究对象**: 230名继子女参与者
- **数据维度**: 366个变量，涵盖人口统计学信息、关系质量评估、心理健康指标等
- **研究目标**: 分析继子女与继父母、生父母的关系质量变化，以及这些关系对心理健康的影响

## 项目结构

```
stepfamilyProject/
├── assets/
│   └── data.xlsx                    # 原始调查数据
├── scripts/
│   ├── 01_preprocess_data.py        # 数据预处理脚本
│   ├── 02_correlation_analysis.py   # 相关性分析脚本
│   ├── 03_visualize_results.py      # 结果可视化脚本
│   └── run_analysis.sh              # 自动化执行脚本
├── output/
│   ├── processed_data.csv           # 预处理后的数据
│   ├── correlation_matrix.csv       # 相关性矩阵
│   ├── correlation_report.txt       # 相关性分析报告
│   ├── correlation_heatmap.png      # 相关性热力图
│   └── scatter_*.png               # 各种散点图
├── .gitignore                       # Git忽略文件配置
└── README.md                        # 项目说明文档（本文件）
```

## 数据结构说明

### 原始数据特征
- **参与者数量**: 230人
- **变量总数**: 366个
- **数据格式**: Excel文件，包含中文问卷回答

### 关键变量类别

#### 1. 人口统计学变量
- `demo_age`: 参与者年龄
- `demo_cohab_duration`: 与继父母同居时长
- `demo_start_age_cohab`: 开始与继父母同居时的年龄

#### 2. 关系质量评估
- **继父母关系** (28个维度):
  - `rel_stepparent_past`: 过去的继父母关系质量
  - `rel_stepparent_current`: 当前的继父母关系质量
- **生父母关系** (16个维度):
  - `rel_bioparent_past`: 过去的生父母关系质量
  - `rel_bioparent_current`: 当前的生父母关系质量

#### 3. 心理健康指标
- `mental_self_esteem`: 自尊水平
- `mental_anxiety`: 焦虑水平
- `mental_depression`: 抑郁水平

## 代码结构详解

### 1. 数据预处理 (`01_preprocess_data.py`)

**主要功能**:
- 加载原始Excel数据
- 将中文李克特量表回答转换为数值
- 处理反向计分题目
- 计算各维度的复合得分
- 清理人口统计学数据

**核心处理逻辑**:
```python
# 李克特量表映射
likert_mapping = {
    "几乎从不或从不": 1,
    "很少如此": 2, 
    "有时如此": 3,
    "经常如此": 4,
    "几乎总是或总是": 5
}

# 反向计分处理
def reverse_score_items(df, columns, scale_max=5):
    for col in columns:
        df[col] = (scale_max + 1) - df[col]
```

**输出**: `processed_data.csv` - 包含230行×10列的清洁数据

### 2. 相关性分析 (`02_correlation_analysis.py`)

**主要功能**:
- 计算所有变量间的皮尔逊相关系数
- 生成相关性矩阵
- 输出格式化的分析报告

**分析方法**:
```python
# 计算皮尔逊相关系数
corr_matrix = df.corr(method='pearson')
```

**输出文件**:
- `correlation_matrix.csv`: 数值格式的相关性矩阵
- `correlation_report.txt`: 可读性强的英文分析报告

### 3. 结果可视化 (`03_visualize_results.py`)

**主要功能**:
- 创建相关性热力图
- 生成关键变量的散点图
- 添加回归拟合线

**可视化类型**:
1. **相关性热力图**: 展示所有变量间的相关强度
2. **散点图系列**:
   - 当前继父母关系 vs 抑郁水平
   - 当前继父母关系 vs 焦虑水平  
   - 当前继父母关系 vs 自尊水平
   - 同居开始年龄 vs 当前继父母关系

### 4. 自动化执行 (`run_analysis.sh`)

**功能**: 按顺序执行所有分析脚本
```bash
#!/bin/bash
echo "开始执行继子女关系数据分析..."
python scripts/01_preprocess_data.py
python scripts/02_correlation_analysis.py  
python scripts/03_visualize_results.py
echo "分析完成！"
```

## 技术实现细节

### 数据处理挑战与解决方案

1. **中文文本转数值问题**
   - **问题**: 原始数据包含中文李克特量表回答
   - **解决**: 创建映射字典，将文本转换为1-5数值

2. **反向计分题处理**
   - **问题**: 部分题目需要反向计分
   - **解决**: 使用公式 `new_score = (scale_max + 1) - old_score`

3. **人口统计学数据清理**
   - **问题**: 年龄和时长数据包含范围格式（如"1-3年"）
   - **解决**: 使用正则表达式提取并计算平均值

4. **中文字体显示问题**
   - **问题**: 图表中文标签显示异常
   - **解决**: 将所有输出标签转换为英文

### 依赖库
- `pandas`: 数据处理和分析
- `numpy`: 数值计算
- `seaborn`: 统计图表绘制
- `matplotlib`: 基础图表功能
- `openpyxl`: Excel文件读取

## 运行说明

### 环境要求
- Python 3.7+
- 已安装必要的Python包

### 执行步骤

1. **单步执行**:
```bash
# 数据预处理
python scripts/01_preprocess_data.py

# 相关性分析  
python scripts/02_correlation_analysis.py

# 结果可视化
python scripts/03_visualize_results.py
```

2. **一键执行**:
```bash
bash scripts/run_analysis.sh
```

## 分析结果说明

### 输出文件解读

1. **processed_data.csv**: 
   - 230行参与者数据
   - 10个关键变量的数值化结果
   - 可直接用于后续统计分析

2. **correlation_matrix.csv**:
   - 10×10的相关系数矩阵
   - 数值范围：-1到+1
   - 可导入其他统计软件进一步分析

3. **correlation_report.txt**:
   - 英文格式的相关性分析报告
   - 包含相关系数解释说明
   - 便于非技术人员理解

4. **可视化图表**:
   - `correlation_heatmap.png`: 直观展示变量间相关强度
   - `scatter_*.png`: 关键关系的散点图，包含趋势线

### 关键发现指标

通过相关性分析，可以重点关注以下关系：
- 继父母关系质量与心理健康指标的相关性
- 生父母关系质量的变化模式
- 同居开始年龄对关系发展的影响
- 不同关系质量间的相互影响

## 后续扩展建议

1. **统计检验**: 添加相关系数的显著性检验
2. **回归分析**: 构建多元回归模型预测心理健康结果
3. **分组分析**: 按年龄、性别等进行分层分析
4. **时间序列**: 分析关系质量的变化趋势
5. **交互效应**: 探索变量间的交互作用

## 注意事项

- 所有个人信息已匿名化处理
- 分析结果仅供学术研究使用
- 数据解释需结合专业心理学知识
- 相关性不等于因果关系

---

**项目维护者**: [您的姓名]  
**最后更新**: [当前日期]  
**联系方式**: [您的联系方式]
