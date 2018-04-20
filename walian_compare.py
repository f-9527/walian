import unittest
from HTMLTestRunner import HTMLTestRunner
import schedule
import time
from bs4 import BeautifulSoup
import walian


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
                assert flag, (name + ' 货币实时价格 没有更新 ' + coin_data[0]['nowPrice'])

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
            assert flag, (name + ' 货币交易数据 没有更新')

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

            c_exchang = [exchang_data[0]['marketName'], exchang_data[1]['marketName'], exchang_data[2]['marketName'],
                         exchang_data[3]['marketName'], exchang_data[4]['marketName']]

            # 上一次的5个交易所和这次的是否一致
            if c_exchang == exchang:

                wa.save_walian('exchangInfo', exchang_save)
                for j in exchang:

                    # 查找对比
                    exchangs_data = wa.find_walian('exchangInfo_2', {'coinName': name, 'marketName': j})
                    flag = (exchangs_data[0]['newestTransactionPrice'] != exchangs_data[1]['newestTransactionPrice']) or \
                           (exchangs_data[0]['h24PriceMax'] != exchangs_data[1]['h24PriceMax']) or \
                           (exchangs_data[0]['h24PriceMin'] != exchangs_data[1]['h24PriceMin']) or \
                           (exchangs_data[0]['h24TransactionAmout'] != exchangs_data[1]['h24TransactionAmout'])

                    # 断言
                    assert flag, (name + j + ' 交易所数据 没有更新')

            else:
                wa.save_walian('exchangInfo', exchang_save)

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
            assert flag, (name + ' 挖链指数 没有更新')


if __name__ == '__main__':

    def run_coinprice():
        testsuite = unittest.TestSuite()
        testsuite.addTest(walian_data_update('test_coinprice_data'))

        with open('D:\\result.html', 'wb') as report:
            runner = HTMLTestRunner(stream=report, title='挖链实时数据对比', verbosity=2)
            runner.run(testsuite)

        html = open('D:\\result.html', encoding='utf-8')
        soup = BeautifulSoup(html.read(), 'lxml')
        td = soup.find(name='tr', id='total_row').find_all(name='td')
        if td[3].text != '0' or td[4].text != '0':
            content = soup.find(name='pre').text
            index = content.rfind('Error')
            errorinfo = content[index:len(content)]

            x = walian.waliandata_save()
            x.send_email(title='实时价格', content=errorinfo)

        html.close()


    def run_cointrade():
        testsuite = unittest.TestSuite()
        testsuite.addTest(walian_data_update('test_cointrade_data'))
        testsuite.addTest(walian_data_update('test_walianindex_data'))

        with open('D:\\result1.html', 'wb') as report:
            runner = HTMLTestRunner(stream=report, title='挖链实时数据对比', verbosity=2)
            runner.run(testsuite)

        html = open('D:\\result1.html', encoding='utf-8')
        soup = BeautifulSoup(html.read(), 'lxml')
        td = soup.find(name='tr', id='total_row').find_all(name='td')
        if td[3].text != '0' or td[4].text != '0':
            content = soup.find(name='pre').text
            index = content.rfind('Error')
            errorinfo = content[index:len(content)]

            x = walian.waliandata_save()
            x.send_email(title='货币24h交易信息以及挖链指数', content=errorinfo)

        html.close()


    def run_exchang():
        testsuite = unittest.TestSuite()
        testsuite.addTest(walian_data_update('test_exchang_data'))

        with open('D:\\result2.html', 'wb') as report:
            runner = HTMLTestRunner(stream=report, title='挖链实时数据对比', verbosity=2)
            runner.run(testsuite)

        html = open('D:\\result2.html', encoding='utf-8')
        soup = BeautifulSoup(html.read(), 'lxml')
        td = soup.find(name='tr', id='total_row').find_all(name='td')
        if td[3].text != '0' or td[4].text != '0':
            content = soup.find(name='pre').text
            index = content.rfind('Error')
            errorinfo = content[index:len(content)]

            x = walian.waliandata_save()
            x.send_email(title='交易所数据信息', content=errorinfo)

        html.close()


    schedule.every(3).minutes.do(run_coinprice)
    schedule.every(30).minutes.do(run_exchang)
    schedule.every(6).hours.do(run_cointrade)

    while True:
        schedule.run_pending()
        time.sleep(1)
