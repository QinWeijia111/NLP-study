# NLP-study

这是一个自然语言处理(NLP)学习项目，目前包含了文本分类应用（后续会继续添加其他应用）。
目前包含了 B 站弹幕情感分析系统的项目，前端采用 Bootstrap 5 框架，后端采用 Flask 框架。

## TextSequenceClassification 项目结构

```
NLP-study/
├── TextSequenceClassification/ # 文本分类相关代码
│ ├── requirements.txt # 项目依赖
│ ├── example.ipynb # BERT 模型微调示例代码
│ └── SentimentAnalysisOFBiliBiliPopUps/ # B 站弹幕情感分析项目
│ ├── frontend_and_backend/ # 前后端实现
│ │ ├── backend.py # Flask 后端服务
│ │ ├── gunicorn_config.py # Gunicorn 配置文件
│ │ ├── static/ # 静态资源文件
│ │ │ ├── bootstrap5/ # Bootstrap 5 框架文件
│ │ │ └── CSS/ # 自定义样式文件
│ │ └── templates/ # HTML 模板文件
│ └── data/ # 训练数据集
├── LICENSE # GNU GPL v3.0 开源协议
└── README.md # 项目说明文档
```

## 主要功能

### B 站弹幕情感分析系统

该系统提供以下功能：

- 支持输入 B 站视频链接自动获取弹幕
- 提供两种情感分析模型：
  - 二分类模型：基于 BERT-base-Chinese 微调，分类为正面/负面评论
  - 四分类模型：基于 FinBERT-tone-Chinese 微调，可识别更细粒度的情感
- 可视化功能：
  - 弹幕词云生成
  - 情感分析结果展示
  - 分析结果得分展示

### 模型说明

项目使用的预训练模型已开源在 Hugging Face:

- [二分类模型](https://huggingface.co/qinweijia/finbert-tone-chinese-finetuned-sentiment)
- [四分类模型](https://huggingface.co/qinweijia/distilbert-base-uncased-finetuned-cola)

## 使用说明

1. 运行 Web 服务

2. 访问系统
   打开浏览器访问: `http://localhost:7777`

## 开发指南

```python
cd TextSequenceClassification/SentimentAnalysisOFBiliBiliPopUps/frontend_and_backend
python backend.py
```

### 模型训练

可以参考`example.ipynb`中的代码进行模型训练，主要步骤包括：

1. 数据预处理
2. 模型微调
3. 模型评估
4. 模型保存

### API 说明

后端提供以下 API 接口：

- `/analyze`: POST 请求，进行弹幕情感分析
- `/generate_wordcloud`: POST 请求，生成弹幕词云图

## 开源协议

本项目采用 GNU General Public License v3.0 开源协议。详见 [LICENSE](LICENSE) 文件。

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。
