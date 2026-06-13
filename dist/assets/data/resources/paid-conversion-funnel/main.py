# -*- coding: utf-8 -*-
"""paid-conversion-funnel：付费转化漏斗分析"""
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

STAGE_ORDER = ["访问", "注册", "试听", "付费"]


def load_data():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_data.csv")
    return pd.read_csv(path)


def funnel_overall(df):
    overall = df.groupby("阶段")["用户数"].sum().reindex(STAGE_ORDER)
    fig, ax = plt.subplots(figsize=(8, 4))
    colors = sns.color_palette("Blues_d", len(overall))
    bars = ax.bar(overall.index, overall.values, color=colors)
    for b, v in zip(bars, overall.values):
        ax.text(b.get_x() + b.get_width() / 2, v + max(overall) * 0.01, str(int(v)), ha="center")
    ax.set_title("整体付费转化漏斗")
    ax.set_ylabel("用户数")
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "funnel_overall.png"), dpi=120)
    plt.close(fig)
    return overall


def conversion_by_channel(df):
    pivot = df.pivot(index="渠道", columns="阶段", values="用户数").fillna(0)[STAGE_ORDER]
    pivot["注册转化率"] = pivot["注册"] / pivot["访问"]
    pivot["试听转化率"] = pivot["试听"] / pivot["注册"]
    pivot["付费转化率"] = pivot["付费"] / pivot["试听"]
    pivot["整体付费率"] = pivot["付费"] / pivot["访问"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    pivot[["注册转化率", "试听转化率", "付费转化率", "整体付费率"]].plot(kind="bar", ax=axes[0])
    axes[0].set_title("各渠道分阶段转化率")
    axes[0].set_ylabel("转化率")
    axes[0].tick_params(axis="x", rotation=25)

    for ch in pivot.index:
        axes[1].plot(STAGE_ORDER, [pivot.loc[ch, s] for s in STAGE_ORDER], marker="o", label=ch)
    axes[1].set_title("各渠道漏斗曲线")
    axes[1].set_ylabel("用户数")
    axes[1].legend()
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "conversion_by_channel.png"), dpi=120)
    plt.close(fig)
    return pivot


def main():
    df = load_data()
    print("===== 付费转化漏斗分析 =====")
    print(f"渠道数：{df['渠道'].nunique()}，总访问：{df[df['阶段']=='访问']['用户数'].sum()}")
    overall = funnel_overall(df)
    pivot = conversion_by_channel(df)
    print("\n【整体漏斗】")
    for s in STAGE_ORDER:
        print(f"  {s}: {int(overall[s])}")
    print(f"\n  访问→注册: {overall['注册']/overall['访问']:.1%}")
    print(f"  注册→试听: {overall['试听']/overall['注册']:.1%}")
    print(f"  试听→付费: {overall['付费']/overall['试听']:.1%}")
    print(f"  访问→付费(整体): {overall['付费']/overall['访问']:.1%}")
    print("\n【分渠道转化率(%)】")
    print((pivot[["注册转化率", "试听转化率", "付费转化率", "整体付费率"]] * 100).round(1))
    print("已生成图表：funnel_overall.png, conversion_by_channel.png")


if __name__ == "__main__":
    main()
