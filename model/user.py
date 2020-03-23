class User(object):
    def __init__(self, mid, name, sex, level, vip_type, official, follower_num, following_num=0, archive_view=0, article_view=0, likes=0):
        self.mid = mid
        self.name = name
        self.sex = sex
        self.level = level
        self.vip_type = vip_type
        self.official = official
        self.follower_num = follower_num    # 粉丝数
        self.following_num = following_num      # 关注数
        self.archive_view = archive_view   # 播放数
        self.article_view = article_view   # 阅读数
        self.likes = likes      # 获赞数

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
            ', 大会员: ' + str(vip_type()) + ', 认证机构: ' + str(official_type())

    def attr_list(self):
        return [self.mid, self.name, self.sex, self.level, self.vip_type, self.official, self.follower_num]

    def attr_list_all(self):
        attr = self.attr_list()
        attr.extend([self.following_num, self.archive_view, self.article_view, self.likes])
        return attr
