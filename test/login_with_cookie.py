# -*- coding: utf-8 -*-
# @Time: 2022/11/12 10:36
# @Author: kenis
# @File: login_with_cookie.py

import json

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import pprint


def open_url(url) -> Chrome:
    # 浏览器启动配置
    options = Options()
    options.binary_location = r"C:\Users\24353\scoop\apps\googlechrome_ScoopInstaller\current\chrome.exe"
    options.add_argument("--start-maximized")  # 窗口最大化
    options.add_argument('--incognito')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
    preferences = {
        "webrtc.ip_handling_policy": "disable_non_proxied_udp",
        "webrtc.multiple_routes_enabled": False,
        "webrtc.nonproxied_udp_enabled": False
    }
    options.add_experimental_option("prefs", preferences)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)  # 禁用 Chrome 自动化扩展
    options.add_experimental_option('detach', True)  # 不自动关闭浏览器

    service = Service(executable_path='chromedriver.exe')
    _driver = Chrome(options=options, service=service)

    # 打开网址
    _driver.get(url)
    return _driver


if __name__ == '__main__':
    base_url = "https://admin.xiaoe-tech.com/t/login?reg_source=0101&src_page=A#/wx"
    driver = open_url(base_url)
    # 添加cookie
    cookies_list = json.load(open('cookie.json', 'r', encoding='utf-8'))
    pprint.pprint(cookies_list)

    for cookie in cookies_list:
        driver.add_cookie(cookie)

    driver.get('https://admin.xiaoe-tech.com/t/account/muti_index?type=wx#/myParticipate')
    # 退出selenium
    # driver.quit()
