from model.crawler import Crawler
from decimal import Decimal
import csv, time


def config_parse(config_file='../config.txt'):
    with open(config_file, 'r') as f:
        up_id, cookie, last_id, page_size, thread_pool_size, csv_file = '', '', '', '', 0, ''
        for line in f.readlines():
            option, content = [ s.strip() for s in line.split(':')]
            if content == '':
                continue
            if option == 'id':
                up_id = content
            elif option == 'cookie':
                cookie = content
            elif option == 'last_id':
                last_id = content
            elif option == 'page_size':
                page_size = content
            elif option == 'thread_pool_size':
                thread_pool_size = int(content)
            elif option == 'csv_file':
                csv_file = content
        assert up_id != '', 'id 不能为空'
        assert cookie != '', 'cookie 不能为空'
        assert last_id != '', 'last_id 不能为空'
        assert thread_pool_size >= 0, '线程池中线程个数不能为负'
        crawler = Crawler(up_id, cookie, last_id)
        if page_size != '':
            crawler.page_size = page_size
        if thread_pool_size != 0:
            crawler.thread_pool_size = thread_pool_size
        if csv_file != '':
            crawler.csv_file = csv_file
    return crawler


# 统计男女，正式会员，大会员，官方账号，粉丝数范围
def statistic_fans(all_fans):
    boy, girl, member, vip, official = 0, 0, 0, 0, 0
    official_list = []
    up_list = []
    fans_nums = [0 for i in range(6)]
    for fan in all_fans:
        if fan.sex == '男':
            boy += 1
        elif fan.sex == '女':
            girl += 1
        if fan.vip_type == 1:
            member += 1
        elif fan.vip_type == 2:
            vip += 1
        if fan.official == 1:
            official += 1
            official_list.append(fan)
        if fan.follower_num < 1000:
            fans_nums[0] += 1
        elif fan.follower_num < 5000:
            fans_nums[1] += 1
        elif fan.follower_num < 10000:
            fans_nums[2] += 1
        elif fan.follower_num < 50000:
            fans_nums[3] += 1
        elif fan.follower_num < 100000:
            fans_nums[4] += 1
        elif fan.follower_num > 100000:
            fans_nums[5] += 1
        if fan.follower_num >= 10000:
            up_list.append(fan)
    # 将粉丝数过1W的阿婆主按粉丝数降序排列
    up_list.sort(key=lambda up: up.follower_num, reverse=True)
    log_content = '粉丝总数：' + str(len(all_fans)) + '\n'
    log_content += '男：' + str(boy) + '，' + fn(boy / (boy + girl)) + '\n'
    log_content += '女：' + str(girl) + '，' + fn(girl / (boy + girl)) + '\n'
    log_content += '正式会员：' + str(member) + '人，' + fn(member/len(all_fans)) + '\n'
    log_content += '大会员：' + str(vip) + '人，' + fn(vip/len(all_fans)) + '\n'
    log_content += '官方账号：' + str(official) + '个'
    if len(official_list) > 0:
        log_content += '，他们是：\n'
    for i in official_list:
        log_content += i.name + ', '
    log_content = log_content[:-2] + '\n'
    log_content += '粉丝的粉丝数：\n'
    log_content += '<1000\t' + str(fans_nums[0]) + '\t' + fn(fans_nums[0]/len(all_fans)) + '\n'
    log_content += '1000-5000\t' + str(fans_nums[1]) + '\t' + fn(fans_nums[1]/len(all_fans)) + '\n'
    log_content += '5000-1W\t' + str(fans_nums[2]) + '\t' + fn(fans_nums[2]/len(all_fans)) + '\n'
    log_content += '1W-5W\t' + str(fans_nums[3]) + '\t' + fn(fans_nums[3]/len(all_fans)) + '\n'
    log_content += '5W-10W\t' + str(fans_nums[4]) + '\t' + fn(fans_nums[4]/len(all_fans))+ '\n'
    log_content += '10W+\t' + str(fans_nums[5]) + '\t' + fn(fans_nums[5]/len(all_fans)) + '\n'
    log_content += '你的粉丝中粉丝数超过1W的有' + str(len(up_list)) + '个，他们是（粉丝数降序）：\n'
    for i in up_list:
        log_content += i.name + ', '
    log_content = log_content[:-2]
    log_content += '\n'
    print(log_content)
    with open('../log.txt', 'a', errors='ignore') as f:
        f.write(log_content)

def fn(num):
    return str(Decimal(num*100).quantize(Decimal('0.00'))) + '%'

def write_csv(all_fans, suffix=''):
    if suffix == '':
        suffix = str(len(all_fans))
    fans_list = [fan.attr_list() for fan in all_fans]
    headers = ['id', 'name', 'sex', 'level', '大会员', '官方', '粉丝数']
    file_name = time.strftime('%Y-%m-%d %H-%M', time.localtime()) + '_' + suffix + '.csv'
    with open('../' + file_name, 'w', newline='', errors='ignore') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(fans_list)

def write_csv_all_attr(all_fans, suffix=''):
    if suffix == '':
        suffix = time.strftime('%Y-%m-%d %H-%M-', time.localtime()) + str(len(all_fans))
    fans_list = [fan.attr_list_all() for fan in all_fans]
    headers = ['id', 'name', 'sex', 'level', '大会员', '官方', '粉丝数', '关注数', '播放数', '阅读数', '获赞数']
    file_path = suffix + '.csv'
    with open(file_path, 'w', newline='', errors='ignore') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(fans_list)

def seconds_format(cost):
    m, s = divmod(cost, 60)
    h, m = divmod(m, 60)
    if h == 0:
        return '%02d:%02d' % (m, s)
    return '%02d:%02d:%02d'% (h, m ,s)

