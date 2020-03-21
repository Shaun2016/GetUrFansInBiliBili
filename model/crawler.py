import requests, json, time, random
from model.user import User
from utils.expection import RequestFailException, NoFansException
import utils.tools as Tools
from utils.Bar import Bar


class Crawler(object):
    def __init__(self, uid, cookie, last_id, page_size=500, thread_pool_size=5, csv_file=None):
        self.uid = uid
        self.cookie = cookie
        self.last_id = last_id
        self.page_size = page_size
        self.all_fans = {}
        # 初始化自己的粉丝数
        following, follower = self.user_following_follower(uid)
        # 计算总进度长度
        self.total_steps = int(follower / page_size)
        if follower % page_size > 0:
            self.total_steps += 1
        self.bar = Bar(self.total_steps, 'Fans Progress: ')
        self.csv_file = csv_file

    # 返回用户的关注数(following)，粉丝数(follower)
    def user_following_follower(self, mid):
        url = 'https://api.bilibili.com/x/relation/stat'
        querystring = {'vmid': mid, 'jsonp': 'jsonp', 'callback': '__jp11'}
        headers = {
            'Referer': 'https://space.bilibili.com/' + str(self.uid) + '/fans/fans',
            'Cache-Control': 'no-cache',
        }
        response = requests.request('GET', url, headers=headers, params=querystring)
        fan = json.loads(response.text[7:-1])
        return fan['data']['following'], fan['data']['follower']

    # 为用户设置关注数(following)和粉丝数(follower)
    def set_user_following_follower(self, u):
        assert isinstance(u, User), 'parameter u must be a instance of class User'
        following, follower = self.user_following_follower(u.mid)
        u.following_num = following
        u.follower_num = follower
        self.bar.update_once()


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
        error_time = 0
        while True:
            if error_time > 50:
                print('请求失败次数过多，请检查网络或配置信息，搜索终止')
                break
            # print('last_id', self.last_id)
            try:
                fans_one_page = self.fans_one_page()
            except RequestFailException as re:
                # print('error: ', re)
                error_time += 1
                continue
            except NoFansException as ne:
                print('finish: ', ne)
                break
            self.bar.update_once()
            self.all_fans |= fans_one_page
        print('粉丝获取完毕...')
        Tools.write_csv(self.all_fans, 'old')
        sorted(self.all_fans, key=lambda f: f.follower_num, reverse=True)
        print('保存数据完毕...\n开始更新粉丝信息...')
        # 按粉丝数降序排列
        self.update_fans()
        Tools.statistic_fans(self.all_fans)
        Tools.write_csv(self.all_fans, 'updated')

    # 更新所有粉丝信息
    def update_fans(self):
        self.bar = Bar(len(self.all_fans), 'Update Fans: ')
        # with ThreadPoolExecutor(5) as executor:
        #     for fan in self.all_fans:
        #         executor.submit(self.set_user_following_follower, fan)
        tmp = []
        for index, fan in enumerate(self.all_fans):
            self.set_user_following_follower(fan)
            tmp.append(fan)
            time.sleep(0.1)
            if (index + 1) % 60 == 0:
                time.sleep(random.randint(3, 6))    # 每请求60次睡眠3-6秒
            # 防止中途失败，每5000条保存一次
            group_num = 5000
            if (index + 1) % group_num == 0:
                Tools.write_csv(tmp, str(index-group_num+1) + '_' + str(index+1))
                print('  save the fans from %d-%d' % (index-group_num+1, index+1))
                tmp.clear()

