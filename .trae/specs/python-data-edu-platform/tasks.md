# Python 商务数据分析在线教育平台 - 实施计划

## [ ] Task 1: 项目脚手架与 Cloudflare Pages 部署结构
- **Priority**: P0
- **Depends On**: None
- **Description**:
  - 约定仓库目录：`/index.html`、`/courses/*.html`、`/assets/css`、`/assets/js`、`/assets/data/courses/*.json`、`/assets/data/courses/codes/*.py / .ipynb / .csv`
  - 约定构建命令："None"（纯静态，Pages 直接发布仓库根目录）
  - 提供部署说明（在 README 中）：登录 Cloudflare Pages → Connect Git → 选择仓库 → Build command 留空 → Output directory 设为 `/` → 部署
- **Acceptance Criteria Addressed**: AC-9
- **Test Requirements**:
  - `programmatic` TR-1.1: 使用本地静态服务器（`python -m http.server`）在 `http://localhost:8000` 打开首页无 404
  - `programmatic` TR-1.2: 根目录存在 `index.html`、`assets/js/app.js`、`assets/css/style.css` 且可被浏览器加载
- **Notes**: 不引入 Node 构建工具；后续若迁移到 Vite 可单独分支进行。

## [ ] Task 2: 课程数据模型与 10 门课程 JSON 内容框架
- **Priority**: P0
- **Depends On**: Task 1
- **Description**:
  - 设计课程 JSON schema：`{id, title, summary, skills[], difficulty, hours, badges[], chapters: [{id, title, sections:[{type, content, code?}], quiz:[{type, question, options?, answer, explain}]}], finalExam:[...]}`
  - 为 10 个项目各自创建 `assets/data/courses/{id}.json`，至少包含：
    1. 教育平台用户注册与活跃行为分析
    2. 课程学习完成度与 dropout 流失预测
    3. 在线教育用户 RFM 价值分层分析
    4. 课程评价 NLP 情感分析
    5. 学生学习时长与成绩相关性分析
    6. 在线课程付费转化漏斗分析
    7. 课程关联规则分析（Apriori）
    8. 访问量与销量时间序列预测
    9. 教师授课质量多维度综合评分
    10. 用户画像与精准运营策略
  - 为每门课程编写 ≥ 3 章示例内容骨架、≥ 3 道章节练习、≥ 10 道综合测评题目
- **Acceptance Criteria Addressed**: AC-1, AC-2, FR-1
- **Test Requirements**:
  - `programmatic` TR-2.1: 10 个课程 JSON 文件存在且能被浏览器 `fetch` 解析无异常
  - `programmatic` TR-2.2: 每个课程至少包含 3 个章节、每章节至少 3 道题目、最终测评至少 10 题
  - `human-judgement` TR-2.3: 内容语言与讲解层次符合"商务数据分析与应用专业"教学逻辑

## [ ] Task 3: 课程页面渲染引擎（章节 + 上一章/下一章）
- **Priority**: P0
- **Depends On**: Task 2
- **Description**:
  - 创建 `/course.html?id=...`（或使用 hash 路由）读取对应 JSON，渲染章节 TOC、正文、代码块
  - 代码块包含"复制"与"下载为 .py"两个按钮（`navigator.clipboard` + `Blob` / `URL.createObjectURL`）
  - 渲染"上一章 / 下一章"导航，点击切换并在 URL 中保留章节锚点
- **Acceptance Criteria Addressed**: AC-2, AC-3
- **Test Requirements**:
  - `programmatic` TR-3.1: 访问任意课程第 N 章，点击"下一章" URL 更新并内容更新
  - `programmatic` TR-3.2: 点击代码块的"复制"后，剪贴板内容与代码块文本一致
  - `programmatic` TR-3.3: 点击"下载 .py"触发浏览器下载，文件名形如 `{courseId}_ch{chapterId}.py`

## [ ] Task 4: 章节练习与即时判分模块
- **Priority**: P0
- **Depends On**: Task 3
- **Description**:
  - 根据 JSON 渲染单选 / 多选 / 填空 / 代码填空题
  - 提交时在客户端判分并在每题下方显示"正确 / 错误 + 解析"
  - 记录章节得分到 LocalStorage（key: `progress:{courseId}:{chapterId}`）
- **Acceptance Criteria Addressed**: AC-4
- **Test Requirements**:
  - `programmatic` TR-4.1: 答对所有题 → 显示 100；全部答错 → 显示 0；部分答对按比例得分
  - `programmatic` TR-4.2: 刷新页面后章节得分仍存在于 LocalStorage
  - `human-judgement` TR-4.3: 题目与解析排版清晰易读

## [ ] Task 5: 课程综合测评模块
- **Priority**: P0
- **Depends On**: Task 4
- **Description**:
  - 在课程页增加"进入综合测评"入口（默认在完成全部章节后出现，但不强制）
  - 渲染 10-15 题，提交后在页面显示总分、通过判定（≥60）、错题回顾
  - 持久化成绩（`exam:{courseId}`）并触发成就系统检查
- **Acceptance Criteria Addressed**: AC-5
- **Test Requirements**:
  - `programmatic` TR-5.1: 随机作答后成绩在 [0, 100] 之间，且 ≥60 显示"通过"
  - `programmatic` TR-5.2: 满分会触发"满分"徽章（见 Task 7）条件

