#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json, numpy as np, pandas as pd

BASE = "/workspace/assets/data/resources"
np.random.seed(42)

COURSES = [
    "user-registration-activity",
    "course-completion-dropout",
    "online-education-rfm",
    "review-nlp-sentiment",
    "study-time-score-correlation",
    "paid-conversion-funnel",
    "course-apriori",
    "traffic-sales-timeseries",
    "teacher-quality-score",
    "user-persona-operation",
]

def save_df(df, path):
    df.to_csv(path, index=False, encoding="utf-8-sig")

def gen_user_registration_activity(out_dir):
    n = 480
    channels = np.random.choice(["官网","微信公众号","知乎","抖音","B站","朋友推荐"],size=n,p=[0.25,0.22,0.1,0.18,0.15,0.10])
    start = pd.Timestamp("2025-11-01")
    dates = [start + pd.Timedelta(days=np.random.randint(0,60)) for _ in range(n)]
    uids = [f"U{10000+i:06d}" for i in range(n)]
    ret1, ret7 = [], []
    base_map = {"官网":0.55,"微信公众号":0.6,"知乎":0.5,"抖音":0.35,"B站":0.45,"朋友推荐":0.7}
    for c in channels:
        b = base_map[c]
        ret1.append(1 if np.random.rand()<b else 0)
        ret7.append(1 if np.random.rand()<b*0.6 else 0)
    df = pd.DataFrame({"用户ID":uids,"注册渠道":channels,"注册日期":[d.strftime("%Y-%m-%d") for d in dates],
        "是否次日留存":ret1,"是否7日留存":ret7,"首次学习分钟数":np.random.randint(0,120,n)})
    save_df(df, os.path.join(out_dir,"sample_data.csv"))

def gen_course_completion_dropout(out_dir):
    n = 400
    chapters = ["章节1-入门","章节2-基础","章节3-进阶","章节4-实战","章节5-综合"]
    rows = []
    np.random.seed(7)
    for i in range(n):
        uid = f"U{20000+i:06d}"
        course = np.random.choice(["Python 数据分析","机器学习入门","Excel 高级应用"])
        max_chap = np.random.choice([1,2,3,4,5],p=[0.20,0.25,0.20,0.15,0.20])
        total_dur = np.random.randint(60,900)
        for j in range(1,6):
            if j <= max_chap:
                enter_flag = 1
                done_flag = 1 if j < max_chap else (1 if np.random.rand() < 0.9 else 0)
            else:
                enter_flag = 0
                done_flag = 0
            rows.append({"用户ID":uid,"课程名":course,"章节":chapters[j-1],"章节顺序":j,
                "是否进入":enter_flag,
                "是否完成该章":done_flag,
                "该章学习时长分钟":int(np.random.randint(10,80)) if enter_flag else 0,
                "总学习时长":total_dur})
    df = pd.DataFrame(rows)
    save_df(df, os.path.join(out_dir,"sample_data.csv"))

def gen_online_education_rfm(out_dir):
    n = 500
    uids = [f"U{30000+i:06d}" for i in range(n)]
    start = pd.Timestamp("2025-12-31")
    recency = np.random.randint(1,180,n)
    frequency = np.random.poisson(8,n)+1
    monetary = np.round(np.random.exponential(180,n)+50,2)
    df = pd.DataFrame({"用户ID":uids,"最近一次学习距今天数":recency,"近90天学习次数":frequency,
        "近90天付费金额元":monetary,"注册渠道":np.random.choice(["官网","微信","抖音","知乎","B站"],n),
        "最后学习日期":[(start-pd.Timedelta(days=int(r))).strftime("%Y-%m-%d") for r in recency]})
    save_df(df, os.path.join(out_dir,"sample_data.csv"))

def gen_review_nlp_sentiment(out_dir):
    n = 320
    positive_phrases = ["老师讲得很清晰案例丰富非常推荐","内容扎实答疑及时学习体验很好",
        "课程节奏合适知识点覆盖全面","老师很有耐心代码讲解细致入微",
        "性价比高课后作业有挑战性但能学到东西"]
    negative_phrases = ["节奏太快没基础跟不上","PPT太旧案例不够新","答疑回复慢课程体验一般",
        "部分章节跳过太多细节看不懂","内容偏浅不适合进阶学员"]
    labels, texts, scores = [], [], []
    for _ in range(n):
        if np.random.rand()<0.65:
            texts.append(np.random.choice(positive_phrases)); labels.append("正面"); scores.append(np.random.randint(4,6))
        else:
            texts.append(np.random.choice(negative_phrases)); labels.append("负面"); scores.append(np.random.randint(1,4))
    df = pd.DataFrame({"评论ID":[f"R{40000+i:06d}" for i in range(n)],
        "课程名":np.random.choice(["Python 数据分析","机器学习入门","Excel 高级应用","SQL 实战"],n),
        "评论内容":texts,"评分":scores,"人工情感标注":labels,
        "评论日期":[(pd.Timestamp("2025-11-01")+pd.Timedelta(days=np.random.randint(0,90))).strftime("%Y-%m-%d") for _ in range(n)]})
    save_df(df, os.path.join(out_dir,"sample_data.csv"))

