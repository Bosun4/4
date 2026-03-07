import os
import requests
import json
from datetime import datetime

# 从 GitHub Secrets 获取 Key
API_KEY = os.getenv("OPENAI_API_KEY")
URL = "https://nan.meta-api.vip/v1/chat/completions"

# 这里是你明天爬虫抓取到的数据，目前用占位符代替
today_matches = "今日竞彩赛事数据：获取自 500.com 和 澳客..." 

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

payload = {
    "model": "gpt-5.4",
    "messages": [
        {
            "role": "system",
            "content": "你是一个顶尖的足球数据分析师。你需要结合历史数据、赔率模型（ELO/泊松），每天分析竞彩足球比赛。请推荐胜率最高的4场比赛，并给出精准的比分预测、概率和详细理由。输出适合网页前端展示的 Markdown 格式。"
        },
        {
            "role": "user",
            "content": f"请分析以下今天的比赛数据，并给出预测：\n{today_matches}"
        }
    ]
}

print("正在请求 GPT-5.4 接口进行深度预测...")
response = requests.post(URL, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    result = response.json()
    prediction_text = result['choices'][0]['message']['content']
    
    # 写入文件供前端 UI 读取
    os.makedirs("site/data", exist_ok=True)
    with open(f"site/data/prediction_{datetime.now().strftime('%Y%m%d')}.md", "w", encoding="utf-8") as f:
        f.write(prediction_text)
    print("✅ 预测成功！结果已保存。")
else:
    print(f"❌ 请求失败，状态码: {response.status_code}")
    print(response.text)
