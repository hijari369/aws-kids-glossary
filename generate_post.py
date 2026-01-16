from datetime import date
import os
from openai import OpenAI

# GitHub Secrets の OPENAI_API_KEY を読む
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

THEME = "キャッシュってなに？なんで2回目は速いの？"

PROMPT = f"""
あなたは「小学生向けITコラム」の編集者です。
次の条件で、今日のコラムを1本書いてください。

【テーマ】{THEME}
【条件】
- 対象：小学生（むずかしい言葉は言い換える）
- 文字数：500〜650文字
- 1文は60文字以内（短く）
- 例え話を必ず2つ入れる（学校・家・ゲームなど）
- 最後に「今日のAWSことば」を1つだけ出す（1行で説明）
- 断定しすぎず、安心できる言い方にする

【出力形式】（この形を厳守）
<title>タイトル（28文字以内）</title>
本文（改行あり）
---
今日のAWSことば：◯◯（25文字以内で説明）
"""

res = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": PROMPT}],
)

content = res.choices[0].message.content
today = date.today().isoformat()

# posts フォルダが無いと失敗するので保険（.keep作ってればOK）
os.makedirs("posts", exist_ok=True)

# 今日の記事ファイル
post_path = f"posts/{today}.html"

html = f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{today} のITコラム</title>
</head>
<body style="font-family: system-ui, -apple-system, 'Hiragino Kaku Gothic ProN', 'Meiryo', sans-serif; line-height: 1.8; padding: 18px;">
  <h1>{today} のITコラム</h1>
  <div>{content.replace("\n", "<br>")}</div>
  <hr>
  <p><a href="../index.html">← 目次へ戻る</a></p>
</body>
</html>
"""

with open(post_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Created: {post_path}")
