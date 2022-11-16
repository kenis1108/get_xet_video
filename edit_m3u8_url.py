# -*- coding: utf-8 -*-
# @Author: kenis
# @File: edit_m3u8_url.py
"""
1. 获取文件加列表
2. 替换ts文件url
3. 获取key
4. 利用N_m3u8DL-CLI_v3.0.2下载mp4
"""

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


def add_file_name(_name, _file, _id, _type):
    """补全ts文件路径

    :param _name:
    :param _file:
    :param _id:
    :param _type:
    :return:
    """
    # pri-cdn-tx.xiaoeknow.com 的替换需要找到去浏览器开发者工具网络里找到.ts
    add_url_before = 'https://encrypt-k-vod.xet.tech/2919df88vodtranscq1252524126/{}/drm/'.format(_id) + _name
    file_name = 'test/m3u8/' + _file + '/m3u8.m3u8'
    change_file_re(file_name, _name, add_url_before)
    change_file_re(file_name, '&type=mpegts', _type)


def add_file_name1(_name, _file):
    """补全ts文件路径

    :param _name:
    :param _file:
    :return:
    """
    # pprint.pp(_file)
    # encrypt-k-vod.xet.tech 的替换方式
    add_url_before = 'https://' + '/'.join(_file.split('_')[1:]) + '/' + _name
    # pprint.pp(add_url_before)
    file_name = 'test/m3u8/' + _file + '/m3u8.m3u8'
    # pprint.pp(file_name)
    change_file_re(file_name, _name, add_url_before)


def main():
    path = "test/m3u8"  # 文件夹目录
    if os.path.isdir(path):
        print('开始删除test/m3u8')
        shutil.rmtree(path)
    print('开始复制m3u8到test')
    shutil.copytree('m3u8', path)

    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    files.sort(key=lambda x: int(x.split("_")[0]))  # 关键在于如何取出文件中的数字字符，然后对数字进行排序

    id_type_list = [
        {'id': 'ed7407783701925920300204578',
         'type': '&type=mpegts&sign=b0bf8427b8f45e71a4fa9dac44c38ac5&t=63753144&us=uDblYkSlae', 'time': '29:20'},
        {'id': '2b4022983701925920304680260',
         'type': '&type=mpegts&sign=ef8a2b6572e8048d42d48adbe3f57698&t=6375316f&us=AdkwKZHfLc', 'time': '31:32'},
        {'id': 'fbcc61603701925920300852685',
         'type': '&type=mpegts&sign=bd82c8468c25dc9ba2df8c59954d15d2&t=63753199&us=PuUJPWtFKj', 'time': '20:28'},
        {'id': 'db9a259b3701925920303537524',
         'type': '&type=mpegts&sign=d692b9d545a52ee4bdb262c4157f4bd2&t=637531ba&us=yLhOOwcdKY', 'time': '08:46'},
        {'id': '69e0e2233701925920166801675',
         'type': '&type=mpegts&sign=e8492312136b4714689a4778caa60137&t=637531d6&us=ALaOYZWbWh', 'time': '22:00'},
        {'id': '2afc41653701925920304648962',
         'type': '&type=mpegts&sign=805c3ac615f0ecc061e173a3b6630eea&t=637531fb&us=FPqoPsWuCE', 'time': '09:08'},

    ]

    index = 0
    for file in files:
        # if index == 2:
        #     break

        if ('encrypt-k-vod.xet.tech' in file):
            add_file_name1('v.f1228559', file)

        if ('pri-cdn-tx.xiaoeknow.com' in file):
            add_file_name('v.f421220.ts', file, id_type_list[index]['id'], id_type_list[index]['type'])
            # 读取m3u8第五行的key的URI
            out_index = file.split('_')[0]
            file_name = 'test/m3u8/{}/m3u8.m3u8'.format(file)
            with open(file_name) as f:
                key_uri = f.readlines()[10].split('"')[1]
                key = get_key(key_uri)
                cmd = 'D:/N_m3u8DL-CLI_v3.0.2_with_ffmpeg_and_SimpleG/N_m3u8DL-CLI_v3.0.2.exe "D:/shared/get_xet_video/{in_file}" --headers "Referer: https://v.51doit.cn/" --saveName "{out_file}" --useKeyBase64 "{key}" --enableDelAfterDone'.format(
                    in_file=file_name, out_file=out_index, key=key)
                print(cmd)
                print(' ')
                os.system(cmd)
            index += 1


if __name__ == '__main__':
    main()
