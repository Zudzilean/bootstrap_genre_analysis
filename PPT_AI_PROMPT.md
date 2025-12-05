# PPT制作AI提示词（可直接复制使用）

## 完整提示词（复制给ChatGPT/Claude等）

```
请帮我制作一个学术风格的PPT演示文稿，主题是"Bootstrap Analysis of Genre Impact on Regional Video Game Sales"。

要求：
1. 总共15页，学术风格
2. 配色：深蓝色/深灰色背景，白色/浅色文字
3. 字体：Arial，标题加粗，正文至少18pt
4. 布局：简洁专业，每页不超过7行要点
5. 每页需要插入的图片文件路径已标注

以下是每一页的详细内容：

---

## 第1页：标题页
布局：居中
内容：
- 主标题（大号加粗）：Bootstrap Analysis of Genre Impact on Regional Video Game Sales
- 副标题（中号）：A Statistical Uncertainty Framework
- 底部（小号）：MATH3110 Project | [作者名字] | [日期]

---

## 第2页：研究问题
布局：左侧文字60%，右侧示意图40%
内容：
标题：Research Question

正文：
Can we, with statistical confidence, conclude that certain video game genres systematically receive higher or lower average sales than others within specific regional markets?

Key Questions:
• Do regional preferences for genres differ significantly?
• Can we quantify the uncertainty around these differences?
• Which genres perform best in which regions?

右侧：世界地图轮廓，标注5个区域（Global, NA, EU, JP, Other）

---

## 第3页：研究目标
布局：标题居中，4个目标列表
内容：
标题：Research Objectives

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

---

## 第4页：数据与方法
布局：上下分栏
内容：
标题：Data & Methodology

上半部分 - 数据：
Data Source: Kaggle Video Game Sales Dataset
• 16,598 games (1995-2016)
• 3 genres: Action (3,167), Role-Playing (1,422), Simulation (835)
• 5 regions: Global, NA, EU, JP, Other
• Log transformation: log1p(sales) for robust analysis

下半部分 - 方法：
Bootstrap Resampling Method
• Non-parametric approach
• 10,000 bootstrap iterations per analysis
• 95% percentile confidence intervals
• Random seed: 42 (reproducibility)
• Independent resampling for each group

---

## 第5页：关键发现概览
布局：标题居中，4个发现
内容：
标题：Key Findings at a Glance

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

---

## 第6页：区域对比热力图
布局：全页展示图表
内容：
标题：Genre Performance Across Regions

插入图片：results/figures/regional_comparison_heatmap.png
（如果不存在，创建数据表格热力图）

图表说明（底部小字）：
Heatmap showing mean log-transformed sales by genre and region.
Darker colors indicate higher sales.

关键观察：
• Japan: Strong preference for Role-Playing (0.145)
• Global/NA/EU: Action games lead
• Simulation: Consistent but lower across regions

---

## 第7页：置信区间可视化
布局：左侧图表60%，右侧表格40%
内容：
标题：95% Confidence Intervals for Genre Means

插入图片：results/figures/confidence_intervals_all_regions.png

右侧表格：
Global Region:
Genre          Mean    95% CI
─────────────────────────────
Role-Playing   0.326   [0.304, 0.350]
Action         0.313   [0.299, 0.326]
Simulation     0.278   [0.255, 0.303]

说明：Error bars show 95% confidence intervals. Non-overlapping intervals indicate significant differences.

---

## 第8页：日本市场特殊发现
布局：左侧数据60%，右侧发现40%
内容：
标题：Japan Market: Unique Genre Preferences

左侧表格：
Japan Region:
Genre          Mean    95% CI        Rank
─────────────────────────────────────
Role-Playing   0.145   [0.131, 0.160]  1st
Simulation     0.052   [0.042, 0.063]  2nd
Action         0.038   [0.035, 0.042]  3rd

右侧发现：
🔍 Key Finding:
Role-Playing games in Japan show significantly higher sales than Action games

📊 Statistical Evidence:
• Mean difference: -0.107
• 95% CI: [-0.122, -0.092]
• Significant: YES (CI excludes 0)

💡 Interpretation:
Japanese market has distinct preferences, favoring RPGs over action games

---

## 第9页：Bootstrap分布示例
布局：全页展示图表
内容：
标题：Bootstrap Distribution: Action in Global Market

插入图片：results/figures/bootstrap_dist_action_global.png

图表说明（底部）：
Histogram of 10,000 bootstrap means for Action genre in Global market.
Red dashed line: Observed mean (0.313)
Green shaded area: 95% confidence interval [0.299, 0.326]

关键信息（右上角）：
Bootstrap Method:
• 10,000 resamples with replacement
• Distribution shows sampling variability
• CI captures uncertainty around estimate

---

## 第10页：显著性差异总结
布局：标题+表格
内容：
标题：Statistically Significant Differences (α = 0.05)

表格：
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

底部总结：
• Most differences are statistically meaningful
• Japan shows strongest regional preference pattern
• Action games generally outperform in Western markets

---

## 第11页：方法优势
布局：标题+4个优势列表
内容：
标题：Why Bootstrap Method?

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

---

## 第12页：实际意义
布局：左侧发现60%，右侧建议40%
内容：
标题：Practical Implications for Game Developers & Publishers

左侧 - 关键发现：
🎮 Regional Strategy Matters
   • One-size-fits-all approach may not work
   • Japan requires different genre focus

📊 Action Games: Safe Bet
   • Consistent performance across most regions
   • Lower risk for global releases

🎯 Role-Playing: Niche Opportunity
   • Strong in Japan and Global markets
   • Potential for targeted marketing

右侧 - 建议：
For Developers:
• Consider regional preferences in portfolio planning
• Use confidence intervals for risk assessment
• Don't rely solely on point estimates

For Publishers:
• Market-specific genre strategies
• Quantify uncertainty in sales projections
• Bootstrap provides robust estimates

---

## 第13页：项目完成度
布局：标题+模块状态
内容：
标题：Project Implementation Status

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

交付物：
📊 12 result tables
📈 Multiple visualizations (300 DPI)
📓 Complete Jupyter Notebook
💻 Reproducible codebase

---

## 第14页：结论
布局：标题+结论列表
内容：
标题：Conclusions

1. Regional preferences for video game genres are statistically significant and quantifiable

2. Japan market shows distinct preferences, with Role-Playing games significantly outperforming Action

3. Bootstrap method successfully quantifies uncertainty without distributional assumptions

4. Results provide evidence-based guidance for regional marketing and portfolio decisions

未来工作（小字，底部）：
• Sensitivity analysis (all years vs 1995-2016)
• Platform-specific analysis
• BCa method comparison

---

## 第15页：致谢
布局：居中
内容：
主标题：Thank You

副标题：Questions & Discussion

联系信息（小字）：
Project Repository: github.com/Zudzilean/bootstrap_genre_analysis
Jupyter Notebook: notebooks/bootstrap_analysis_workflow.ipynb

---

请为每一页设计合适的布局，确保：
1. 学术风格，专业简洁
2. 所有数字和关键发现清晰可见
3. 图片位置已标注，如果图片不存在请用数据表格替代
4. 颜色对比度足够（深色背景+浅色文字）
5. 每页内容不超过7行要点
```

