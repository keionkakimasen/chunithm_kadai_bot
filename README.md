# CHUNITHM課題曲bot

CHUNITHMの課題曲をdiscordで発表します

# 必要
- DiscordのBotToken
- chunirecの開発者Token

適宜必要な環境変数を定義してください。

# 実行環境
- 環境変数を設定
  - CHUNITHM_DISCORD_BOT_TOKEN: Disocrd botのToken
  - CHUNIREC_TOKEN: chunirec開発者APIのToken
- poetryをインストールする
  - ```curl -sSL https://install.python-poetry.org | python3 -``` とかやる 
- 実行
  - ```poetry run python main.py```


# 使い方
- `/課題曲 <const>`
  - constの定数の譜面が選ばれる
  - const = 0でMAS,ULTから乱択
- `renewal.py`
  - 画像定義を更新します。
  - たまに実行してください(余裕があれば自動化を行いたい。)
  - 
