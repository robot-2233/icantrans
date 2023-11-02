import argparse
import logging
import os
import sys
from datetime import datetime


def get_config():
    parser = argparse.ArgumentParser()
    base_lan = ['af', 'sq', 'am', 'ar', 'hy', 'as', 'ay', 'az', 'bm', 'eu', 'be', 'bn', 'bho', 'bs', 'bg', 'ca', 'ceb',
                'ny', 'zh-CN', 'zh-TW', 'co', 'hr', 'cs', 'da', 'dv', 'doi', 'nl', 'en', 'eo', 'et', 'ee', 'tl', 'fi',
                'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gn', 'gu', 'ht', 'ha', 'haw', 'iw', 'hi', 'hmn', 'hu', 'is', 'ig',
                'ilo', 'id', 'ga', 'it', 'ja', 'jw', 'kn', 'kk', 'km', 'rw', 'gom', 'ko', 'kri', 'ku', 'ckb', 'ky',
                'lo', 'la', 'lv', 'ln', 'lt', 'lg', 'lb', 'mk', 'mai', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mni-Mtei',
                'lus', 'mn', 'my', 'ne', 'no', 'or', 'om', 'ps', 'fa', 'pl', 'pt', 'pa', 'qu', 'ro', 'ru', 'sm', 'sa',
                'gd', 'nso', 'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tg', 'ta', 'tt',
                'te', 'th', 'ti', 'ts', 'tr', 'tk', 'ak', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu']
    '''Base'''
    parser.add_argument('--input_path', type=str, default='raw_data')
    parser.add_argument('--output_path', type=str, default='trans_data')
    parser.add_argument('--row_name', type=str, default='text')
    parser.add_argument('--fr', type=str, default='en', choices=base_lan+['auto'])
    parser.add_argument('--to', type=str, default=['zh-CN','ar',], nargs='+')

    '''Translate'''
    parser.add_argument('--queue_num', type=int, default=16)
    parser.add_argument('--batch_size', type=int, default=16)
    parser.add_argument('--crawler_speed', type=int, default=1, choices=[1, 2, 3, 4, 5])
    parser.add_argument('--save_scale', type=float, default=0.8, help='The scale of translation required, make sure <1')

    '''Clash_Proxy'''
    parser.add_argument('--local_host', type=str, default='127.0.0.1')
    parser.add_argument('--pp', type=str, default='7890')
    parser.add_argument('--cp', type=str, default='50609')
    # Controller port may change after restarting, please note

    args = parser.parse_args()

    if not os.path.exists(args.output_path):
        os.mkdir(args.output_path)

    '''middleware'''
    if not os.path.exists('temp'):
        os.mkdir('temp')

    '''logger'''
    args.log_name = '{}.log'.format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S')[2:])
    if not os.path.exists('logs'):
        os.mkdir('logs')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.addHandler(logging.FileHandler(os.path.join('logs', args.log_name)))
    return args, logger
