class User(object):
    def __init__(self, mid, name, sex, level, vip_type, official, follower_num, coins=0):
        self.mid = mid
        self.name = name
        self.sex = sex
        self.level = level
        self.vip_type = vip_type
        self.official = official
        self.follower_num = follower_num
        self.following_num = 0
        self.coins = coins

    def __str__(self):
        def vip_type():
            if self.vip_type == 0:
                return '无'
            if self.vip_type == 1:
                return '正式会员'
            if self.vip_type == 2:
                return '年度大会员'

        def official_type():
            if self.official == -1:
                return '无'
            if self.official == 1:
                return '官方认证'

        return 'id: ' + str(self.mid) + ', 昵称: ' + str(self.name) + ', 性别: ' + str(self.sex) + \
            ', 等级: ' + str(self.level) + ', 硬币数: ' + str(self.coins) + \
            ', 大会员: ' + vip_type() + ', 认证机构: ' + official_type()

    def attr_list(self):
        return [self.mid, self.name, self.sex, self.level, self.vip_type, self.official, self.follower_num]
