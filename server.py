# -*- coding: utf-8 -*-
import scrapy
import sqlite3
import os
import time
from selenium import webdriver
import random
import zipfile
from selenium.webdriver.common.by import By
import sqlite3
import time

pc_user_agent_list = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
    "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 ",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
]

# Chrome代理模板插件(https://github.com/RobinDev/Selenium-Chrome-HTTP-Private-Proxy)目录
# cd /data && git clone https://github.com/RobinDev/Selenium-Chrome-HTTP-Private-Proxy.git
CHROME_PROXY_HELPER_DIR = '/data/Selenium-Chrome-HTTP-Private-Proxy'
# 存储自定义Chrome代理扩展文件的目录
CUSTOM_CHROME_PROXY_EXTENSIONS_DIR = '/tmp/chrome-proxy-extensions'

def get_chrome_proxy_extension(username,password,ip,port):
    # 创建一个定制Chrome代理扩展(zip文件)
    if not os.path.exists(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR):
        os.mkdir(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR)
    extension_file_path = os.path.join(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR, '{}.zip'.format(port))

    zf = zipfile.ZipFile(extension_file_path, mode='w')
    zf.write(os.path.join(CHROME_PROXY_HELPER_DIR, 'manifest.json'), 'manifest.json')
    # 替换模板中的代理参数
    background_content = open(os.path.join(CHROME_PROXY_HELPER_DIR, 'background.js')).read()
    background_content = background_content.replace('%proxy_host', ip)
    background_content = background_content.replace('%proxy_port', port)
    background_content = background_content.replace('%username', username)
    background_content = background_content.replace('%password', password)
    zf.writestr('background.js', background_content)
    zf.close()
    print(extension_file_path)
    return extension_file_path

url = 'https://www.celestyles.com/'
# url = 'https://www.163.com/'

conn = sqlite3.connect('/data/proxy.db')
cur = conn.cursor()

hour = time.time()%(3600*24)/3600  # 0时区的小时数
# 美国西五～西十, 西七区晚上时间对应0时区是5～15
if 5 <= hour <= 15:
    count = 4
else:
    count = 8

if open('/data/index').read().strip() == '1':
    print('prepare doing')
else:
    print('stopping')
    import sys
    sys.exit(1)

time.sleep(60)
while open('/data/index').read().strip() == '1':
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('user-agent=' + random.choice(pc_user_agent_list))

        files = os.listdir('/data/port')
        port = ''
        if files:
            port = files[random.randint(0, len(files))]

        # cur.execute('select * from proxy limit 1')
        # proxy = cur.fetchone()
        # proxy = ('127.0.0.1', 8888, 'http')
        print(port)
        if port:
            os.remove('/data/port/' + port)
        else:
            print('port not found, exit...')
            import sys
            sys.exit(1)

        # port = random.randint(10001, 29999)
        # options.add_extension(get_chrome_proxy_extension('spef4f3f33', 'Celes@2801', 'us.smartproxy.com', str(port)))
        # port = random.randint(20001, 37960)
        options.add_extension(get_chrome_proxy_extension('spef4f3f33', 'Celes@2801', 'gate.dc.smartproxy.com', str(port)))

        options.add_argument("--no-sandbox")
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=options)
        driver.maximize_window()
        driver.implicitly_wait(2)
        driver.get(url)

        boxes = driver.find_elements(By.XPATH, '//a')

        # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        for i in range(random.randint(2, 4)):  # 随机点链接
            items = driver.find_elements(By.XPATH, '//a')
            try:
                item = items[random.randint(0, len(items))]
                href = item.get_attribute('href') or ''
                if 'channel' in href or 'detail' in href:
                    item.click()
            except:
                pass
            time.sleep(random.randint(10, 20))

        if random.randint(1, 200) == 102:  # 千分之五的点击
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            driver.find_element_by_class_name('ad-box').click()
            time.sleep(10)
        time.sleep(random.randint(10, 20))

    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()
    finally:
        try:
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                driver.close()
        except:
            pass