## [ ] Task 6: 学习进度持久化与"重置 / 导出"功能
- **Priority**: P1
- **Depends On**: Task 4
- **Description**:
  - 统一封装 `storage.js`：读/写章节已读、章节得分、测评得分、访问日期
  - 在"学习中心"提供"导出学习记录（JSON）"与"重置全部数据"两个按钮
- **Acceptance Criteria Addressed**: AC-7
- **Test Requirements**:
  - `programmatic` TR-6.1: 关闭浏览器后再次打开，首页显示历史进度数据
  - `programmatic` TR-6.2: 点击"重置"后 LocalStorage 对应 key 被清空，页面立即反映

## [ ] Task 7: 成就 / 徽章 / 积分系统
- **Priority**: P1
- **Depends On**: Task 5, Task 6
- **Description**:
  - 定义徽章 JSON：`{id, title, icon, condition: {type, value}, points}`
  - 支持的 condition 类型：`firstCourseCompleted`、`courseCompleted:{id}`、`streakDays>=7`、`examFullScore`、`totalPoints>=N`
  - 在每个可能的用户动作（提交测评、记录访问日）后调用 `achievements.checkAll()`，将新徽章写入 LocalStorage 并在顶部弹出 toast 提示
  - 提供成就中心页 `/achievements.html` 展示已获 / 未获徽章与总积分
- **Acceptance Criteria Addressed**: AC-6
- **Test Requirements**:
  - `programmatic` TR-7.1: 完成一门课程 → 徽章 +1、积分 +N、toast 可见
  - `programmatic` TR-7.2: 连续 7 天有访问记录 → 点亮"坚持学习 7 天"徽章
  - `human-judgement` TR-7.3: 徽章视觉与动画有明显完成感

## [ ] Task 8: 首页 / 学习中心仪表盘
- **Priority**: P1
- **Depends On**: Task 6
- **Description**:
  - `index.html` 展示：欢迎横幅、推荐继续学习、已完成课程数、总积分、最近徽章、今日任务（今日目标：学 1 章）
  - 使用轻量图表（ECharts / Chart.js via CDN）渲染"本周学习时长"柱状图（演示数据即可）
- **Acceptance Criteria Addressed**: AC-8
- **Test Requirements**:
  - `programmatic` TR-8.1: 访问首页能读取并展示课程数、积分与最近徽章
  - `human-judgement` TR-8.2: 仪表盘信息层次分明、关键信息在首屏可见

## [ ] Task 9: 10 门课程 Python 代码与数据文件
- **Priority**: P1
- **Depends On**: Task 2
- **Description**:
  - 为 10 个项目编写完整 Python 代码文件（`*.py`）与最简样本数据（CSV），保证直接在本地 Jupyter / Python 中可运行
  - 关键代码在课程 JSON 的 `code` 字段中同步，学员可在线复制
  - 在 `/assets/data/resources/` 目录提供 ZIP 打包（可在构建时或本地手动打包）或直接链接 `.py/.csv` 文件下载
- **Acceptance Criteria Addressed**: AC-3
- **Test Requirements**:
  - `programmatic` TR-9.1: 每个课程存在至少一个 `.py`、一个 `.csv` 资源链接
  - `human-judgement` TR-9.2: 代码注释清晰、可直接本地运行

## [ ] Task 10: 课程搜索 / 标签过滤
- **Priority**: P2
- **Depends On**: Task 2
- **Description**:
  - 课程列表页提供搜索输入框（按课程名/简介模糊匹配）与技能标签多选（Pandas、Seaborn、RFM、NLP…）
  - 过滤逻辑在前端 JS 完成，不依赖后端
- **Acceptance Criteria Addressed**: FR-9
- **Test Requirements**:
  - `programmatic` TR-10.1: 搜索"RFM"只显示课程 3；清空恢复全部
  - `programmatic` TR-10.2: 组合筛选（标签 + 关键词）结果正确

## [ ] Task 11: 响应式与样式打磨
- **Priority**: P2
- **Depends On**: Task 1
- **Description**:
  - 基于 CSS Flex/Grid 与 `@media` 实现 ≥ 320px（手机）到 ≥ 1200px（桌面）响应式
  - 点击区域 ≥ 40×40px；正文文本对比度 ≥ WCAG AA
- **Acceptance Criteria Addressed**: AC-10, NFR-3
- **Test Requirements**:
  - `programmatic` TR-11.1: 主要页面无横向滚动（在 375×812 视窗下）
  - `human-judgement` TR-11.2: 移动端使用体验流畅

## [ ] Task 12: 部署说明与 README
- **Priority**: P0
- **Depends On**: Task 1-11
- **Description**:
  - 在项目根目录写入 `README.md`，包含：目录结构、本地预览命令、Cloudflare Pages 部署步骤截图或文字步骤、常见问题（如 CORS、资源体积过大）
- **Acceptance Criteria Addressed**: AC-9
- **Test Requirements**:
  - `human-judgement` TR-12.1: 按 README 步骤可完成 Pages 部署（由人工在实际环境验证一次）

## 任务依赖图（示意）
```
Task1 ──┬──> Task2 ──┬──> Task3 ──> Task4 ──┬──> Task5 ──> Task7 ──> Task12
        │            │                      └──> Task6 ──> Task8
        │            └──> Task10                        └──> Task9
        └──> Task11
```
