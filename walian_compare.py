# -*- coding:utf-8 -*-

import unittest
from HTMLTestRunner import HTMLTestRunner
import schedule
import time
from bs4 import BeautifulSoup
import walian
import DingTalk_link

class walian_data_update(unittest.TestCase):

    # coininfo 对比（1分钟更新）
    def test_coinprice_data(self):
        # 获取并存储
        wa = walian.waliandata_save()
        wa.save_walian('coinInfo', wa.get_coinprice_info())

        # 查找
        coinName = wa.para
        for name in coinName:

            if name == 'BCX':

                pass

            else:
                coin_data = wa.find_walian('coinInfo', {'coinName': name})
                # 对比
                flag = (coin_data[0]['nowPrice'] != coin_data[1]['nowPrice']) or \
                       (coin_data[0]['nowPrice'] != coin_data[2]['nowPrice']) or \
                       (coin_data[0]['nowPrice'] != coin_data[3]['nowPrice'])
                # 断言
                assert flag, ('Waring: ' + name + u' 货币实时价格 没有更新 ' + str(coin_data[0]['nowPrice']))

    # cointradeinfo 对比（6小时更新）
    def test_cointrade_data(self):
        # 获取并存储
        wa = walian.waliandata_save()
        wa.save_walian('tradeInfo', wa.get_cointrade_info())

        # 查找
        coinName = wa.para
        for name in coinName:
            trade_data = wa.find_walian('tradeInfo', {'coinName': name})

            # 对比
            flag = (trade_data[0]['range'] != trade_data[1]['range']) or \
                   (trade_data[0]['sevenRange'] != trade_data[1]['sevenRange']) or \
                   (trade_data[0]['marketValue'] != trade_data[1]['marketValue']) or \
                   (trade_data[0]['volume'] != trade_data[1]['volume'])

            # 断言
            assert flag, ('Waring: ' + name + u' 货币交易数据 没有更新')

    # exchanginfo 对比（半小时更新）
    def test_exchang_data(self):
        wa = walian.waliandata_save()
        coinName = wa.para

        for name in coinName:

            # 获取
            exchang_save = wa.get_exchang_info(name)
            exchang = [exchang_save[0]['marketName'], exchang_save[1]['marketName'], exchang_save[2]['marketName'],
                       exchang_save[3]['marketName'], exchang_save[4]['marketName']]

            # 这次5个交易所是否出现重复
            assert len(exchang) == len(set(exchang)), name + ' 出现相同的交易所'

            # 查上一次的交易所数据
            exchang_data = wa.find_walian('exchangInfo_5', {'coinName': name})

            wa.save_walian('exchangInfo', exchang_save)

            c_exchang = [exchang_data[0]['marketName'], exchang_data[1]['marketName'], exchang_data[2]['marketName'],
                         exchang_data[3]['marketName'], exchang_data[4]['marketName']]

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
                    assert flag, ('Waring: ' + name + j + u' 交易所数据 没有更新')

    # walianinfo  对比（6小时更新）
    def test_walianindex_data(self):

        # 获取并存储
        wa = walian.waliandata_save()
        wa.save_walian('walianInfo', wa.get_walianindex_info())

        # 查找
        coinName = wa.para
        for name in coinName:
            walian_data = wa.find_walian('walianInfo', {'coinName': name})

            # 对比
            flag = (walian_data[0]['chainIndex'] != walian_data[1]['chainIndex']) or \
                   (walian_data[0]['investIndex'] != walian_data[1]['investIndex']) or \
                   (walian_data[0]['miningIndex'] != walian_data[1]['miningIndex']) or \
                   (walian_data[0]['controlIndex'] != walian_data[1]['controlIndex'])

            # 断言
            assert flag, ('Waring: ' + name + u' 挖链指数 没有更新')


if __name__ == '__main__':

    url = 'https://oapi.dingtalk.com/robot/send?' \
          'access_token=15cef87df0d5c4aa60adf70c893840cba2b645855f68a2e6c3aaac48eac87f8f'
    ding = DingTalk_link.DingTalk_sendMessage(url)


    def run_coinprice():
        testsuite = unittest.TestSuite()
        testsuite.addTest(walian_data_update('test_coinprice_data'))

        with open('result.html', 'wb') as report:
            runner = HTMLTestRunner(stream=report, title=u'挖链实时数据对比', verbosity=2)
            runner.run(testsuite)

        html = open('result.html')
        soup = BeautifulSoup(html.read(), 'lxml')
        td = soup.find(name='tr', id='total_row').find_all(name='td')
        if td[3].text != '0' or td[4].text != '0':
            # 获取错误信息
            content = soup.find(name='pre').text
            # 去除空白
            result = content.strip()
            # 找到错误信息
            index = result.rfind('Error')
            errorinfo = result[(index + 6):len(result)].decode("unicode-escape")

            # 发送钉钉
            ding.send_text_message(errorinfo)

        html.close()


    def run_cointrade():
        testsuite = unittest.TestSuite()
        testsuite.addTest(walian_data_update('test_cointrade_data'))
        testsuite.addTest(walian_data_update('test_walianindex_data'))

        with open('result1.html', 'wb') as report:
            runner = HTMLTestRunner(stream=report, title=u'挖链实时数据对比', verbosity=2)
            runner.run(testsuite)

        html = open('result1.html')
        soup = BeautifulSoup(html.read(), 'lxml')
        td = soup.find(name='tr', id='total_row').find_all(name='td')
        if td[3].text != '0' or td[4].text != '0':
            content = soup.find(name='pre').text
            result = content.strip()
            index = result.rfind('Error')
            errorinfo = result[(index + 6):len(result)].decode("unicode-escape")
            ding.send_text_message(errorinfo)

        html.close()


    def run_exchang():
        testsuite = unittest.TestSuite()
        testsuite.addTest(walian_data_update('test_exchang_data'))

        with open('result2.html', 'wb') as report:
            runner = HTMLTestRunner(stream=report, title=u'挖链实时数据对比', verbosity=2)
            runner.run(testsuite)

        html = open('result2.html')
        soup = BeautifulSoup(html.read(), 'lxml')
        td = soup.find(name='tr', id='total_row').find_all(name='td')
        if td[3].text != '0' or td[4].text != '0':
            content = soup.find(name='pre').text
            result = content.strip()
            index = result.rfind('Error')
            errorinfo = result[(index + 6):len(result)].decode("unicode-escape")
            ding.send_text_message(errorinfo)

        html.close()


    schedule.every(3).seconds.do(run_coinprice)
    schedule.every(30).seconds.do(run_exchang)
    schedule.every(6).seconds.do(run_cointrade)

    while True:
        schedule.run_pending()
        time.sleep(1)
