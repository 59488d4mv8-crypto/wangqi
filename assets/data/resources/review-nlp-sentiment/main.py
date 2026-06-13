# -*- coding: utf-8 -*-
"""review-nlp-sentiment：评论情感与词频分析"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

try:
    import jieba
    HAS_JIEBA = True
except Exception:
    HAS_JIEBA = False

try:
    from wordcloud import WordCloud
    HAS_WC = True
except Exception:
    HAS_WC = False

sns.set(style="whitegrid", font="DejaVu Sans")
plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

STOPWORDS = {"的", "了", "是", "我", "也", "在", "都", "和", "有", "就",
             "很", "不", "太", "但", "与", "这", "那", "没", "还", "会",
             "老师", "课程", "学习", "内容", "章节", "案例", "学员", "用户"}


def load_data():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_data.csv")
    return pd.read_csv(path)


def tokenize(text):
    if HAS_JIEBA:
        return [w for w in jieba.lcut(text) if len(w) > 1 and w not in STOPWORDS]
    return [w for w in text.split() if len(w) > 1 and w not in STOPWORDS]


def sentiment_and_freq(df):
    df = df.copy()
    df["tokens"] = df["评论内容"].apply(tokenize)
    pos_tokens = sum(df.loc[df["人工情感标注"] == "正面", "tokens"].tolist(), [])
    neg_tokens = sum(df.loc[df["人工情感标注"] == "负面", "tokens"].tolist(), [])

    pos_top = Counter(pos_tokens).most_common(15)
    neg_top = Counter(neg_tokens).most_common(15)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    if pos_top:
        words, counts = zip(*pos_top)
        sns.barplot(x=list(counts), y=list(words), ax=axes[0], palette="Greens_d")
        axes[0].set_title("正面评论高频词 Top15")
    if neg_top:
        words, counts = zip(*neg_top)
        sns.barplot(x=list(counts), y=list(words), ax=axes[1], palette="Reds_d")
        axes[1].set_title("负面评论高频词 Top15")
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sentiment_freqwords.png"), dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4))
    cnt = df["人工情感标注"].value_counts()
    sns.barplot(x=cnt.index, y=cnt.values, ax=ax, palette=["#4C72B0", "#DD8452"])
    for i, v in enumerate(cnt.values):
        ax.text(i, v + 2, str(v), ha="center")
    ax.set_title("评论情感分布")
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sentiment_distribution.png"), dpi=120)
    plt.close(fig)

    if HAS_WC and pos_tokens:
        try:
            wc = WordCloud(width=800, height=400, background_color="white",
                           font_path=None, collocations=False).generate(" ".join(pos_tokens))
            fig, ax = plt.subplots(figsize=(9, 5))
            ax.imshow(wc, interpolation="bilinear")
            ax.axis("off")
            ax.set_title("正面评论词云")
            fig.tight_layout()
            fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "wordcloud_positive.png"), dpi=120)
            plt.close(fig)
        except Exception:
            pass

    return pos_top, neg_top


def main():
    df = load_data()
    print("===== 评论情感与词频分析 =====")
    print(f"样本评论数：{len(df)}，正面占比：{(df['人工情感标注']=='正面').mean():.1%}")
    print(f"分词器：{'jieba' if HAS_JIEBA else 'split(降级)'}，词云：{'可用' if HAS_WC else '不可用(跳过)'}")
    pos_top, neg_top = sentiment_and_freq(df)
    print("\n【正面高频词】", pos_top[:8])
    print("【负面高频词】", neg_top[:8])
    print("已生成图表：sentiment_freqwords.png, sentiment_distribution.png, wordcloud_positive.png")


if __name__ == "__main__":
    main()
