# -*- coding: utf-8 -*-
"""course-apriori：课程关联规则挖掘（Apriori）"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

try:
    from mlxtend.frequent_patterns import apriori, association_rules
    HAS_MLXTEND = True
except Exception:
    HAS_MLXTEND = False

sns.set(style="whitegrid", font="DejaVu Sans")
plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def load_data():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_data.csv")
    return pd.read_csv(path)


def build_basket(df):
    basket = df.groupby(["用户ID", "课程名"])["是否购买"].max().unstack().fillna(0).astype(bool)
    return basket


def run_apriori(basket, min_support=0.08, min_confidence=0.4):
    if HAS_MLXTEND:
        freq = apriori(basket, min_support=min_support, use_colnames=True)
        rules = association_rules(freq, metric="confidence", min_threshold=min_confidence)
        return freq, rules
    return None, None


def run_manual(basket, min_support=0.08):
    n = len(basket)
    support_items = (basket.sum() / n).sort_values(ascending=False)
    frequent = support_items[support_items >= min_support]

    pair_support = {}
    items = list(basket.columns)
    for i, a in enumerate(items):
        for b in items[i + 1:]:
            s = (basket[a] & basket[b]).mean()
            if s >= min_support:
                pair_support[(a, b)] = s
    return frequent, pair_support


def plot_bars(df, freq, basket):
    single = df.groupby("课程名")["用户ID"].nunique().sort_values(ascending=False)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.barplot(x=single.values, y=list(single.index), ax=axes[0], hue=list(single.index), palette="Blues_d", legend=False)
    axes[0].set_title("各课程购买用户数")
    axes[0].set_xlabel("用户数")

    co_occur = basket.astype(int).T.dot(basket.astype(int)).astype(int)
    co_occur = co_occur.copy()
    for c in co_occur.columns:
        co_occur.loc[c, c] = 0
    sns.heatmap(co_occur, annot=True, fmt="d", cmap="YlOrRd", ax=axes[1])
    axes[1].set_title("课程共同购买热力图")
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "course_association.png"), dpi=120)
    plt.close(fig)


def main():
    df = load_data()
    print("===== 课程关联规则挖掘 =====")
    print(f"样本用户数：{df['用户ID'].nunique()}，课程数：{df['课程名'].nunique()}，总记录：{len(df)}")
    basket = build_basket(df)
    freq, rules = run_apriori(basket)
    plot_bars(df, freq, basket)

    if HAS_MLXTEND:
        print(f"\n【频繁项集】共 {len(freq)} 个")
        print(freq.sort_values("support", ascending=False).head(10).to_string(index=False))
        print(f"\n【关联规则】共 {len(rules)} 条（按 lift 排序）")
        if not rules.empty:
            top = rules.sort_values("lift", ascending=False).head(10)[
                ["antecedents", "consequents", "support", "confidence", "lift"]]
            print(top.to_string(index=False))
    else:
        print("\nmlxtend 未安装，使用手动频次统计：")
        frequent, pair_support = run_manual(basket)
        print(f"单课程高频 (support ≥ 0.08): {len(frequent)} 个")
        print(frequent.round(3))
        if pair_support:
            pairs = sorted(pair_support.items(), key=lambda x: -x[1])[:10]
            print("\n二元频繁项集 Top10:")
            for (a, b), s in pairs:
                print(f"  {{{a}, {b}}}: support={s:.3f}")
    print("已生成图表：course_association.png")


if __name__ == "__main__":
    main()
