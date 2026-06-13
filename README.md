# Python 商务数据分析在线教育平台

面向"商务数据分析与应用"专业学生的在线学习平台：10 门 Python 数据分析实战项目课程 +
学/练/测/成就激励系统，纯静态前端，一键部署到 Cloudflare Pages（免费版）。

## 功能概览

- 10 门实战项目课程（注册活跃分析、课程完成度与流失预测、RFM 价值分层、NLP 情感分析、
  学习时长与成绩相关分析、付费转化漏斗、Apriori 关联规则、时间序列预测、教师综合评分、
  用户画像与运营策略）。
- 每门课程包含：项目背景 → Python 代码讲解（可复制 / 下载 `.py` / `.csv`）→ 章节练习
  （单选/多选/填空/代码填空，即时判分）→ 综合测评。
- 成就激励系统：积分、徽章、连续学习天数、本地排行榜（与虚拟同学对比）。
- 学习记录完全保存在浏览器本地（localStorage），可一键导出 JSON / 重置。
- 响应式布局，PC / Pad / 手机均可使用。

## 目录结构

```
.
├── index.html                 # 首页 / 学习中心仪表盘
├── courses.html               # 课程列表 + 搜索 + 技能标签筛选
├── course.html                # 单门课程详情（章节 / 代码 / 练习 / 测评）
├── achievements.html          # 成就中心：徽章列表与统计
├── 404.html
├── favicon.svg
├── robots.txt
├── assets/
│   ├── css/style.css          # 全站样式 + 响应式
│   ├── js/
│   │   ├── app.js             # 全局导航 / toast / 年份
│   │   ├── storage.js         # localStorage 封装：进度 / 分数 / 徽章 / 导出
│   │   ├── course.js          # 课程数据加载 + 练习判分
│   │   └── achievements.js    # 徽章 & 积分引擎
│   └── data/
│       ├── badges.json        # 徽章配置
│       ├── courses/
│       │   ├── index.json     # 课程列表
│       │   ├── user-registration-activity.json
│       │   ├── course-completion-dropout.json
│       │   ├── online-education-rfm.json
│       │   ├── review-nlp-sentiment.json
│       │   ├── study-time-score-correlation.json
│       │   ├── paid-conversion-funnel.json
│       │   ├── course-apriori.json
│       │   ├── traffic-sales-timeseries.json
│       │   ├── teacher-quality-score.json
│       │   └── user-persona-operation.json
│       └── resources/          # 10 门课程的 Python 代码 / Notebook / 示例 CSV
│           ├── <课程id>/main.py
│           ├── <课程id>/notebook.ipynb
│           └── <课程id>/sample_data.csv
└── README.md
```

## 本地预览

因为页面通过 `fetch()` 读取 JSON 数据，建议启动一个本地 HTTP 服务器（直接双击打开 HTML
可能触发浏览器的 file:// 跨域限制）。

```bash
cd <项目根目录>
python3 -m http.server 8000
# 浏览器打开 http://localhost:8000
```

或使用 Node：

```bash
npx http-server -p 8000
```

## 在本地运行课程 Python 代码

每门课程在 `assets/data/resources/<课程id>/` 下包含：

- `main.py` — 可直接执行的 Python 脚本，会在同目录生成若干 `.png` 图表。
- `notebook.ipynb` — 在 Jupyter Notebook / JupyterLab 中打开即可。
- `sample_data.csv` — 示例数据（UTF-8）。

建议的环境：

- Python 3.9+
- pandas, numpy, matplotlib, seaborn, scikit-learn, scipy
- 可选：jieba、wordcloud、mlxtend（对应课程会在缺库时降级处理）

```bash
pip install -r <(echo -e "pandas\nnumpy\nmatplotlib\nseaborn\nscikit-learn\nscipy\njieba\nwordcloud\nmlxtend")

# 示例：运行 RFM 课程
cd assets/data/resources/online-education-rfm
python3 main.py
ls *.png
```

## 部署到 Cloudflare Pages（免费版）

本项目是**纯静态站点**，在 Cloudflare Pages 上零构建即可部署。

方式一：连接 Git 仓库（推荐，支持自动部署）

1. 将本项目推送到 GitHub / GitLab 仓库。
2. 登录 Cloudflare Dashboard → Workers & Pages → Create → Pages → Connect to Git。
3. 选择仓库，按以下配置创建项目：
   - **Project name**：任取，例如 `python-data-edu`
   - **Production branch**：`main`（或 `master`）
   - **Build command**：（留空）
   - **Build output directory**：`/`
4. 点 Save and Deploy。数秒后你将得到一个 `*.pages.dev` 域名，访问即可。

方式二：直接上传目录

1. 在 Pages 项目中点 **Create → Upload assets**。
2. 将整个项目目录（含 `index.html` 与 `assets/`）拖入上传区，发布即可。

> 注意：Cloudflare Pages 免费版有月度构建次数与带宽额度，对本项目来说绰绰有余。

## 自定义与扩展

- **新增课程**：在 `assets/data/courses/index.json` 添加条目；在同目录下新建
  `<课程id>.json`，参考现有课程 JSON 结构。
- **新增徽章**：编辑 `assets/data/badges.json`，每条记录形如
  `{ "id": "...", "title": "...", "description": "...", "icon": "🏅",
  "points": 100, "condition": {"type":"firstCourseCompleted","value":""} }`。
  目前引擎支持的 `condition.type`：`firstCourseCompleted`、`courseCompleted`（值为课程 id）、
  `streakDays`、`examFullScore`、`totalPoints`、`allChaptersRead`。
- **修改样式**：直接编辑 `assets/css/style.css`。所有颜色/圆角/阴影通过 CSS 变量定义在
  文件开头，方便统一修改。

## 常见问题

1. **页面显示空白或课程列表加载失败**
   - 确认通过 `http://localhost:8000` 访问，而不是 `file://...`。
   - 浏览器 DevTools → Console 可看到具体错误。

2. **`charts.html` 显示的中文为方框**
   - 平台前端页面不会出现此问题；这只发生在你在本地 `python main.py` 生成图表时。请为
     matplotlib 安装中文字体（例如 Noto Sans CJK、SimHei），并在脚本中加入
     `plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC','SimHei']`。

3. **想要云同步学习进度？**
   - 目前设计为纯静态 + 本地存储。如需云端同步，需要额外引入身份认证与后端服务，
     不在免费 Pages 范围。

4. **我想删除本地的学习记录**
   - 在首页 → 学习中心 → 工具区 → 点"重置全部学习记录"，或浏览器 DevTools →
     Application → Local Storage → 删除以 `learn_` 开头的所有键。

## License

项目代码以 MIT 许可证发布，课程示例数据为随机模拟数据。
