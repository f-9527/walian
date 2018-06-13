# -*- coding:utf-8 -*-

import schedule
import time
import walian
import DingTalk_link


# coininfo 对比（1分钟更新）

def coinprice_data():
    # 获取并存储
    wa = walian.waliandata_save()
    data = wa.get_coinprice_info()

    if not data:
        pass
    else:
        wa.save_walian('coinInfo', data)

        # 查找
        wa.para.pop()
        coinname = wa.para
        for name in coinname:

            coin_data = wa.find_walian('coinInfo', {'coinName': name})
            # 对比
            flag = (coin_data[0]['nowPrice'] != coin_data[1]['nowPrice']) or \
                   (coin_data[0]['nowPrice'] != coin_data[2]['nowPrice']) or \
                   (coin_data[0]['nowPrice'] != coin_data[3]['nowPrice'])

            # 断言
            if not flag:

                ding = DingTalk_link.DingTalk_sendMessage()
                message = (u'Waring: ' + name + u' 货币实时价格 没有更新 ' + str(coin_data[0]['nowPrice']))
                ding.send_text_message(message)


# cointradeinfo 对比（6小时更新）
def cointrade_data():
    # 获取并存储
    wa = walian.waliandata_save()
    data = wa.get_cointrade_info()
    if not data:
        pass

    else:
        wa.save_walian('tradeInfo', data)

        # 查找
        coinname = wa.para
        for name in coinname:
            trade_data = wa.find_walian('tradeInfo', {'coinName': name})

            # 对比
            flag = (trade_data[0]['range'] != trade_data[1]['range']) or \
                   (trade_data[0]['sevenRange'] != trade_data[1]['sevenRange']) or \
                   (trade_data[0]['marketValue'] != trade_data[1]['marketValue']) or \
                   (trade_data[0]['volume'] != trade_data[1]['volume'])

            # 断言
            if not flag:

                ding = DingTalk_link.DingTalk_sendMessage()
                message = 'Waring: ' + name + u' 货币交易数据 没有更新'
                ding.send_text_message(message)


# exchanginfo 对比（半小时更新）
def allexchang_data():
    wa = walian.waliandata_save()
    coinname = wa.para

    for name in coinname:

        # 获取
        exchang_save = wa.get_exchang_info(name)
        exchang = [exchang_save[0]['marketName'], exchang_save[1]['marketName'], exchang_save[2]['marketName'],
                   exchang_save[3]['marketName'], exchang_save[4]['marketName']]

        # 这次5个交易所是否出现重复
        if len(exchang) != len(set(exchang)):

            ding = DingTalk_link.DingTalk_sendMessage()
            message = name + u' 出现相同的交易所'
            ding.send_text_message(message)

        else:
            # 查上一次的交易所数据
            exchang_data = wa.find_walian('exchangInfo_5', {'coinName': name})

            c_exchang = [exchang_data[0]['marketName'], exchang_data[1]['marketName'], exchang_data[2]['marketName'],
                         exchang_data[3]['marketName'], exchang_data[4]['marketName']]

            wa.save_walian('exchangInfo', exchang_save)

            # 上一次的5个交易所和这次的是否一致
            if c_exchang == exchang:

                for j in exchang:
                    # 查找对比
                    exchangs_data = wa.find_walian('exchangInfo_2', {'coinName': name, 'marketName': j})
                    flag = (exchangs_data[0]['newestTransactionPrice'] != exchangs_data[1]['newestTransactionPrice']) or \
                           (exchangs_data[0]['h24PriceMax'] != exchangs_data[1]['h24PriceMax']) or \
                           (exchangs_data[0]['h24PriceMin'] != exchangs_data[1]['h24PriceMin']) or \
                           (exchangs_data[0]['h24TransactionAmout'] != exchangs_data[1]['h24TransactionAmout'])

                    # 断言
                    if not flag:

                        ding = DingTalk_link.DingTalk_sendMessage()
                        message = 'Waring: ' + name + j + u' 交易所数据 没有更新'
                        ding.send_text_message(message)


# walianinfo  对比（6小时更新）
def walianindex_data():
    # 获取并存储
    wa = walian.waliandata_save()
    data = wa.get_walianindex_info()
    if not data:
        pass

    else:
        wa.save_walian('walianInfo', data)

        # 查找
        coinname = wa.para
        for name in coinname:

            walian_data = wa.find_walian('walianInfo', {'coinName': name})

            # 对比
            flag = (walian_data[0]['chainIndex'] != walian_data[1]['chainIndex']) or \
                   (walian_data[0]['investIndex'] != walian_data[1]['investIndex']) or \
                   (walian_data[0]['miningIndex'] != walian_data[1]['miningIndex']) or \
                   (walian_data[0]['controlIndex'] != walian_data[1]['controlIndex'])

            # 断言
            if not flag:

                ding = DingTalk_link.DingTalk_sendMessage()
                message = 'Waring: ' + name + u' 挖链指数 没有更新'
                ding.send_text_message(message)


schedule.every(3).minutes.do(coinprice_data)
schedule.every(30).minutes.do(allexchang_data)
schedule.every(6).hours.do(cointrade_data)
schedule.every(6).hours.do(walianindex_data)

while True:
    schedule.run_pending()
    time.sleep(1)