---

## 简化版提示词（如果AI工具限制长度）

```
制作15页学术风格PPT：Bootstrap Analysis of Genre Impact on Regional Video Game Sales

风格：深蓝/深灰背景，白色文字，Arial字体，标题加粗

内容结构：
1. 标题页
2. 研究问题（5个区域对比）
3. 研究目标（4个目标）
4. 数据与方法（Kaggle数据，Bootstrap方法，10,000次迭代）
5. 关键发现（4个要点）
6. 区域热力图（插入results/figures/regional_comparison_heatmap.png）
7. 置信区间图（插入results/figures/confidence_intervals_all_regions.png）
8. 日本市场特殊发现（Role-Playing显著高于Action，差异-0.107）
9. Bootstrap分布示例（插入results/figures/bootstrap_dist_action_global.png）
10. 显著性差异表格（12/15显著，80%）
11. 方法优势（4个优势）
12. 实际意义（开发者/出版商建议）
13. 项目完成度（4个模块，100测试通过）
14. 结论（4个主要结论）
15. 致谢页

关键数据：
- 3个类型：Action(3167), Role-Playing(1422), Simulation(835)
- 5个区域：Global, NA, EU, JP, Other
- 日本：Role-Playing(0.145) > Simulation(0.052) > Action(0.038)
- 12/15差异显著
```

---

## 使用建议

1. **完整版**：适合Claude/ChatGPT等支持长文本的AI
2. **简化版**：适合有长度限制的工具
3. **自定义**：可以根据需要调整页数和内容

## 图片文件检查

使用前请确认以下图片文件存在：
- `results/figures/regional_comparison_heatmap.png`
- `results/figures/confidence_intervals_all_regions.png`
- `results/figures/bootstrap_dist_action_global.png`

如果图片不存在，AI会使用数据表格替代。

