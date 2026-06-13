# -*- coding: utf-8 -*-
"""traffic-sales-timeseries：流量与销量时间序列分析"""
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
    df["日期"] = pd.to_datetime(df["日期"])
    df = df.sort_values("日期").reset_index(drop=True)
    return df


def moving_average_and_smooth(df, window=7, alpha=0.3):
    df = df.copy()
    df["访问量_MA7"] = df["访问量"].rolling(window=window, center=False).mean()
    df["访问量_EMA"] = df["访问量"].ewm(alpha=alpha, adjust=False).mean()
    df["销售额_MA7"] = df["销售额元"].rolling(window=window, center=False).mean()

    fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
    axes[0].plot(df["日期"], df["访问量"], label="原始访问量", color="#CCCCCC", linewidth=1)
    axes[0].plot(df["日期"], df["访问量_MA7"], label=f"{window}日移动平均", color="#4C72B0", linewidth=2)
    axes[0].plot(df["日期"], df["访问量_EMA"], label=f"指数平滑 α={alpha}", color="#DD8452", linewidth=2)
    axes[0].set_title("访问量时间序列与平滑")
    axes[0].legend(fontsize=8)

    axes[1].plot(df["日期"], df["销售额元"], label="原始销售额", color="#CCCCCC", linewidth=1)
    axes[1].plot(df["日期"], df["销售额_MA7"], label=f"{window}日移动平均", color="#55A868", linewidth=2)
    axes[1].set_title("销售额时间序列")
    axes[1].legend(fontsize=8)
    plt.setp(axes[1].get_xticklabels(), rotation=30, ha="right")
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "timeseries_smoothing.png"), dpi=120)
    plt.close(fig)
    return df


def forecast_next(df, horizon=14):
    last_date = df["日期"].iloc[-1]
    future = pd.date_range(last_date + pd.Timedelta(days=1), periods=horizon, freq="D")
    last_ma = df["访问量"].rolling(7).mean().iloc[-1]
    last_ema_v = df["访问量"].ewm(alpha=0.3, adjust=False).mean().iloc[-1]
    simple_pred = [last_ma] * horizon
    trend_pred = [last_ema_v + i * (df["访问量"].diff().mean()) for i in range(1, horizon + 1)]

    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(df["日期"], df["访问量"], color="#CCCCCC", label="历史访问量")
    ax.plot(df["日期"], df["访问量"].rolling(7).mean(), color="#4C72B0", label="历史 MA7")
    ax.plot(future, simple_pred, color="#DD8452", linestyle="--", label="常数预测(MA)")
    ax.plot(future, trend_pred, color="#55A868", linestyle="--", label="带趋势预测(EMA+漂移)")
    ax.set_title(f"未来 {horizon} 天访问量预测")
    ax.legend(fontsize=8)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "forecast_next.png"), dpi=120)
    plt.close(fig)
    return future, simple_pred, trend_pred


def weekly_heatmap(df):
    df = df.copy()
    df["weekday"] = df["日期"].dt.day_name()
    df["week"] = df["日期"].dt.isocalendar().week.astype(int)
    pivot = df.pivot_table(values="访问量", index="weekday", columns="week", aggfunc="mean")
    ordered = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    ordered = [d for d in ordered if d in pivot.index]
    pivot = pivot.reindex(ordered)
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.heatmap(pivot, cmap="YlOrRd", ax=ax, annot=True, fmt=".0f")
    ax.set_title("按周×星期的访问量热力图")
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "weekly_heatmap.png"), dpi=120)
    plt.close(fig)


def main():
    df = load_data()
    print("===== 流量与销量时间序列分析 =====")
    print(f"日期跨度：{df['日期'].min().date()} ~ {df['日期'].max().date()}（共 {len(df)} 天）")
    print(df[["访问量", "订单量", "销售额元", "新增注册"]].describe().round(0))
    df_smooth = moving_average_and_smooth(df)
    future, simple_pred, trend_pred = forecast_next(df_smooth)
    weekly_heatmap(df_smooth)
    print(f"\n未来首日预测访问量（常数 MA7）：{simple_pred[0]:.0f}")
    print(f"未来首日预测访问量（带趋势 EMA+漂移）：{trend_pred[0]:.0f}")
    print(f"未来末日预测访问量（带趋势 EMA+漂移）：{trend_pred[-1]:.0f}")
    print("已生成图表：timeseries_smoothing.png, forecast_next.png, weekly_heatmap.png")


if __name__ == "__main__":
    main()
