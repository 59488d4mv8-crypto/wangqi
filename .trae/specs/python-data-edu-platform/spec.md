# Python 商务数据分析在线教育平台 - Product Requirement Document

## Overview
- **Summary**: 一款面向"商务数据分析与应用"专业学生的在线教育平台，以 10 个 Python 商务数据分析实战项目为核心课程，部署于 Cloudflare Pages（免费版）。平台提供完整课程体系、互动式学习模块（学/练/测）、成就激励系统，并在前端静态页面中展示 Python 代码案例与数据分析可视化结果。
- **Purpose**: 解决商务数据分析专业学生缺少"贴近真实业务、可动手复现的 Python 项目"的痛点；提供一个轻量级、零运维成本的课程平台，让学生在浏览器中学习课程、下载/复制 Python 代码、在线完成测验与练习，并通过成就系统获得学习动力。
- **Target Users**: 商务数据分析与应用专业的学生（本科 / 高职 / 中职）、教师（作为授课辅助）、对 Python 商务数据分析感兴趣的入门自学者。

## Goals
- 搭建一个可一键部署到 Cloudflare Pages 免费版的静态在线教育平台。
- 提供 10 个结构化、围绕业务目标的 Python 数据分析实战项目课程。
- 每门课程均包含"学（理论与代码讲解）+ 练（互动练习）+ 测（章节测评）"。
- 提供成就 / 徽章 / 学习积分 / 排行榜等激励系统（浏览器本地持久化）。
- 平台对免费用户友好：零后端、零服务器、数据持久化依赖浏览器 LocalStorage / IndexedDB，无需第三方付费服务。

## Non-Goals (Out of Scope)
- 不在 Cloudflare Pages 免费环境中运行真实 Python 代码执行沙箱（免费版无 K8s、无 Workers Python runtime 持久化）；学员需在自己本地 Jupyter / VS Code 运行 Python 代码。
- 不提供多端账号云同步（免费方案，云端存储与身份认证不在本次范围）。
- 不包含视频流、直播、付费交易系统。
- 不做跨用户数据分析的真实后端（仅在前端模拟数据以演示知识点）。

## Background & Context
- Cloudflare Pages 免费版提供静态站点托管，支持 Cloudflare Pages Functions（JS/TS Worker），但不适合直接托管 Python 教学沙箱。因此平台采用"**纯静态前端 + 本地 JS 运行测评 + 课程配套 Python 代码下载**"的架构。
- 学员运行 Python 的方式：在本地安装 Anaconda / Python 3.9+，使用课程中提供的 `.ipynb` / `.py` 与样本数据；平台网页负责引导、讲解与测验。
- 10 个项目覆盖用户画像、RFM、NLP 情感、时间序列、Apriori、漏斗分析等真实业务场景，与"商务数据分析与应用"专业教学大纲高度契合。

## Functional Requirements
- **FR-1 课程体系**：提供 10 门课程列表页、课程详情页、章节导航；每门课程含"项目背景 - 业务目标 - 数据准备 - Python 代码步骤 - 结果解读 - 拓展思考"。
- **FR-2 互动学习模块**：每章节提供可折叠的代码块（含复制按钮）、关键知识点高亮、下一步引导。
- **FR-3 练习模块**：每章节提供 3-5 道互动练习题（单选 / 多选 / 填空 / 代码填空），即时判分并给出解析。
- **FR-4 测评模块**：每门课程结束时提供 10-15 道综合测评题，记录得分并判定是否通过（例如 ≥60 分）。
- **FR-5 成就激励系统**：学习积分、连续学习天数、徽章（完成课程 / 首次满分 / 坚持 7 天 / 掌握某项技能等）、本地排行榜（与"虚拟同学"对比）。
- **FR-6 代码与资源下载**：每个项目提供 Python 代码 / Jupyter Notebook / 样本 CSV 的打包下载按钮（链接指向仓库 assets 或数据 URI 生成）。
- **FR-7 学习进度持久化**：基于浏览器 LocalStorage 记录每章节已读、练习完成、测评得分，刷新不丢失。
- **FR-8 仪表盘 / 学习中心**：首页展示学员学习进度、已获徽章、今日任务推荐、最近学习课程。
- **FR-9 站内导航与搜索**：支持按课程名 / 技能标签（Pandas、可视化、RFM、NLP…）快速查找。
- **FR-10 响应式 & 无障碍**：支持 PC / Pad / 手机浏览；基础对比度与键盘可达。

## Non-Functional Requirements
- **NFR-1 可部署**：项目结构直接满足 Cloudflare Pages 要求（根目录 `public/` 或框架 `dist/` 产出），提供 `README` 一键部署说明。
- **NFR-2 零后端**：所有测评、积分、进度在浏览器端完成；不依赖外部服务。
- **NFR-3 性能**：首屏 HTML/CSS/JS ≤ 500KB（不含资源包），LCP ≤ 2.5s。
- **NFR-4 可维护**：课程内容以结构化数据（JSON / Markdown）驱动，新增课程不改动逻辑代码。
- **NFR-5 浏览器兼容**：Chrome / Edge / Firefox / Safari 最近两个主版本。
- **NFR-6 数据安全**：不采集用户实名信息，学习记录仅存本地；提供"导出学习记录"与"重置数据"按钮。

