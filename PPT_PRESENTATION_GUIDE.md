# PPT演示制作详细指南

## 总体设计建议
- **主题色**：深蓝色/深灰色背景，白色/浅色文字（学术风格）
- **字体**：标题用Arial/Bold，正文用Arial Regular，字号至少18pt
- **布局**：简洁、专业，每页不超过7行要点
- **总页数**：建议12-15页（10-15分钟演示）

---

## 第1页：标题页 (Title Slide)

### 布局
- 居中布局
- 上半部分：标题
- 中间：副标题/作者信息
- 底部：日期、课程/项目信息

### 内容
**主标题**（大号，加粗）：
```
Bootstrap Analysis of Genre Impact 
on Regional Video Game Sales
```

**副标题**（中号）：
```
A Statistical Uncertainty Framework
```

**底部信息**（小号）：
```
MATH3110 Project
[你的名字] & [Ben的名字]
[日期]
```

### 设计元素
- 背景：深蓝色渐变或纯色
- 可添加：游戏手柄图标（可选，左上角或右下角小图标）

---

## 第2页：研究问题 (Research Question)

### 布局
- 左侧：问题陈述（60%宽度）
- 右侧：关键概念图标/示意图（40%宽度）

### 内容
**标题**：Research Question

**主要内容**：
```
Can we, with statistical confidence, conclude that 
certain video game genres systematically receive 
higher or lower average sales than others within 
specific regional markets?

Key Questions:
• Do regional preferences for genres differ significantly?
• Can we quantify the uncertainty around these differences?
• Which genres perform best in which regions?
```

**右侧示意图**：
- 世界地图轮廓，标注5个区域（Global, NA, EU, JP, Other）
- 或：三个游戏类型图标（Action, Role-Playing, Simulation）

---

## 第3页：研究目标 (Objectives)

### 布局
- 标题居中
- 3-4个目标，每个用图标+文字

### 内容
**标题**：Research Objectives

**目标列表**（带图标）：
```
1. 📊 Estimate 95% confidence intervals for genre means
   • 3 genres × 5 regions = 15 analyses
   • Bootstrap resampling (N=10,000)

2. 🔍 Compare pairwise differences between genres
   • 3 pairs × 5 regions = 15 comparisons
   • Statistical significance testing

3. 🌍 Identify regional patterns and preferences
   • Which genres perform best in each region?
   • Are differences statistically meaningful?

4. 📈 Provide uncertainty-aware decision support
   • Quantify sampling variability
   • Robust to non-normal distributions
```

### 设计元素
- 使用图标或emoji增强视觉效果
- 每个目标用不同颜色区分（可选）

---

## 第4页：数据与方法 (Data & Methodology)

### 布局
- 上下分栏：数据（上）+ 方法（下）

### 内容
**上半部分 - 数据**：
```
Data Source: Kaggle Video Game Sales Dataset
• 16,598 games (1995-2016)
• 3 genres: Action (3,167), Role-Playing (1,422), Simulation (835)
• 5 regions: Global, NA, EU, JP, Other
• Log transformation: log1p(sales) for robust analysis
```

**下半部分 - 方法**：
```
Bootstrap Resampling Method
• Non-parametric approach
• 10,000 bootstrap iterations per analysis
• 95% percentile confidence intervals
• Random seed: 42 (reproducibility)
• Independent resampling for each group
```

### 设计元素
- 数据部分：用表格或列表展示
- 方法部分：可添加流程图（数据→Bootstrap→CI→结论）

---

## 第5页：关键发现概览 (Key Findings Overview)

### 布局
- 标题居中
- 3-4个关键发现，用大号数字+文字

### 内容
**标题**：Key Findings at a Glance

**发现列表**：
```
1️⃣ Regional Preferences Exist
   • Japan: Role-Playing significantly outperforms Action
   • North America & Europe: Action leads
   • Global: Role-Playing slightly ahead

2️⃣ Significant Differences Found
   • 12 out of 15 pairwise comparisons are statistically significant
   • 80% of genre differences show meaningful patterns

3️⃣ Uncertainty Quantified
   • All estimates include 95% confidence intervals
   • Bootstrap method robust to data distribution

4️⃣ Action Games: Consistent Performance
   • Highest or second-highest in 4 out of 5 regions
   • Most reliable across markets
```

