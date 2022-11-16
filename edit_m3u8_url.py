# -*- coding: utf-8 -*-
# @Author: kenis
# @File: edit_m3u8_url.py


import os
import pprint
import re
import shutil
from get_key import main as get_key

def change_file_re(_file, old_str, new_str):
    """修改文件内容（正则替换字符）

    :param _file:
    :param old_str:
    :param new_str:
    :return:
    """
    with open(_file, "r", encoding="utf-8") as f1, open("%s.bak" % _file, "w", encoding="utf-8") as f2:
        for line in f1:
            f2.write(re.sub(old_str, new_str, line))
    os.remove(_file)
    os.rename("%s.bak" % _file, _file)


def add_file_name(_name, _file):
    """补全ts文件路径

    :param _name:
    :param _file:
    :return:
    """
    pprint.pp(_file)
    # encrypt-k-vod.xet.tech 的替换方式
    # add_url_before = 'https://' + '/'.join(_file.split('_')[1:]) + '/' + _name
    # pri-cdn-tx.xiaoeknow.com 的替换需要找到去浏览器开发者工具网络里找到.ts
    add_url_before = 'https://encrypt-k-vod.xet.tech/2919df88vodtranscq1252524126/2e4384cd3701925920946505975/drm/' + _name
    pprint.pp(add_url_before)
    file_name = 'test/m3u8/' + _file + '/m3u8.m3u8'
    pprint.pp(file_name)
    change_file_re(file_name, _name, add_url_before)
    change_file_re(file_name, '&type=mpegts',
                   '&type=mpegts&sign=5f68853f59e509cd7935220112d198df&t=63750347&us=UxbDLKViRj')


def main():
    path = "test/m3u8"  # 文件夹目录
    if os.path.isdir(path):
        print('开始删除test/m3u8')
        shutil.rmtree(path)
    print('开始复制m3u8到test')
    shutil.copytree('m3u8', path)

    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    files.sort(key=lambda x: int(x.split("_")[0]))  # 关键在于如何取出文件中的数字字符，然后对数字进行排序

    for file in files:
        if ('encrypt-k-vod.xet.tech' in file):
            add_file_name('v.f1228559', file)

        if ('pri-cdn-tx.xiaoeknow.com' in file):
            add_file_name('v.f421220.ts', file)
            # 读取m3u8第五行的key的URI
            out_index = file.split('_')[0]
            file_name = 'test/m3u8/{}/m3u8.m3u8'.format(file)
            with open(file_name) as f:
                key_uri = f.readlines()[10].split('"')[1]
                key = get_key(key_uri)
                print('./N_m3u8DL-CLI_v3.0.2 "D:/shared/get_xet_video/{in_file}" --headers "Referer: https://v.51doit.cn/" --saveName "{out_file}" --useKeyBase64 "{key}" --enableDelAfterDone'.format(in_file=file_name,out_file=out_index,key=key))
                print(' ')

if __name__ == '__main__':
    main()
