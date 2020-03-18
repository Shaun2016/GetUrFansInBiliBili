import requests
import json
from model.user import User
from utils.expection import RequestFailException, NoFansException
import utils.tools as Tools


class Crawler(object):
    def __init__(self, uid, cookie, last_id, page_size=500):
        self.uid = uid
        self.cookie = cookie
        self.last_id = last_id
        self.page_size = page_size
        self.all_fans = set()

    # 返回用户的关注数，粉丝数
    def user_stat(self, mid):
        url = 'https://api.bilibili.com/x/relation/stat'
        querystring = {'vmid': mid, 'jsonp': 'jsonp', 'callback': '__jp11'}
        headers = {
            'Referer': 'https://space.bilibili.com/' + str(self.uid) + '/fans/fans',
            'Cache-Control': 'no-cache',
        }
        response = requests.request('GET', url, headers=headers, params=querystring)
        # print(response.text)
        fan = json.loads(response.text[7:-1])
        return fan['data']['following'], fan['data']['follower']

    # 返回用户个人信息
    def user_info(self):
        url = 'https://api.bilibili.com/x/space/acc/info'
        querystring = {'mid': self.uid, 'jsonp': 'jsonp'}
        headers = {
            'Cache-Control': 'no-cache',
        }
        response = requests.request('GET', url, headers=headers, params=querystring)
        data = json.loads(response.text)['data']
        user = User(data['mid'], data['name'], data['sex'], data['level'],
            data['vip']['type'], data['official']['type'], 0, data['coins'])
        return user

    # 返回粉丝列表, page_num 最大值为500
    def fans_one_page(self):
        url = "https://member.bilibili.com/x/h5/data/fan/list"
        querystring = {"ps": self.page_size, "last_id": self.last_id}
        headers = {
            'Cookie': self.cookie,
            'Cache-Control': "no-cache",
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        res = json.loads(response.text)
        if res['code'] != 0:
            raise RequestFailException('请求失败，请重试...')
        fans = res['data']['result']
        if len(fans) == 0:
            raise NoFansException('已经没有粉丝了...')
        fan_set = set()
        for fan in fans:
            u = User(fan['mid'], fan['card']['name'], fan['card']['sex'], fan['card']['level'],
                     fan['card']['vip']['type'], fan['card']['official']['type'], fan['follower'])
            fan_set.add(u)
        self.last_id = fans[-1]['mtime_id']
        return fan_set


    # 获取我的所有粉丝
    def get_my_all_fans(self):

        while True:
            print('last_id', self.last_id)
            try:
                fans_one_page = self.fans_one_page()
            except RequestFailException as re:
                print('error: ', re)
                continue
            except NoFansException as ne:
                print('finish: ', ne)
                break
            self.all_fans |= fans_one_page
        Tools.statistic_fans(self.all_fans)
        Tools.write_csv(self.all_fans)


if __name__ == '__main__':
    crawler = Tools.config_parse()
    crawler.get_my_all_fans()