### 设计元素
- 使用大号数字（1️⃣ 2️⃣ 3️⃣ 4️⃣）或圆形图标
- 每个发现用不同颜色背景框

---

## 第6页：区域对比热力图 (Regional Comparison Heatmap)

### 布局
- 全页展示图表

### 内容
**标题**：Genre Performance Across Regions

**插入图片**：
- 文件：`results/figures/regional_comparison_heatmap.png`
- 如果该图不存在，使用数据创建表格热力图

**图表说明**（底部小字）：
```
Heatmap showing mean log-transformed sales by genre and region.
Darker colors indicate higher sales.
```

**关键观察**（右侧或底部文本框）：
```
• Japan: Strong preference for Role-Playing (0.145)
• Global/NA/EU: Action games lead
• Simulation: Consistent but lower across regions
```

### 设计元素
- 图表占页面80%空间
- 确保图表清晰可读（300 DPI）

---

## 第7页：置信区间可视化 (Confidence Intervals)

### 布局
- 左侧：图表（60%）
- 右侧：关键数值表格（40%）

### 内容
**标题**：95% Confidence Intervals for Genre Means

**插入图片**：
- 文件：`results/figures/confidence_intervals_all_regions.png`
- 或：`results/figures/confidence_intervals_global.png`

**右侧表格**（关键数值）：
```
Global Region:
Genre          Mean    95% CI
─────────────────────────────
Role-Playing   0.326   [0.304, 0.350]
Action         0.313   [0.299, 0.326]
Simulation     0.278   [0.255, 0.303]
```

**说明文字**：
```
Error bars show 95% confidence intervals.
Non-overlapping intervals indicate significant differences.
```

### 设计元素
- 图表清晰，误差条可见
- 表格使用专业格式

---

## 第8页：日本市场特殊发现 (Japan Market - Special Case)

### 布局
- 左侧：数据/图表（60%）
- 右侧：发现说明（40%）

### 内容
**标题**：Japan Market: Unique Genre Preferences

**左侧内容**：
- 插入：`results/figures/confidence_intervals_jp.png`
- 或创建对比表格：
```
Japan Region:
Genre          Mean    95% CI        Rank
─────────────────────────────────────
Role-Playing   0.145   [0.131, 0.160]  1st
Simulation     0.052   [0.042, 0.063]  2nd
Action         0.038   [0.035, 0.042]  3rd
```

**右侧发现**：
```
🔍 Key Finding:
Role-Playing games in Japan show 
significantly higher sales than Action games

📊 Statistical Evidence:
• Mean difference: -0.107
• 95% CI: [-0.122, -0.092]
• Significant: YES (CI excludes 0)

💡 Interpretation:
Japanese market has distinct preferences,
favoring RPGs over action games
```

### 设计元素
- 突出显示"Significant: YES"
- 使用对比色强调差异

---

## 第9页：Bootstrap分布示例 (Bootstrap Distribution Example)

### 布局
- 全页展示图表

### 内容
**标题**：Bootstrap Distribution: Action in Global Market

**插入图片**：
- 文件：`results/figures/bootstrap_dist_action_global.png`

**图表说明**（底部）：
```
Histogram of 10,000 bootstrap means for Action genre in Global market.
Red dashed line: Observed mean (0.313)
Green shaded area: 95% confidence interval [0.299, 0.326]
```

**关键信息**（右上角文本框）：
```
Bootstrap Method:
• 10,000 resamples with replacement
• Distribution shows sampling variability
• CI captures uncertainty around estimate
```

### 设计元素
- 图表清晰，标注可见
- 确保红色和绿色在深色背景下可见

---

## 第10页：显著性差异总结 (Significant Differences Summary)

### 布局
- 标题
- 表格展示所有显著性结果

