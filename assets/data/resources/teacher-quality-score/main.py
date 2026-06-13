# -*- coding: utf-8 -*-
"""teacher-quality-score：教师质量综合评分与雷达图"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid", font="DejaVu Sans")
plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

METRICS = ["学生满意度评分", "课程完成率百分比", "学员平均考试分数", "答疑响应小时", "每周直播小时数", "学员人数"]
# 指标方向：是否"越高越好"
HIGHER_BETTER = {"学生满意度评分": True, "课程完成率百分比": True, "学员平均考试分数": True,
                 "答疑响应小时": False, "每周直播小时数": True, "学员人数": True}


def load_data():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_data.csv")
    return pd.read_csv(path)


def standardize(df):
    df = df.copy()
    for col in METRICS:
        v = df[col].astype(float)
        mu, sigma = v.mean(), v.std()
        if sigma == 0:
            sigma = 1
        z = (v - mu) / sigma
        if not HIGHER_BETTER[col]:
            z = -z
        df[col + "_Z"] = z
    weights = {"学生满意度评分": 0.25, "课程完成率百分比": 0.2, "学员平均考试分数": 0.2,
               "答疑响应小时": 0.15, "每周直播小时数": 0.1, "学员人数": 0.1}
    df["综合评分"] = sum(df[c + "_Z"] * w for c, w in weights.items())
    df["排名"] = df["综合评分"].rank(ascending=False).astype(int)
    return df.sort_values("排名").reset_index(drop=True)


def radar_top(df, top_n=5):
    top = df.head(top_n)
    cols_norm = [c + "_Z" for c in METRICS]
    labels = METRICS
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    palette = sns.color_palette("tab10", len(top))
    for i, (_, row) in enumerate(top.iterrows()):
        vals = row[cols_norm].tolist()
        vals += vals[:1]
        ax.plot(angles, vals, color=palette[i], linewidth=2, label=row["教师姓名"])
        ax.fill(angles, vals, color=palette[i], alpha=0.15)

    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_title(f"教师质量综合雷达图（Top {top_n}）")
    ax.legend(loc="upper right", bbox_to_anchor=(1.2, 1.05), fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "teacher_radar.png"), dpi=120)
    plt.close(fig)


def score_bar(df):
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(x="教师姓名", y="综合评分", data=df, ax=ax, palette="viridis")
    for i, (_, row) in enumerate(df.iterrows()):
        ax.text(i, row["综合评分"] + 0.03, f"#{row['排名']}", ha="center", fontsize=9)
    ax.set_title("教师综合评分排名")
    ax.set_ylabel("综合评分(Z加权)")
    plt.setp(ax.get_xticklabels(), rotation=25, ha="right")
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "teacher_score_bar.png"), dpi=120)
    plt.close(fig)


def main():
    df = load_data()
    print("===== 教师质量综合评分 =====")
    print(f"参评教师数：{len(df)}")
    scored = standardize(df)
    radar_top(scored, top_n=min(5, len(scored)))
    score_bar(scored)
    print("\n【排名 Top5】")
    cols_show = ["排名", "教师姓名", "综合评分"] + METRICS
    print(scored[cols_show].head(10).round(2).to_string(index=False))
    print("\n已生成图表：teacher_radar.png, teacher_score_bar.png")


if __name__ == "__main__":
    main()
