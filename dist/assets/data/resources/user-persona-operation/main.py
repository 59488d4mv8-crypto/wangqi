# -*- coding: utf-8 -*-
"""user-persona-operation：用户画像 K-Means 聚类分析"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

sns.set(style="whitegrid", font="DejaVu Sans")
plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

FEATURES = ["近90天学习天数", "近90天学习分钟数", "近90天消费金额元", "近90天互动次数", "完成课程数", "平均考试分数"]


def load_data():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_data.csv")
    return pd.read_csv(path)


def choose_k(X_scaled, max_k=8):
    inertias, sil = [], []
    for k in range(2, max_k + 1):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        inertias.append(km.inertia_)
        sil.append(silhouette_score(X_scaled, labels))
    return list(range(2, max_k + 1)), inertias, sil


def plot_k_search(ks, inertias, sil):
    fig, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(ks, inertias, "bo-", label="inertia")
    ax1.set_ylabel("inertia")
    ax2 = ax1.twinx()
    ax2.plot(ks, sil, "rs-", label="silhouette")
    ax2.set_ylabel("silhouette")
    ax1.set_xlabel("K")
    ax1.set_title("K 值选择 (elbow + silhouette)")
    fig.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "k_search.png"), dpi=120)
    plt.close(fig)


def plot_clusters(df_scored, X_scaled):
    best_k = 4
    km = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    df_scored = df_scored.copy()
    df_scored["cluster"] = km.fit_predict(X_scaled).astype(str)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    sns.scatterplot(x="近90天学习分钟数", y="近90天消费金额元", hue="cluster",
                    data=df_scored, ax=axes[0], s=50, alpha=0.75, palette="Set2")
    axes[0].set_title("学习分钟 vs 消费金额（按聚类着色）")

    sns.scatterplot(x="平均考试分数", y="完成课程数", hue="cluster",
                    data=df_scored, ax=axes[1], s=50, alpha=0.75, palette="Set2")
    axes[1].set_title("分数 vs 完成课程数（按聚类着色）")
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cluster_scatter.png"), dpi=120)
    plt.close(fig)

    means = df_scored.groupby("cluster")[FEATURES].mean()
    fig, ax = plt.subplots(figsize=(10, 5))
    norm_means = (means - means.min()) / (means.max() - means.min() + 1e-9)
    norm_means.plot(kind="bar", ax=ax)
    ax.set_title("各人群画像特征均值（归一化后）")
    ax.set_ylabel("归一化值")
    plt.setp(ax.get_xticklabels(), rotation=0)
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1), fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "persona_bar.png"), dpi=120)
    plt.close(fig)

    return df_scored, means


def main():
    df = load_data()
    print("===== 用户画像 K-Means 聚类分析 =====")
    print(f"样本用户数：{len(df)}")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[FEATURES].astype(float))

    ks, inertias, sil = choose_k(X_scaled)
    plot_k_search(ks, inertias, sil)
    df_scored, means = plot_clusters(df, X_scaled)

    print("\n【K 搜索结果】silhouette 最高：")
    for k, s in zip(ks, sil):
        print(f"  K={k}: silhouette={s:.3f}")
    print("\n【各人群特征均值】")
    print(means.round(2))
    print("\n【各人群人数】")
    print(df_scored["cluster"].value_counts().sort_index())
    print("已生成图表：k_search.png, cluster_scatter.png, persona_bar.png")


if __name__ == "__main__":
    main()
