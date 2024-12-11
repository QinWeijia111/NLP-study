from flask import Flask, request, jsonify, render_template, send_file
import re
import requests
from bs4 import BeautifulSoup as BS
import time
import pandas as pd
import os
from transformers import pipeline
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import random

app = Flask(__name__)

# 用于存储链接信息的列表
link_list = []


@app.route("/")
def home():
    return render_template("frontend.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    # 获取请求中的数据
    data = request.get_json()
    video_link = data.get("video_link")
    model = data.get("model")
    print(model)
    if model == "model2":
        model = "/home/pod/shared-nvme/NLP-study/TextSequenceClassification/SentimentAnalysisOFBiliBiliPopUps/yiyanghkust/finbert-tone-chinese-finetuned-sentiment/checkpoint-72352"
    else:
        model = "/home/pod/shared-nvme/NLP-study/TextSequenceClassification/google-bert/bert-base-chinese-finetuned-sentiment/checkpoint-1430"
    if not video_link:
        return jsonify({"error": "视频链接不能为空"}), 400

    # 假设你有一个函数来获取B站视频的弹幕
    try:
        danmu_list = get_bilibili_comments(video_link)
    except Exception as e:
        return jsonify({"error": f"获取弹幕失败: {str(e)}"}), 500

    # 根据选择的模型进行情感分析
    try:
        results = analyze_danmu(danmu_list, model)
    except Exception as e:
        return jsonify({"error": f"情感分析失败: {str(e)}"}), 500

    # 返回情感分析结果
    return jsonify({"results": results})


@app.route("/generate_wordcloud", methods=["POST"])
def generate_wordcloud():
    data = request.get_json()
    video_link = data.get("video_link")

    # 调用函数生成弹幕列表（假设已有实现）
    danmu_list = get_bilibili_comments(video_link)
    text = " ".join(danmu_list)

    # 生成词云图
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white",
        font_path="TextSequenceClassification/SentimentAnalysisOFBiliBiliPopUps/frontend_and_backend/static/simkai.ttf",
    ).generate(text)
    img_buffer = io.BytesIO()
    wordcloud.to_image().save(img_buffer, format="PNG")
    img_buffer.seek(0)

    # 直接返回图片文件
    return send_file(img_buffer, mimetype="image/png")


def get_bilibili_comments(video_url):
    # 设置请求头
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.1.3162 SLBChan/105"
    }

    # 发送请求获取视频页面内容
    try:
        video_page = requests.get(video_url, headers=headers)
        video_page.encoding = video_page.apparent_encoding
    except Exception as e:
        print(f"请求视频页面失败: {e}")
        return []

    # 使用BeautifulSoup解析页面，提取CID
    soup = BS(video_page.text, "html.parser")
    cid = None
    for script in soup.find_all("script"):
        if "cid" in script.string:
            match = re.search(r'"cid":(\d+)', script.string)
            if match:
                cid = match.group(1)
                break

    if not cid:
        print("未能从视频页面提取到cid")
        return []

    # 获取评论数据
    url = f"https://comment.bilibili.com/{cid}.xml"
    try:
        r2 = requests.get(url, headers=headers)
        r2.encoding = r2.apparent_encoding
        comments = re.findall('<d p=".*?">(.*?)</d>', r2.text)
    except Exception as e:
        print(f"请求评论数据失败: {e}")
        return []

    return comments


def analyze_danmu(danmu_list, model):
    sentiment_analysis = pipeline("sentiment-analysis", model=model, device=0)
    results = []
    for danmu in danmu_list:
        out = sentiment_analysis(danmu)[0]
        out["content"] = danmu
        results.append(out)
    return results


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=7777)
