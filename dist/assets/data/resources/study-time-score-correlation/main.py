# -*- coding: utf-8 -*-
"""study-time-score-correlation：学习时长与成绩相关性分析"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr

sns.set(style="whitegrid", font="DejaVu Sans")
plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def load_data():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_data.csv")
    return pd.read_csv(path)


def scatter_and_regression(df):
    x = df["学习时长分钟"].values.reshape(-1, 1)
    y = df["最终考试分数"].values
    model = LinearRegression().fit(x, y)
    y_pred = model.predict(x)
    r, p = pearsonr(df["学习时长分钟"], df["最终考试分数"])

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x="学习时长分钟", y="最终考试分数", hue="课程名", data=df, ax=ax, s=40, alpha=0.7)
    ax.plot(df["学习时长分钟"], y_pred, color="red", linewidth=2,
            label=f"拟合线 y={model.coef_[0]:.3f}x+{model.intercept_:.1f}")
    ax.set_title(f"学习时长 vs 考试分数（皮尔逊 r={r:.3f}, p={p:.2e}）")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scatter_regression.png"), dpi=120)
    plt.close(fig)
    return r, p, model


def box_by_pause(df):
    df = df.copy()
    df["暂停次数分组"] = pd.cut(df["暂停次数"], bins=[-1, 2, 4, 6, 99], labels=["0-2", "3-4", "5-6", "≥7"])
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.boxplot(x="暂停次数分组", y="最终考试分数", data=df, ax=ax, palette="Set2")
    ax.set_title("按暂停次数分组的分数箱线图")
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "box_pause_score.png"), dpi=120)
    plt.close(fig)


def main():
    df = load_data()
    print("===== 学习时长与成绩相关性分析 =====")
    print(f"样本用户数：{len(df)}")
    print(df.describe().round(2))
    r, p, model = scatter_and_regression(df)
    box_by_pause(df)
    print(f"\n皮尔逊相关系数 r = {r:.3f} (p={p:.2e})")
    print(f"线性回归：分数 = {model.coef_[0]:.3f} × 学习时长分钟 + {model.intercept_:.2f}")
    print(f"每多学习 60 分钟，预期分数增加 {model.coef_[0]*60:.2f} 分")
    print("已生成图表：scatter_regression.png, box_pause_score.png")


if __name__ == "__main__":
    main()