### 内容
**标题**：Statistically Significant Differences (α = 0.05)

**表格**（可滚动或分页）：
```
Region    Comparison              Difference    95% CI          Significant
─────────────────────────────────────────────────────────────────────────
Global    Action vs Simulation    0.034        [0.005, 0.061]   ✓
Global    Role-Playing vs Sim.    0.048        [0.016, 0.081]   ✓
NA        Action vs Role-Playing  0.036        [0.018, 0.053]   ✓
NA        Action vs Simulation    0.024        [0.005, 0.042]   ✓
EU        Action vs Role-Playing  0.031        [0.017, 0.044]   ✓
EU        Action vs Simulation    0.027        [0.010, 0.043]   ✓
JP        Action vs Role-Playing  -0.107       [-0.122, -0.092] ✓
JP        Action vs Simulation    -0.013       [-0.025, -0.003] ✓
JP        Role-Playing vs Sim.     0.093        [0.076, 0.111]   ✓
Other     Action vs Role-Playing  0.012        [0.006, 0.018]   ✓
Other     Action vs Simulation    0.014        [0.008, 0.021]   ✓

Total: 12 out of 15 comparisons are significant (80%)
```

**底部总结**：
```
• Most differences are statistically meaningful
• Japan shows strongest regional preference pattern
• Action games generally outperform in Western markets
```

### 设计元素
- 表格使用交替行颜色
- 显著性列用绿色✓标记
- 字体大小确保可读性

---

## 第11页：方法优势 (Methodological Advantages)

### 布局
- 标题
- 3-4个优势，每个配图标

### 内容
**标题**：Why Bootstrap Method?

**优势列表**：
```
✅ Non-Parametric
   • No assumptions about data distribution
   • Robust to skewed sales data

✅ Quantifies Uncertainty
   • Direct estimation from empirical data
   • Confidence intervals reflect sampling variability

✅ Handles Unequal Sample Sizes
   • Action: 3,167 games
   • Role-Playing: 1,422 games
   • Simulation: 835 games

✅ Reproducible
   • Fixed random seed (42)
   • Fully documented workflow
   • 100 automated tests passing
```

### 设计元素
- 每个优势用不同颜色框
- 使用图标增强视觉效果

---

## 第12页：实际意义 (Practical Implications)

### 布局
- 左侧：发现（60%）
- 右侧：建议（40%）

### 内容
**标题**：Practical Implications for Game Developers & Publishers

**左侧 - 关键发现**：
```
🎮 Regional Strategy Matters
   • One-size-fits-all approach may not work
   • Japan requires different genre focus

📊 Action Games: Safe Bet
   • Consistent performance across most regions
   • Lower risk for global releases

🎯 Role-Playing: Niche Opportunity
   • Strong in Japan and Global markets
   • Potential for targeted marketing
```

**右侧 - 建议**：
```
For Developers:
• Consider regional preferences in portfolio planning
• Use confidence intervals for risk assessment
• Don't rely solely on point estimates

For Publishers:
• Market-specific genre strategies
• Quantify uncertainty in sales projections
• Bootstrap provides robust estimates
```

### 设计元素
- 使用图标区分不同部分
- 建议部分用不同背景色

---

## 第13页：项目完成度 (Project Completion)

### 布局
- 标题
- 4个模块，每个显示完成状态

### 内容
**标题**：Project Implementation Status

**模块状态**（用进度条或图标）：
```
✅ Module 1: Data Preprocessing
   • 5 cleaned datasets
   • 19 tests passing

✅ Module 2: Bootstrap Analysis
   • 30 analyses completed
   • 29 tests passing

✅ Module 3: Visualization
   • All required figures generated
   • 24 tests passing

✅ Module 4: Reporting
   • Table generation complete
   • 28 tests passing

Total: 100 tests, all passing ✅
```

**交付物**：
```
📊 12 result tables
📈 Multiple visualizations (300 DPI)
📓 Complete Jupyter Notebook
💻 Reproducible codebase
```

