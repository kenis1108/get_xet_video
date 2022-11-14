# -*- coding: utf-8 -*-
# @Author: keins
# @File: getm3u8.py
"""
1. 打开网址
2. 等待扫码登录
3. 点击课程名
4. 滚动到底部
5. 获取课程列表
6. 回到顶部
7. 循环点击课程再点击回退
"""
import json
import os
import pprint
import shutil
import time
from pathlib import Path

import wget
from selenium.common import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from browsermobproxy import Server


def wait_click_btn(_driver: Chrome, selector, timeout, by):
    """等待按钮出现并点击按钮

    :param _driver:
    :param selector:
    :param timeout:
    :param by:
    :return:
    """
    num = 0
    while num < 2:
        try:
            WebDriverWait(_driver, timeout).until(ec.presence_of_element_located((by, selector)))
            break
        except StaleElementReferenceException as err:
            num += 1
            pprint.pp(err)

    btn = driver.find_element(by, selector)
    pprint.pp('开始点击{}'.format(btn.text))
    btn.click()
    time.sleep(3)
    pprint.pp('点击完毕')


def is_login(_driver: Chrome) -> str:
    """查看是否登录

    :param _driver: webdriver对象
    :return: userid
    """
    userid = _driver.execute_script("return window.__user_id")
    if userid:
        pprint.pprint("userid: {}".format(userid))
    return userid


def wait_qr_login(_driver: Chrome):
    """等待扫码登录并保存cookies

    :param _driver:
    :return:
    """
    # 等待60s手动扫码登录
    try:
        WebDriverWait(_driver, timeout=60).until(is_login)
    except TimeoutException as err:
        pprint.pprint('超时未扫码', err)

    pprint.pprint('登录成功')
    cookie = _driver.get_cookies()
    json_cookies = json.dumps(cookie)
    with open('cookie.json', 'w+', encoding='utf-8') as f:
        f.write(json_cookies)
        f.close()
        pprint.pp('cookies保存成功')
    _driver.get('https://appbt7csfy77461.h5.xiaoeknow.com/p/course/member/p_60e027a2e4b0151fc94c898b?type=3')


def login_with_cookie(_driver: Chrome):
    """添加cookie实现免登录

    :param _driver:
    :return:
    """
    # 添加cookie
    cookies_list = json.load(open('cookie.json', 'r', encoding='utf-8'))

    for cookie in cookies_list:
        _driver.add_cookie(cookie)

    pprint.pp('cookie添加成功')
    _driver.get('https://appbt7csfy77461.h5.xiaoeknow.com/p/course/member/p_60e027a2e4b0151fc94c898b?type=3')

    # 更新cookie
    cookie = _driver.get_cookies()
    json_cookies = json.dumps(cookie)
    with open('cookie.json', 'w+', encoding='utf-8') as f:
        f.write(json_cookies)
        f.close()
        pprint.pp('cookie更新成功')


def how_many_handle(_driver: Chrome):
    """获取当前浏览器的所有窗口句柄,判断是否是大于一个标签页，是就跳转到最新的标签页

    :param _driver:
    :return:
    """
    handles = _driver.window_handles
    if len(handles) > 1:
        pprint.pp(handles)
        driver.switch_to.window(handles[-1])
        return 1
    else:
        return 0


def scroll_find_ele(_driver: Chrome, by, value):
    """滚动到元素出现

    :param _driver:
    :param by:
    :param value:
    :return:
    """
    a = 0
    ele = ''
    while a < 10:
        _driver.execute_script('window.scrollBy(0,800)')  # 向下滚
        time.sleep(1)
        a += 1
        try:
            ele = _driver.find_element(by, value)
            _driver.execute_script("arguments[0].scrollIntoView();", ele)
            pprint.pp('找到"{}"'.format(ele.text))
            break
        except NoSuchElementException as err:
            pprint.pp('还没找到它')


def scroll_to_top(_driver: Chrome):
    """回到顶部

    :param _driver:
    :return:
    """
    time.sleep(2)
    _driver.execute_script('document.documentElement.scrollTop = 0')
    pprint.pp('回到顶部')


def start_webdriver_with_bmp(url: str):
    """启动浏览器判断是否存在cookie，存在就直接跳转到课程列表页并更新cookie，不存在就需要手动扫码登录后会保存cookie到json文件中.

    :param url:
    :return:
    """
    # 启动bmp代理服务
    _server = Server(r"F:\Software\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat")
    _server.start()
    _proxy = _server.create_proxy()

    # 浏览器启动配置
    options = Options()
    # options.debugger_address = "127.0.0.1:9222"
    options.binary_location = r"C:\Users\24353\scoop\apps\googlechrome_ScoopInstaller\current\chrome.exe"
    options.add_argument('--proxy-server={0}'.format(_proxy.proxy))
    options.add_argument("--start-maximized")  # 窗口最大化
    options.add_argument('--incognito')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
    # options.add_argument("proxy-server=socks5://127.0.0.1:1080")
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
    _proxy.new_har("xiaoertong", options={'captureHeaders': True, 'captureContent': True})
    _driver.get(url)

    # 判断cookie是否存在
    cookie_file = 'cookie.json'
    if os.path.exists(cookie_file):
        pprint.pp('{}存在'.format(cookie_file))
        sz = os.path.getsize(cookie_file)
        if not sz:
            pprint.pp('{}为空，需要扫码登录'.format(cookie_file))
            wait_qr_login(_driver)
        else:
            pprint.pp('{}不为空'.format(cookie_file))
            login_with_cookie(_driver)
    else:
        pprint.pp('{}不存在，需要扫码登录'.format(cookie_file))
        wait_qr_login(_driver)

    return _driver, _server, _proxy


if __name__ == '__main__':
    base_url = "https://appbt7csfy77461.h5.xiaoeknow.com/p/course/member/p_60e027a2e4b0151fc94c898b?type=3"
    dp = start_webdriver_with_bmp(base_url)
    driver = dp[0]
    server = dp[1]
    proxy = dp[2]

    wait_click_btn(driver,
                   'topics-item_main',
                   30, By.CLASS_NAME)

    a = 0
    while a < 5:
        scroll_find_ele(driver, By.CLASS_NAME, 'more')
        title_list = driver.find_elements(By.CLASS_NAME, 'content-title-wrapper')
        pprint.pp(len(title_list))
        scroll_to_top(driver)
        pprint.pp(title_list[a].get_attribute('class'))
        title_list[a].click()
        time.sleep(5)
        driver.back()
        a += 1

    # 删除m3u8文件夹
    if os.path.isdir('./m3u8'):
        pprint.pp('开始删除m3u8')
        shutil.rmtree('./m3u8')
        pprint.pp('m3u8删除完成')

    # 解析返回内容
    result = proxy.har
    index = 1
    for entry in result['log']['entries']:
        _url: str = entry['request']['url']
        # 根据URL找到数据接口
        if "m3u8" in _url:
            print(f'\033[1;35;47m{_url}\033[0m')
            dirname = "_".join(_url.split('/')[2:5])
            print('创建文件夹')
            mkdir = './m3u8/{}'.format('{}_'.format(index) + dirname)
            os.makedirs(mkdir)
            pprint.pp('开始下载m3u8')
            wget.download(_url, '{}/m3u8.m3u8'.format(mkdir))
            pprint.pp('下载m3u8完成')
            index += 1

    # 停止代理服务，退出selenium
    time.sleep(50)
    server.stop()
    driver.quit()
