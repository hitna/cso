import cso_class
import sys, os
from slack_sdk.errors import SlackApiError

try:
    # スタンプをカウントするクラスを呼び出す
    cs = cso_class.CountStamp()
    # チャンネル一覧をセットする
    cs.setChannelList()
    # スタンプをカウントする
    cs.cntStamp()
    # メッセージを作成する
    cs.setMessage()
    # メッセージをポストする
    cs.postMessage()

except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    assert e.response["ok"] is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print(f"Got an error: {e.response['error']}")
    
except Exception as e:
    print('Unknown exception.')
    print(e)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print("{} {} line:{}".format(exc_type, fname, exc_tb.tb_lineno))
