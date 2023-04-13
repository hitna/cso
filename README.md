# slackのスタンプをカウントするアプリ
## 事前設定
* `local.py.sample` を同ディレクトリ内(main.pyが配置されているのと同じ場所)に `local.py` という名前でコピーする
* `local.py` 内の定数を適用したい環境のものに変更する

	```python
	#投稿先のチャンネル名
	CHANNEL_NAME = "#random"
	#OAuth Access Token
	USER_TOKEN = "xoxp-xxxx-xxxx-xxxx-xxxx"
	#Bot User OAuth Access Token
	BOT_TOKEN = "xoxb-xxxx-xxxx-xxxx"
	```

* slack APIでBOTに割り当てる権限
	* chat:write
	* users:read
* slack APIでUSERに割り当てる権限
	* channels:history
	* channels:read
	* groups:read
	* im:read
	* mpim:read
## 実行方法
* pythonで `main.py` を実行してください。
	```bash
	python main.py
	```
## 投稿イメージ
* 表示件数等の変更は、 `const.py` の数値を変更してください。
	```
	2020年11月22日のスタンプランキングを発表します。
	このスタンプが良く使われました:+1:
	1位 :おだんご: 3
	2位 :ハロウィーン: 2
	3位 :爆笑: 1
	このユーザーがたくさんスタンプしました:+1:
	1位 Aさん 3
	2位 Bさん 2
	3位 Cさん 1
	```
