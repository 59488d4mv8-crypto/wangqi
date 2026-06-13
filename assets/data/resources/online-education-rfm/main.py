# -*- coding: utf-8 -*-
"""online-education-rfm：在线教育用户 RFM 分析"""
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


def load_data():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_data.csv")
    df = pd.read_csv(path)
    return df


def rfm_score(df):
    df = df.copy()
    df["R_score"] = pd.qcut(df["最近一次学习距今天数"], q=4, labels=[4, 3, 2, 1]).astype(int)
    df["F_score"] = pd.qcut(df["近90天学习次数"].rank(method="first"), q=4, labels=[1, 2, 3, 4]).astype(int)
    df["M_score"] = pd.qcut(df["近90天付费金额元"].rank(method="first"), q=4, labels=[1, 2, 3, 4]).astype(int)
    df["RFM_score"] = df["R_score"] + df["F_score"] + df["M_score"]

    def segment(row):
        r, f, m = row["R_score"], row["F_score"], row["M_score"]
        s = r + f + m
        if r >= 3 and f >= 3 and m >= 3:
            return "1-重要价值用户"
        elif r >= 3 and f <= 2 and m <= 2:
            return "2-新用户"
        elif r <= 2 and f >= 3 and m >= 3:
            return "3-重要唤回用户"
        elif r <= 2 and f <= 2 and m <= 2:
            return "4-流失用户"
        elif s >= 9:
            return "5-高价值用户"
        else:
            return "6-一般用户"

    df["人群分段"] = df.apply(segment, axis=1)
    return df


def plot_segments(df):
    cnt = df["人群分段"].value_counts().sort_index()
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    colors = sns.color_palette("Set2", len(cnt))
    axes[0].pie(cnt.values, labels=cnt.index, autopct="%1.1f%%", colors=colors, startangle=90)
    axes[0].set_title("人群分段占比饼图")

    sns.barplot(x=cnt.index, y=cnt.values, ax=axes[1], palette=colors)
    axes[1].set_title("人群分段数量柱状图")
    axes[1].set_ylabel("用户数")
    plt.setp(axes[1].get_xticklabels(), rotation=25, ha="right", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rfm_segments.png"), dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 5))
    pivot = df.groupby("人群分段")[["最近一次学习距今天数", "近90天学习次数", "近90天付费金额元"]].mean()
    pivot.plot(kind="bar", secondary_y=["近90天付费金额元"], ax=ax)
    ax.set_title("各人群 RFM 均值对比")
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rfm_means.png"), dpi=120)
    plt.close(fig)
    return cnt, pivot


def main():
    df = load_data()
    print("===== 在线教育 RFM 分析 =====")
    print(f"样本用户数：{len(df)}")
    print(df.describe().round(2))

    scored = rfm_score(df)
    cnt, pivot = plot_segments(scored)

    print("\n【人群分段分布】")
    for name, v in cnt.items():
        print(f"  {name}: {v} 人 ({v / len(scored):.1%})")
    print("\n【各人群 RFM 均值】")
    print(pivot.round(2))
    print("已生成图表：rfm_segments.png, rfm_means.png")


if __name__ == "__main__":
    main()
