from selenium import webdriver
import random
import zipfile
from selenium.webdriver.common.by import By
import requests
import time


while True:
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=http://127.0.0.1:8888')
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    driver.implicitly_wait(2)
    driver.get('https://hidemy.name/en/proxy-list/')
    time.sleep(10)
    trs = driver.find_elements_by_tag_name('tr')

    for tr in trs:
        try:
            tds = tr.find_elements_by_tag_name('td')
            ip = tds[0].text.strip()
            ip = ''.join([i for i in ip if i in '0123456789.'])

            if len(ip.split('.')) == 4:
                port = tds[1].text.strip()
                schema = tds[4].text.split(',')[0].strip().lower()
                code = tds[2].text.strip()
                print(ip, port, schema, code)
                requests.get('http://ipinfo.io/ip', proxies={'http': schema + "://" + ip + ":" + port}, timeout=10)
                item = ip + "-" + port + "-" + schema
                open('/data/proxy/' + item, 'w').write(code)
        except:
            import traceback
            traceback.print_exc()

    try:
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            driver.close()
    except:
        pass


    try:
        https = requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all').text.split()
        for i in https:
            try:
                if requests.get('http://ipinfo.io/ip', proxies={'http': 'http://' + i}, timeout=10).status_code == 200:
                    print(i)
                    item = i.replace(':', '-') + '-' + 'http'
                    open('/data/proxy/' + item, 'w').write('')
            except:
                pass

        https = requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=10000&country=all').text.split()
        for i in https:
            try:
                if requests.get('http://ipinfo.io/ip', proxies={'http': 'socks4://' + i}, timeout=10).status_code == 200:
                    print(i)
                    item = i.replace(':', '-') + '-' + 'socks4'
                    open('/data/proxy/' + item, 'w').write('')
            except:
                pass

        https = requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&country=all').text.split()
        for i in https:
            try:
                if requests.get('http://ipinfo.io/ip', proxies={'http': 'socks5://' + i}, timeout=10).status_code == 200:
                    print(i)
                    item = i.replace(':', '-') + '-' + 'socks5'
                    open('/data/proxy/' + item, 'w').write('')
            except:
                pass
    except:
        pass

