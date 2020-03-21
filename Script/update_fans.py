import argparse, csv
import utils.tools as Tools
from model.user import User


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=str, default='')
    args = parser.parse_args()
    config_file = args.c
    if config_file == '':
        crawler = Tools.config_parse()
    else:
        crawler = Tools.config_parse('../' + config_file)
    f = csv.reader(open('../' + crawler.csv_file, 'r'))
    headers = ['id', 'name', 'sex', 'level', '大会员', '官方', '粉丝数']
    fans = []
    for item in f:
        fans.append(User(item[0], item[1], item[2], item[3], item[4], item[5], item[6]))
    fans = fans[1:]
    print('载入完毕')
    fans.sort(key=lambda u: int(u.follower_num), reverse=True)
    crawler.all_fans = fans
    crawler.update_fans()
    Tools.write_csv(crawler.all_fans)
