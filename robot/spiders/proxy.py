# -*- coding: utf-8 -*-
import scrapy
import sqlite3
import requests

class ProxySpider(scrapy.Spider):
    name = 'proxy'
    allowed_domains = ['proxynova.com', 'free-proxy-list.net']
    start_urls = [
        'https://www.proxynova.com/proxy-server-list/',
        'https://free-proxy-list.net/',
    ]
    conn = sqlite3.connect('/tmp/proxy.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE if not exists proxy( ip CHAR(20) PRIMARY KEY NOT NULL, port int not null, '
                'type CHAR(100) NOT NULL, code CHAR(100) NOT NULL);')

    def insert(self, ip, port, code):
        ip = ''.join([i for i in ip if i in '0123456789.'])
        if len(ip.split('.')) == 4:
            for schema in ['http', 'https', 'socks4', 'socks5']:
                resp = requests.get('http://ipinfo.io/ip', proxies={'http': schema+"://" + ip + ":" + port})
                if resp == ip:
                    self.cur.execute('insert into proxy values(%r, %r, %r, %r);' % (ip, port, schema, code))
                    self.conn.commit()

    def parse(self, response):
        if response.url == 'https://free-proxy-list.net/':
            trs = response.xpath('//tr')
            for tr in trs:
                try:
                    ip = tr.xpath('.//td[1]/text()').extract_first().strip()
                    port = tr.xpath('.//td[2]/text()').extract_first().strip()
                    code = tr.xpath('.//td[3]/text()').extract_first().strip()
                    self.insert(ip, port, code)
                except Exception as e:
                    print('------11111111111---------')
                    print(e)

        elif response.url == 'https://www.proxynova.com/proxy-server-list/':
            trs = response.xpath('//tr')
            for tr in trs:
                try:
                    ip = tr.xpath('.//td[1]/abbr/@title').extract_first().strip()
                    port = tr.xpath('.//td[2]').xpath('string(.)').extract_first().strip()
                    code = tr.xpath('.//td[6]').xpath('string(.)').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')
                    self.insert(ip, port, code)
                except Exception as e:
                    print('---------------')
                    print(e)


