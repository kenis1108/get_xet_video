from selenium import webdriver
from browsermobproxy import Server

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# 开启Proxy：注意指定自己下载解压后路径
server = Server(r"F:\Software\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat")
server.start()
proxy = server.create_proxy()

# 配置Proxy启动WebDriver
options = Options()
options.add_argument("--start-maximized") #open Browser in maximized mode
options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
options.add_argument('--proxy-server={0}'.format(proxy.proxy))
options.add_argument('--incognito')
options.add_argument('--ignore-certificate-errors')
options.binary_location = r"C:\Users\24353\scoop\apps\googlechrome_ScoopInstaller\current\chrome.exe"    #chrome binary location specified here
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
service = Service(executable_path='../chromedriver.exe')
driver = webdriver.Chrome(options=options, service=service)

# 获取返回内容
base_url = "http://www.baidu.com"
proxy.new_har(options={'captureHeaders': True, 'captureContent': True})
driver.get(base_url)

result = proxy.har

for entry in result['log']['entries']:
    _url = entry['request']['url']
    print(_url)
    # # 根据URL找到数据接口
    # if "api/sysapi/p_sysapi" in _url:
    #     _response = entry['response']
    #     _content = _response['content']         # ['text']
    #     # 获取接口返回内容
    #     print(_content)

# 停止代理服务，退出selenium
server.stop()
driver.quit()