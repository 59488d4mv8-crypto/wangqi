# -*- coding: utf-8 -*-
"""批量生成 10 门课程的 notebook.ipynb"""
import os
import json

BASE = "/workspace/assets/data/resources"

COURSES_META = {
    "user-registration-activity": {
        "title": "用户注册与活跃度分析",
        "intro": "分析各注册渠道的用户分布、注册日期趋势、DAU 以及次日/7日留存率，识别渠道质量差异。",
    },
    "course-completion-dropout": {
        "title": "课程完成率与流失节点分析",
        "intro": "统计章节进入/完成情况，识别流失最严重的节点，并用逻辑回归预测用户是否完成课程。",
    },
    "online-education-rfm": {
        "title": "在线教育 RFM 分群分析",
        "intro": "基于 Recency/Frequency/Monetary 三指标对用户打分，按人群分段（价值用户/新用户/流失用户等）。",
    },
    "review-nlp-sentiment": {
        "title": "课程评论情感与词频分析",
        "intro": "对中文评论进行分词（jieba 或降级 split），统计正负面评论高频词，尝试生成词云。",
    },
    "study-time-score-correlation": {
        "title": "学习时长与成绩相关性分析",
        "intro": "散点图 + 皮尔逊相关 + 简单线性回归，按暂停次数分组查看分数分布差异。",
    },
    "paid-conversion-funnel": {
        "title": "付费转化漏斗分析",
        "intro": "分析 '访问→注册→试听→付费' 各阶段的用户数与转化率，并比较不同渠道。",
    },
    "course-apriori": {
        "title": "课程关联规则挖掘 (Apriori)",
        "intro": "用 Apriori 算法挖掘课程间的频繁项集与关联规则，找到最常见的购课组合。",
    },
    "traffic-sales-timeseries": {
        "title": "流量与销量时间序列分析",
        "intro": "按日聚合后做移动平均 MA 与指数平滑 EMA，并对未来进行简单预测。",
    },
    "teacher-quality-score": {
        "title": "教师质量多维综合评分",
        "intro": "对满意度/完成率/分数/答疑速度等维度做 Z-score 标准化后加权综合评分，生成雷达图。",
    },
    "user-persona-operation": {
        "title": "用户画像 K-Means 聚类",
        "intro": "用 K-Means 对用户做无监督聚类，给出不同人群的特征画像柱状图。",
    },
}


def make_notebook(code_text, title, intro):
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [f"# {title}\n\n{intro}\n"],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": code_text.splitlines(keepends=True),
            },
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.8.0",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    return nb


def load_main(course):
    path = os.path.join(BASE, course, "main.py")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def make_code_snippet(code_raw):
    # 去掉 matplotlib.use("Agg") 以在笔记本中显示；添加 %matplotlib inline
    lines = code_raw.splitlines()
    new_lines = []
    for l in lines:
        if 'matplotlib.use("Agg")' in l or "matplotlib.use('Agg')" in l:
            new_lines.append("# notebook 模式不使用 Agg 后端")
            continue
        new_lines.append(l)
    # 在 imports 后加入 %matplotlib inline
    inserted = False
    final = []
    for l in new_lines:
        final.append(l)
        if (not inserted) and (l.startswith("import ") or l.startswith("from ")):
            # 找下一个空行插入
            continue
    head = ["%matplotlib inline\n"]
    return "\n".join(head + new_lines) + "\n"


def main():
    for course, meta in COURSES_META.items():
        code_raw = load_main(course)
        code = make_code_snippet(code_raw)
        nb = make_notebook(code, meta["title"], meta["intro"])
        out_path = os.path.join(BASE, course, "notebook.ipynb")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
        print(f"[NB] {out_path} 已生成")


if __name__ == "__main__":
    main()
