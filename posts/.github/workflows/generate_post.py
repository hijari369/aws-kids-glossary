from datetime import date
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

THEME = "キャッシュってなに？なんで2回目は速いの？"

PROMPT = f"""
あなたは「小学生向けITコラム」の編集者です。

【テーマ】{THEME}
【条件】
- 対象：小学生
- 文字数：500〜650文字
- 1文は60文字以内
- 例え話を2つ以上
- 最後に「今日のAWSことば」を1つ

【出力形式】
<title>タイトル</title>
本文
---
今日のAWSことば：◯◯（一言）
"""

res = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": PROMPT}]
)

content = res.choices[0].message.content
today = date.today().isoformat()

content_html = content.replace("\n", "<br>")

html = f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{today} のITコラム</title>
</head>
<body style="font-family: system-ui, -apple-system, 'Hiragino Kaku Gothic ProN', 'Meiryo', sans-serif; line-height: 1.8; padding: 18px;">
  <h1>{today} のITコラム</h1>
  <div>{content_html}</div>
  <hr>
  <p><a href="../index.html">← 目次へ戻る</a></p>
</body>
</html>
"""


with open(f"posts/{today}.html", "w", encoding="utf-8") as f:
    f.write(html)