## Constraints
- **Technical**: Cloudflare Pages（免费版）静态托管；前端选用轻量方案（纯静态 HTML + 原生 JS，或 Vue 3 / React 静态构建二选一，本 PRD 推荐"纯静态"以最小化复杂度）；代码资源通过仓库 assets 或内联 Blob 提供下载。
- **Business**: 免费用户额度限制（Pages 构建次数 / 带宽），因此避免大体积视频；课程素材以文本、轻量图片与 SVG 为主。
- **Dependencies**: 可使用 CDN 加载的前端库（如 Chart.js / ECharts、highlight.js 用于代码高亮、marked 用于 Markdown 渲染），无需本地 node_modules 即可运行。

## Assumptions
- 学员已具备或可在课程第 0 章完成 Python 环境安装（Anaconda / venv + Jupyter）。
- 学员通过浏览器访问平台，使用现代浏览器并启用 JavaScript 与 LocalStorage。
- 课程数据与代码在平台仓库中以静态资源提供，教师可通过编辑 Markdown/JSON 更新课程。

## Acceptance Criteria

### AC-1 课程列表页可访问
- **Given**: 用户打开首页
- **When**: 点击"课程"导航或滚动到课程区域
- **Then**: 能看到 10 门课程卡片（标题、简介、技能标签、预计时长、难度），点击卡片进入课程详情页
- **Verification**: `programmatic`
- **Notes**: 可通过静态路由 `/courses/{id}.html` 或 SPA hash 路由实现

### AC-2 课程章节可顺序学习
- **Given**: 用户进入某门课程详情页
- **When**: 点击章节列表中的章节 N
- **Then**: 进入该章节内容页，包含"上一章 / 下一章"按钮，并记录"已访问"
- **Verification**: `programmatic`

### AC-3 代码块可复制与下载
- **Given**: 课程章节内展示 Python 代码
- **When**: 用户点击"复制"按钮或"下载 .py"按钮
- **Then**: 代码复制到剪贴板并提示"已复制"；或生成 `.py` 文件下载
- **Verification**: `programmatic`

### AC-4 练习题即时判分
- **Given**: 章节包含 3-5 道练习
- **When**: 用户作答并点击"提交"
- **Then**: 每题显示对错与解析，章节练习总分被记录
- **Verification**: `programmatic`

### AC-5 课程综合测评给出成绩
- **Given**: 用户完成所有章节练习后进入课程测评
- **When**: 提交测评
- **Then**: 显示得分与通过判定（≥60 分），并持久化该成绩
- **Verification**: `programmatic`

### AC-6 成就与徽章
- **Given**: 用户满足徽章条件（完成第 1 门课程 / 连续 7 天访问 / 某测评满分）
- **When**: 触发条件并刷新页面或访问"成就中心"
- **Then**: 对应徽章点亮，积分数值增加，有明显视觉提示
- **Verification**: `programmatic` + `human-judgment`（动画 / 视觉反馈合理性）

### AC-7 学习进度在刷新后保留
- **Given**: 用户在某课程完成部分章节与练习
- **When**: 关闭浏览器后重新打开
- **Then**: 之前的进度、得分、徽章状态仍存在；并可一键"重置"
- **Verification**: `programmatic`

### AC-8 仪表盘展示个人学习情况
- **Given**: 用户有学习记录
- **When**: 打开首页 / 学习中心
- **Then**: 看到课程完成度、今日任务、已获徽章数量、推荐下一节内容
- **Verification**: `programmatic` + `human-judgment`（信息密度与可读性）

### AC-9 可在 Cloudflare Pages 免费版一键部署
- **Given**: 仓库代码就绪，`README` 提供部署步骤
- **When**: 按 README 指引在 Cloudflare Pages 连接仓库并构建
- **Then**: 构建成功，站点可访问，无 404 / 白屏 / 500
- **Verification**: `programmatic`

### AC-10 移动端可用
- **Given**: 用户使用手机浏览器打开
- **When**: 浏览课程、做题、复制代码
- **Then**: 布局可用，无横向滚动条，按钮点击区域 ≥ 40px
- **Verification**: `human-judgment`

## Open Questions
- [ ] 前端框架选型：纯静态 HTML + 原生 JS（零构建，Pages 直接托管）/ Vue 3 Vite 静态构建 / React Vite 静态构建？（本 PRD 默认推荐"纯静态"以便免费用户最小化部署复杂度）
- [ ] 是否需要"教师端"管理课程内容的简易 UI（例如编辑 JSON 生成器）？本次默认"不需要"，留作后续迭代。
- [ ] 课程样本数据是否需要真实 CSV（体积可能数 MB）？本 PRD 推荐提供 5 万行以内的模拟 CSV，控制在可接受体积。
- [ ] 是否需要国际化（中英双语）？默认仅中文。