### 设计元素
- 使用进度条或完成图标
- 突出"100 tests, all passing"

---

## 第14页：结论 (Conclusions)

### 布局
- 标题
- 3-4个主要结论
- 底部：未来工作（可选）

### 内容
**标题**：Conclusions

**主要结论**：
```
1. Regional preferences for video game genres are 
   statistically significant and quantifiable

2. Japan market shows distinct preferences, with 
   Role-Playing games significantly outperforming Action

3. Bootstrap method successfully quantifies uncertainty 
   without distributional assumptions

4. Results provide evidence-based guidance for 
   regional marketing and portfolio decisions
```

**未来工作**（小字，底部）：
```
• Sensitivity analysis (all years vs 1995-2016)
• Platform-specific analysis
• BCa method comparison
```

### 设计元素
- 结论用大号字体
- 每个结论单独一行或框

---

## 第15页：致谢/问题 (Thank You / Q&A)

### 布局
- 居中布局

### 内容
**主标题**：Thank You

**副标题**：
```
Questions & Discussion
```

**联系信息**（可选，小字）：
```
Project Repository: github.com/Zudzilean/bootstrap_genre_analysis
Jupyter Notebook: notebooks/bootstrap_analysis_workflow.ipynb
```

### 设计元素
- 简洁、专业
- 可添加项目logo或图标

---

## 备用页面建议

### 如果需要更多细节，可添加：

**技术细节页**：
- Bootstrap算法流程图
- 代码架构图
- 测试覆盖率

**数据预处理页**：
- 数据清洗步骤
- 样本量统计
- 时间窗口选择理由

**敏感性分析页**（如果有）：
- 不同时间窗口对比
- 不同置信水平对比

---

## 图片文件清单

### 必须使用的图片：
1. `results/figures/regional_comparison_heatmap.png` - 第6页
2. `results/figures/confidence_intervals_all_regions.png` - 第7页
3. `results/figures/bootstrap_dist_action_global.png` - 第9页

### 可选图片（如果存在）：
- `results/figures/confidence_intervals_global.png`
- `results/figures/confidence_intervals_na.png`
- `results/figures/confidence_intervals_eu.png`
- `results/figures/confidence_intervals_jp.png`
- `results/figures/confidence_intervals_other.png`
- `results/figures/genre_means_by_region.png`
- `results/figures/difference_distributions_*.png`

### 如果图片不存在：
- 使用数据表格替代
- 或快速生成简化版图表

---

## 演示技巧

1. **时间分配**：
   - 介绍（2分钟）：第1-3页
   - 方法（2分钟）：第4页
   - 结果（6分钟）：第5-10页
   - 讨论（3分钟）：第11-13页
   - 结论（1分钟）：第14-15页

2. **重点强调**：
   - 日本市场的特殊发现（第8页）
   - Bootstrap方法的优势（第11页）
   - 显著性差异总结（第10页）

3. **互动准备**：
   - 准备回答关于bootstrap方法的问题
   - 准备解释为什么选择这些游戏类型
   - 准备讨论实际应用价值

---

## AI制作PPT提示词模板

### 对于ChatGPT/Claude等AI工具，可以使用：

```
请帮我制作一个学术风格的PPT演示文稿，主题是"Bootstrap Analysis of Genre Impact on Regional Video Game Sales"。

要求：
1. 总共15页
2. 学术风格，深蓝色/深灰色背景，白色文字
3. 字体：Arial，标题加粗，正文至少18pt
4. 每页内容如下：

[然后复制上面每一页的详细内容]

请为每一页设计合适的布局，并告诉我需要插入哪些图片文件。
```

---

## 快速检查清单

- [ ] 所有15页内容已准备
- [ ] 所有需要的图片文件已确认存在
- [ ] 数据表格已准备好
- [ ] 字体大小确保可读性（至少18pt）
- [ ] 颜色对比度足够（深色背景+浅色文字）
- [ ] 每页不超过7行要点
- [ ] 关键数字和发现已突出显示
- [ ] 时间控制在10-15分钟

