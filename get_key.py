# -*- coding: utf-8 -*-
# @Author: wuaipojie
# @File: get_key.py

import requests
import base64


def get_key_from_url(url: str, userid: str) -> str:
    """
    通过请求m3u8文件中的key的url,获取解密视频key的base64字符串密钥
    :param url: m3u8文件中获取key的url
    :param userid: 用户id，放视频时飘动的那一串
    :return: key的base64字符串
    """
    # url拼接uid参数
    url += f'&uid={userid}'
    # 发送get请求
    rsp = requests.get(url=url)
    rsp_data = rsp.content
    if len(rsp_data) == 16:
        userid_bytes = bytes(userid.encode(encoding='utf-8'))
        result_list = []
        for index in range(0, len(rsp_data)):
            result_list.append(
                rsp_data[index] ^ userid_bytes[index])
        print(result_list)
        return base64.b64encode(bytes(result_list)).decode()
    else:
        print(f"获取异常，请求返回值：{rsp.text}")
        return ''

def main(_url):
    _uid = 'u_6231b44824982_7dt7BKJ7MJ'
    _url = _url
    base64_key = get_key_from_url(url=_url, userid=_uid)
    print(base64_key)
    return base64_key

if __name__ == '__main__':
    main('https://app.xiaoe-tech.com/xe.basic-platform.material-center.distribute.vod.pri.get/1.0.0?app_id=appbt7csfy77461&mid=m_WX6h5sXcj1YAq_gZuQNhlD&urld=e7a53bdcb6a72c1b9b68790c3fc1d038')