from tools.push_tools import PushTool
import requests
import traceback
from urllib import parse
from datetime import datetime
from random import choice
import sys

success_num = 0
failure_num = 0
# cookie = PushTool.get_cookies()
start_time = datetime.now()


def http_push(url_list):
    while True:
        global success_num
        global failure_num
        global start_time
        referer = choice(url_list)
        r = choice(url_list)
        # print(referer, r)
        headers = {
            'User-Agent': PushTool.user_agent(),
            'Referer': referer,
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'api.share.baidu.com',
        }
        proxy = PushTool.get_proxy()
        # proxy = b''
        if isinstance(proxy, bytes):
            proxy = proxy.decode('utf8')
        proxies = {"http": "http://{proxy}".format(proxy=proxy)}
        payload = {
            'l': referer,
            'r': r
        }
        code = 404
        url = ''
        temp = 0
        while temp < 2:
            try:
                r = parse.quote_plus(r)
                url = 'http://api.share.baidu.com/s.gif?r=%s&l=%s' % (r, referer)
                res = requests.get(url, params=payload, timeout=10, headers=headers, proxies=proxies)
                # res = requests.get(url, params=payload, timeout=10, headers=headers)
                code = res.status_code
                url = parse.unquote(res.url)
                if code == 200:
                    if url == 'http://www.baidu.com/search/error.html':
                        failure_num += 1
                    else:
                        success_num += 1
                else:
                    failure_num += 1
            except:
                # traceback.print_exc()
                failure_num += 1
            this_time = datetime.now()
            spend = this_time - start_time
            if int(spend.seconds) == 0:
                speed_sec = success_num / 1
            else:
                speed_sec = success_num / int(spend.seconds)
            speed_day = float('%.2f' % ((speed_sec * 60 * 60 * 24) / 10000000))
            percent = success_num / (failure_num + success_num) * 100
            sys.stdout.write(' ' * 100 + '\r')
            sys.stdout.flush()
            print(referer, code, proxy)
            # sys.stdout.write(
            #     '%s 成功%s 预计(day/千万):%s M 成功率:%.2f%% 状态码:%s \r'
            #     % (datetime.now(), success_num, speed_day, percent, code))
            sys.stdout.write(
                '%s 成功%s 预计(day/千万):%s M 成功率:%.2f%% 状态码:%s\r'
                % (datetime.now(), success_num, speed_day, percent, code))
            temp += 1
