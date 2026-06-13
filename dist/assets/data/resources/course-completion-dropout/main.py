# -*- coding: utf-8 -*-
"""course-completion-dropout：课程完成率与流失节点分析"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

sns.set(style="whitegrid", font="DejaVu Sans")
plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def load_data():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_data.csv")
    return pd.read_csv(path)


def chapter_funnel(df):
    by_chapter = df.groupby("章节顺序").agg(
        进入人数=("是否进入", "sum"),
        完成人数=("是否完成该章", "sum"),
        学习时长总和=("该章学习时长分钟", "sum"),
    ).reset_index()
    by_chapter["章节名"] = ["章节1-入门", "章节2-基础", "章节3-进阶", "章节4-实战", "章节5-综合"]
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(by_chapter["章节名"], by_chapter["进入人数"], marker="o", label="进入人数", color="#4C72B0")
    ax.plot(by_chapter["章节名"], by_chapter["完成人数"], marker="s", label="完成人数", color="#DD8452")
    ax.set_title("章节进入/完成漏斗")
    ax.set_ylabel("人数")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "chapter_funnel.png"), dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=by_chapter["章节名"], y=by_chapter["进入人数"], ax=ax, palette="Reds_d")
    for i, v in enumerate(by_chapter["进入人数"]):
        ax.text(i, v + 5, str(int(v)), ha="center")
    ax.set_title("章节进入人数漏斗图")
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "funnel_bars.png"), dpi=120)
    plt.close(fig)
    return by_chapter


def completion_prediction(df):
    user_level = df.groupby(["用户ID", "课程名"], as_index=False).agg(
        平均每章学习分钟=("该章学习时长分钟", "mean"),
        总学习分钟=("该章学习时长分钟", "sum"),
        最高进入章节=("章节顺序", "max"),
        完成章数=("是否完成该章", "sum"),
    )
    user_level["是否完成"] = (user_level["完成章数"] >= 5).astype(int)
    user_level["课程名_num"] = user_level["课程名"].factorize()[0]
    np.random.seed(42)
    user_level["中途暂停次数"] = np.random.poisson(3, len(user_level)) + (5 - user_level["最高进入章节"]).clip(lower=0)
    X = user_level[["平均每章学习分钟", "总学习分钟", "课程名_num", "中途暂停次数"]]
    y = user_level["是否完成"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    if len(set(y_train)) < 2:
        print("\n【课程完成预测】训练集只有一个类别，跳过训练。")
        return user_level, float("nan")
    model = LogisticRegression(max_iter=500)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\n【课程完成预测】准确率：{acc:.1%}")
    print("分类报告：")
    print(classification_report(y_test, y_pred, digits=3, zero_division=0))
    print(f"逻辑回归系数：{dict(zip(X.columns, model.coef_[0].round(3)))}")
    return user_level, acc


def main():
    df = load_data()
    print("===== 课程完成率与流失节点分析 =====")
    print(f"样本行数：{len(df)}，用户数：{df['用户ID'].nunique()}，课程数：{df['课程名'].nunique()}")
    by_chapter = chapter_funnel(df)
    user_level, acc = completion_prediction(df)
    print("\n【章节漏斗】")
    print(by_chapter)
    print(f"\n整体课程完成率：{user_level['是否完成'].mean():.1%}")
    print("已生成图表：chapter_funnel.png, funnel_bars.png")


if __name__ == "__main__":
    main()
