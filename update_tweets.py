import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
import re

# 取得したいXのユーザー名（デフォルト）
USERNAME = "public_cardigan"
RSS_URL = f"https://nitter.poast.org/{USERNAME}/rss"

try:
    req = urllib.request.Request(
        RSS_URL, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    tweets = []

    for item in root.findall('.//item'):
        title = item.find('title')
        pubDate = item.find('pubDate')
        
        text = title.text if title is not None else ""
        # HTMLタグの除去
        text = re.sub('<.*?>', '', text)
        
        date_str = pubDate.text if pubDate is not None else ""
        if date_str:
            try:
                dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
                date_str = dt.strftime("%Y年%m月%d日 %H:%M")
            except:
                pass

        tweets.append({
            "date": date_str,
            "text": text
        })
        
        if len(tweets) >= 10: # 最新10件を取得
            break

    # tweets.json に書き出す
    with open('tweets.json', 'w', encoding='utf-8') as f:
        json.dump(tweets, f, ensure_ascii=False, indent=2)
    print("Successfully updated tweets.json")

except Exception as e:
    print(f"Error fetching tweets: {e}")