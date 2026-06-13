# -*- coding: utf-8 -*-
"""user-registration-activity：用户注册与活跃度分析"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid", font="DejaVu Sans")
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False


def load_data():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_data.csv")
    df = pd.read_csv(path)
    df["注册日期"] = pd.to_datetime(df["注册日期"])
    return df


def channel_distribution(df):
    cnt = df["注册渠道"].value_counts().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=cnt.index, y=cnt.values, ax=ax, palette="Blues_d")
    ax.set_title("各注册渠道用户数量")
    ax.set_xlabel("注册渠道")
    ax.set_ylabel("用户数")
    for i, v in enumerate(cnt.values):
        ax.text(i, v + max(cnt) * 0.01, str(v), ha="center")
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "channel_distribution.png"), dpi=120)
    plt.close(fig)
    return cnt


def date_trend(df):
    daily = df.groupby(df["注册日期"].dt.date).size().sort_index()
    dau = df.groupby(df["注册日期"].dt.date)["用户ID"].nunique().sort_index()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(daily.index.astype(str), daily.values, marker="o", label="当日注册数")
    ax.plot(dau.index.astype(str), dau.values, marker="s", label="DAU(去重用户数)")
    ax.set_title("注册日期趋势与 DAU")
    ax.set_xlabel("日期")
    ax.set_ylabel("人数")
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=8)
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "registration_trend.png"), dpi=120)
    plt.close(fig)
    return daily, dau


def retention_curve(df):
    d1 = df["是否次日留存"].mean()
    d7 = df["是否7日留存"].mean()
    by_ch = df.groupby("注册渠道")[["是否次日留存", "是否7日留存"]].mean()
    fig, ax = plt.subplots(figsize=(9, 4))
    x = np.arange(len(by_ch))
    w = 0.35
    ax.bar(x - w / 2, by_ch["是否次日留存"], w, label="次日留存率", color="#4C72B0")
    ax.bar(x + w / 2, by_ch["是否7日留存"], w, label="7日留存率", color="#DD8452")
    ax.set_xticks(x)
    ax.set_xticklabels(by_ch.index, rotation=20)
    ax.set_title("按渠道分组的留存率对比")
    ax.set_ylabel("留存率")
    ax.set_ylim(0, 1.0)
    for i, (a, b) in enumerate(zip(by_ch["是否次日留存"], by_ch["是否7日留存"])):
        ax.text(i - w / 2, a + 0.02, f"{a:.1%}", ha="center", fontsize=8)
        ax.text(i + w / 2, b + 0.02, f"{b:.1%}", ha="center", fontsize=8)
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "retention_by_channel.png"), dpi=120)
    plt.close(fig)
    return d1, d7, by_ch


def main():
    df = load_data()
    print("===== 用户注册与活跃度分析 =====")
    print(f"样本用户数：{len(df)}，注册渠道数：{df['注册渠道'].nunique()}，日期跨度：{df['注册日期'].min().date()} ~ {df['注册日期'].max().date()}")
    print(df.describe(include="all").round(2))

    cnt = channel_distribution(df)
    daily, dau = date_trend(df)
    d1, d7, by_ch = retention_curve(df)

    print("\n【渠道分布 Top3】")
    print(cnt.head(3))
    print(f"\n次日留存率：{d1:.1%}，7日留存率：{d7:.1%}")
    print(f"注册峰值日：{daily.idxmax()}（{daily.max()} 人）")
    print(f"DAU 峰值日：{dau.idxmax()}（{dau.max()} 人）")
    print("\n已生成图表：channel_distribution.png, registration_trend.png, retention_by_channel.png")


if __name__ == "__main__":
    main()
