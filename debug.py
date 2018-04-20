import walian
from pymongo import MongoClient
from bs4 import BeautifulSoup
from HTMLTestRunner import HTMLTestRunner
import unittest
import schedule
import time
import requests



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