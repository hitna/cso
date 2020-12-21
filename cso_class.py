import datetime
import time
import const
from slack_sdk import WebClient

class CountStamp:
    startdate = None
    startdatetime = None
    enddatetime = None
    stamp_counter = {}
    user_counter = {}
    client = None
    bot = None
    message = ""

    # インストラクタ
    def __init__(self):
        print("CountStamp Start")
        self.client = WebClient(const.USER_TOKEN)
        self.bot = WebClient(const.BOT_TOKEN)
        #Start of time
        self.startdate = datetime.date.today() - datetime.timedelta(days=const.DAYS_AGO)
        self.startdatetime = datetime.datetime.combine(self.startdate,datetime.time())
        self.enddatetime = self.startdatetime + datetime.timedelta(days=const.DAYS_TERM)
        print("term:{}-{}".format(self.startdatetime,self.enddatetime))  

    # チャンネルリストを取得する
    def setChannelList(self):
        self.channel_list = self.client.conversations_list(exclude_archived=True,limit=const.CHANNEL_LIMIT)
        print("channels:{}".format(len(self.channel_list["channels"])))
    
    # スタンプをカウントする
    def cntStamp(self):
        channel_cnt = 0
        for channel in self.channel_list["channels"]:
            channel_cnt = channel_cnt + 1
            channel_id = channel["id"]
            #apiの呼び出し回数の制限（1分間に50回まで）を回避する
            time.sleep(1)
            history = self.client.conversations_history(channel=channel_id,oldest=self.startdatetime.timestamp(),latest=self.enddatetime.timestamp())
            #スタンプをカウントする
            self.cntReactions(history=history,channel=channel)

    # 履歴内のスタンプをカウントする
    def cntReactions(self,history,channel):
        if(len(history['messages'])>0):
            print("channel_name:{} messages:{}".format(channel['name'],len(history['messages'])))
        for message in history["messages"]:
            try:
                if(message.get("reactions")):
                    for reaction in message["reactions"]:
                        self.cntUsers(users=reaction["users"])
                        key = reaction["name"]
                        if(self.stamp_counter.get(key)):
                            self.stamp_counter[key] = self.stamp_counter[key] + reaction["count"]
                        else:
                            self.stamp_counter[key] = reaction["count"]
            except KeyError as e:
                print("KeyError:")
                print(e.args)

    #スタンプしたユーザーをカウント
    def cntUsers(self,users):
        for user_id in users:
            if(self.user_counter.get(user_id)):
                self.user_counter[user_id] = self.user_counter[user_id] + 1
            else:
                self.user_counter[user_id] = 1

    # カウントをポストする
    def setMessage(self):
        sorted_stamp = sorted(self.stamp_counter.items(), key=lambda x:x[1], reverse=True)
        sorted_user = sorted(self.user_counter.items(), key=lambda x:x[1], reverse=True)

        w_list = ['月', '火', '水', '木', '金', '土', '日']
        self.message = "{}({})のスタンプランキングTOP{}を発表します。\n".format(self.startdate.strftime('%Y年%m月%d日'),w_list[self.startdate.weekday()],const.RANK_LIMIT)

        self.message = self.message + "\nこのスタンプが良く使われました:+1:\n"
        self.message = self.setRanking(sorted_stamp,False)
        
        self.message = self.message + "\nこのユーザーがたくさんスタンプしました:tera_感謝_赤:\n"
        self.message = self.setRanking(sorted_user,True)

        total_stamp = sum(self.stamp_counter.values())
        self.message = self.message + "\nすべてのスタンプを合計すると {} でした！".format(total_stamp)
        i = 1
        while i <=  int(total_stamp / const.CLAP_LOOP):
            self.message = self.message + ":clap:"
            i = i + 1
        self.message = self.message + "\n"

        self.message = self.message + "\nそれでは今日もたくさんスタンプしましょう！"

    def postMessage(self):
        self.bot.chat_postMessage(channel=const.CHANNEL_NAME, text=self.message)
    
    #ランキング処理
    def setRanking(self,rank_list,user_flag):
        rank = 1
        i = 0
        while i < len(rank_list):
            if(user_flag):
                self.message = self.message + '\n{}位 {} {}'.format(rank, self.getUsername(rank_list[i][0]),rank_list[i][1])
            else:
                self.message = self.message + '\n{}位 :{}: {}'.format(rank, rank_list[i][0],rank_list[i][1])
            #同列順位の処理
            j = 1
            while (i + j) < len(rank_list):
                if(rank_list[i][1] == rank_list[i+j][1]):
                    if(user_flag):
                        self.message = self.message + '  {} {}'.format(self.getUsername(rank_list[i+j][0]),rank_list[i+j][1])
                    else:
                        self.message = self.message + '  :{}: {}'.format(rank_list[i+j][0],rank_list[i+j][1])
                    j = j + 1
                else:
                    break
            i = i + j
            rank = rank + j
            if(rank > const.RANK_LIMIT):
                break
        self.message = self.message + '\n'
        return self.message
    
    #ユーザーの表示名を取得する
    def getUsername(self,user_id):
        user_info = self.bot.users_info(user=user_id)
        return user_info['user']['profile']['real_name']

    # デストラクタ
    def __del__(self):
        print("CountStamp End")