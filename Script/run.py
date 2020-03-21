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