# -*- coding:utf-8 -*-


from pymongo import MongoClient
import requests
import time
import DingTalk_link

# import zmail


class waliandata_save():
    def __init__(self):
        # 挖链指数以及交易所信息
        self.chainindex_url = 'https://api.walian.cn/coins/chainIndexDetail.open'
        # 货币信息基本信息
        self.coindata_url = 'https://api.walian.cn/coins/chainIndex.open'

        # 挖链指数的参数
        self.para = ['BTC', 'ETH', 'XRP', 'BCH', 'LTC', 'NEO', 'DASH', 'ETC', 'BTG', 'ZEC', 'HSR', 'BCX']

        self.database = '127.0.0.1:27017'

    # 抓取各种货币当前价格信息（nowPrice）
    def get_coinprice_info(self):
        info = []
        for i in self.para:
            url = self.coindata_url + '?en_name=' + i

            connect = requests.post(url)

            if connect.status_code == 200:
                data = connect.json()

                coin_info = data['data']['coinIndex']
                # 清洗数据
                for key in list(coin_info.keys()):
                    if key != 'nowPrice' and key != 'coinName':
                        del coin_info[key]
                coin_info['date'] = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                info.append(coin_info)
            else:

                ding = DingTalk_link.DingTalk_sendMessage()
                message = ' Waring: 网络连接失败'
                ding.send_text_message(message)

        # print(info)
        return info

    # 抓取各种货币交易信息：24h涨幅（range），7日涨幅（sevenRange），最新市值（marketValue），24h成交量（volume）。
    def get_cointrade_info(self):
        info = []
        for i in self.para:
            url = self.coindata_url + '?en_name=' + i
            # print(url)

            connect = requests.post(url)

            if connect.status_code == 200:
                data = connect.json()

                coin_info = data['data']['coinIndex']
                coin_info['date'] = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                info.append(coin_info)

            else:

                ding = DingTalk_link.DingTalk_sendMessage()
                message = ' Waring: 网络连接失败'
                ding.send_text_message(message)
        # print(info)
        return info

    # 抓取挖链指数信息：挖链指数（chainIndex），短期投资指数（investIndex），挖矿指数（miningIndex），被操控指数（controlIndex）。
    def get_walianindex_info(self):
        info = []
        for i in self.para:
            url = self.chainindex_url + '?en_name=' + i
            # print(url)

            connect = requests.post(url)

            if connect.status_code == 200:
                data = connect.json()

                exchang_info = data['data']['indexScoreCard']
                exchang_info['date'] = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                exchang_info['coinName'] = i
                info.append(exchang_info)

            else:

                ding = DingTalk_link.DingTalk_sendMessage()
                message = ' Waring: 网络连接失败'
                ding.send_text_message(message)
        # print(info)
        return info

    # 抓取交易所信息：交易所，最新成交价（newestTransactionPrice），24h最高（h24PriceMax），24 h最低（h24PriceMin）24h成交量

    def get_exchang_info(self, coinName):
        info = []
        connect = requests.post(self.coindata_url + '?en_name=' + coinName)

        if connect.status_code == 200:
            data = connect.json()

            exchang_info = data['data']['markets']
            for j in exchang_info:
                j['date'] = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                j['coinName'] = coinName
                del j['svg']
                info.append(j)

            # print(info)
            return info

        else:
            ding = DingTalk_link.DingTalk_sendMessage()
            message = ' Waring: 网络连接失败'
            ding.send_text_message(message)

    # 存储数据到数据库walian中的cionInfo表,exchangInfo表,walianInfo表
    def save_walian(self, biao, data):
        conn = MongoClient(self.database).walian
        if biao == 'coinInfo':
            collectinon = conn.coinInfo
            collectinon.insert(data)
        elif biao == 'exchangInfo':

            collectinon = conn.exchangInfo
            collectinon.insert(data)

        elif biao == 'walianInfo':
            collectinon = conn.walianInfo
            collectinon.insert(data)

        elif biao == 'tradeInfo':
            collectinon = conn.tradeInfo
            collectinon.insert(data)


    # 查询数据库walian
    def find_walian(self, biao, shuju):
        conn = MongoClient(self.database).walian
        if biao == 'coinInfo':
            collectinon = conn.coinInfo
            data = collectinon.find(shuju).sort([('date', -1)]).limit(4)
            return data

        elif biao == 'exchangInfo_5':

            collectinon = conn.exchangInfo
            data = collectinon.find(shuju).sort([('date', -1)]).limit(5)
            return data

        elif biao == 'walianInfo':
            collectinon = conn.walianInfo
            data = collectinon.find(shuju).sort([('date', -1)]).limit(2)
            return data

        elif biao == 'tradeInfo':
            collectinon = conn.tradeInfo
            data = collectinon.find(shuju).sort([('date', -1)]).limit(2)
            return data

        elif biao == 'exchangInfo_2':

            collectinon = conn.exchangInfo
            data = collectinon.find(shuju).sort([('date', -1)]).limit(2)
            return data

    # def send_email(self, title, content):
    #     server = zmail.server('fuzhengguo789@163.com', '123qwertyuiop')
    #     mail_content = {
    #         # 邮件标题
    #         'subject': title,
    #         # 邮件内容
    #         'content': content
    #
    #     }
    #
    #     server.send_mail(['fuzhengguo789@163.com', 'yangyefeng@xiaochong.com', 'lisongping@xiaochong.com'],
    #                      mail_content)
    #
    #     return '发送成功'
