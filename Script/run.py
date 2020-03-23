import utils.tools as Tools
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=str, default='')
    args = parser.parse_args()
    config_file = args.c
    if config_file == '':
        crawler = Tools.config_parse()
    else:
        crawler = Tools.config_parse('../' + config_file)
    crawler.get_my_all_fans()
    print('开始更新粉丝信息...')
    turn, num = 0, 5000
    while turn * num < len(crawler.all_fans):
        start = turn * num
        end = (turn + 1) * num
        crawler.update_fans(start=start, end=end)
        turn += 1
    Tools.write_csv_all_attr(crawler.all_fans, 'all')