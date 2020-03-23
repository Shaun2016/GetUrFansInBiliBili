import os, csv
from model.user import User
import utils.tools as Tools

# 如果爬取中途失败，则要对生成的 csv 文件进行合并
if __name__ == '__main__':
    root_path = '../2020-03-23/'
    all_fans = []
    for file in os.listdir(root_path):
        fans = []
        with open(root_path + file, 'r') as f:
            f_csv = csv.reader(f)
            for line in f_csv:
                fans.append(User(line[0], line[1], line[2], line[3], line[4], line[5],
                                 line[6], line[7], line[8], line[9], line[10]))
            fans = fans[1:]
            fans.sort(key=lambda u: int(u.follower_num), reverse=True)
        all_fans += fans
        Tools.write_csv_all_attr(fans, root_path + file[:-4])
    all_fans.sort(key=lambda u: int(u.follower_num), reverse=True)
    Tools.write_csv_all_attr(all_fans, root_path + 'all')