def gen_study_time_score_correlation(out_dir):
    n = 300
    minutes = np.random.randint(30,600,n)
    noise = np.random.normal(0,8,n)
    score = np.clip(40+0.08*minutes+noise,0,100).round(1)
    pause = np.random.poisson(3,n)
    df = pd.DataFrame({"用户ID":[f"U{50000+i:06d}" for i in range(n)],
        "课程名":np.random.choice(["Python 数据分析","机器学习入门","SQL 实战"],n),
        "学习时长分钟":minutes,"暂停次数":pause,
        "章节完成率":np.clip(0.3+minutes/900+np.random.normal(0,0.1,n),0,1).round(3),
        "最终考试分数":score})
    save_df(df, os.path.join(out_dir,"sample_data.csv"))

def gen_paid_conversion_funnel(out_dir):
    channels = ["官网","微信","抖音","知乎","B站"]
    rows = []
    for c in channels:
        total = np.random.randint(800,1500)
        registered = int(total*np.random.uniform(0.25,0.45))
        trial = int(registered*np.random.uniform(0.35,0.55))
        paid = int(trial*np.random.uniform(0.15,0.35))
        rows.append({"渠道":c,"阶段":"访问","用户数":total})
        rows.append({"渠道":c,"阶段":"注册","用户数":registered})
        rows.append({"渠道":c,"阶段":"试听","用户数":trial})
        rows.append({"渠道":c,"阶段":"付费","用户数":paid})
    df = pd.DataFrame(rows)
    save_df(df, os.path.join(out_dir,"sample_data.csv"))

def gen_course_apriori(out_dir):
    courses = ["Python 数据分析","机器学习入门","SQL 实战","Excel 高级应用",
               "Tableau 可视化","统计学基础","深度学习实战","爬虫入门"]
    n = 250
    rows = []
    for i in range(n):
        uid = f"U{60000+i:06d}"
        k = np.random.randint(2,5)
        bought = np.random.choice(courses,k,replace=False)
        for c in bought:
            rows.append({"用户ID":uid,"课程名":c,"是否购买":1,"购买金额元":int(np.random.uniform(99,599))})
    df = pd.DataFrame(rows)
    save_df(df, os.path.join(out_dir,"sample_data.csv"))

def gen_traffic_sales_timeseries(out_dir):
    dates = pd.date_range("2025-10-01",periods=90,freq="D")
    n = len(dates)
    trend = np.linspace(800,1400,n)
    weekly = 150*np.sin(2*np.pi*dates.dayofweek/7)
    noise = np.random.normal(0,80,n)
    visits = (trend+weekly+noise).astype(int)
    df = pd.DataFrame({"日期":dates.strftime("%Y-%m-%d"),"访问量":visits,
        "订单量":(visits*np.random.uniform(0.03,0.06,n)).astype(int),
        "销售额元":(visits*np.random.uniform(0.04,0.08,n)*np.random.uniform(200,400,n)).astype(int),
        "新增注册":(visits*np.random.uniform(0.15,0.25,n)).astype(int)})
    save_df(df, os.path.join(out_dir,"sample_data.csv"))

def gen_teacher_quality_score(out_dir):
    teachers = ["王老师","李老师","张老师","刘老师","陈老师","杨老师","赵老师","黄老师","周老师","吴老师","孙老师","马老师"]
    rows = []
    for t in teachers:
        base = np.random.uniform(60,95)
        rows.append({"教师姓名":t,
            "学生满意度评分":float(round(float(np.clip(base+np.random.normal(0,3),50,100)),2)),
            "课程完成率百分比":float(round(float(np.clip(base-5+np.random.normal(0,4),30,100)),2)),
            "学员平均考试分数":float(round(float(np.clip(base+np.random.normal(0,4),40,100)),2)),
            "答疑响应小时":float(round(np.random.uniform(1,24),1)),
            "每周直播小时数":float(round(np.random.uniform(2,10),1)),
            "学员人数":int(np.random.randint(80,600))})
    df = pd.DataFrame(rows)
    save_df(df, os.path.join(out_dir,"sample_data.csv"))

def gen_user_persona_operation(out_dir):
    n = 360
    df = pd.DataFrame({"用户ID":[f"U{70000+i:06d}" for i in range(n)],
        "近90天学习天数":np.random.randint(1,80,n),
        "近90天学习分钟数":np.random.randint(60,6000,n),
        "近90天消费金额元":np.round(np.random.exponential(200,n),2),
        "近90天互动次数":np.random.poisson(20,n),
        "完成课程数":np.random.randint(0,6,n),
        "平均考试分数":np.clip(np.random.normal(75,10,n),0,100).round(1),
        "注册渠道":np.random.choice(["官网","微信","抖音","知乎","B站"],n)})
    save_df(df, os.path.join(out_dir,"sample_data.csv"))

GENERATORS = {
    "user-registration-activity": gen_user_registration_activity,
    "course-completion-dropout": gen_course_completion_dropout,
    "online-education-rfm": gen_online_education_rfm,
    "review-nlp-sentiment": gen_review_nlp_sentiment,
    "study-time-score-correlation": gen_study_time_score_correlation,
    "paid-conversion-funnel": gen_paid_conversion_funnel,
    "course-apriori": gen_course_apriori,
    "traffic-sales-timeseries": gen_traffic_sales_timeseries,
    "teacher-quality-score": gen_teacher_quality_score,
    "user-persona-operation": gen_user_persona_operation,
}

def main():
    os.makedirs(BASE, exist_ok=True)
    for c in COURSES:
        out_dir = os.path.join(BASE, c)
        os.makedirs(out_dir, exist_ok=True)
        GENERATORS[c](out_dir)
        print(f"[DATA] {c} sample_data.csv 已生成")

if __name__=="__main__":
    main()
