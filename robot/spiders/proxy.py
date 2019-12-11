# -*- coding: utf-8 -*-
import scrapy
import sqlite3

class ProxySpider(scrapy.Spider):
    name = 'proxy'
    allowed_domains = ['proxynova.com', 'free-proxy-list.net']
    start_urls = [
        'https://www.proxynova.com/proxy-server-list/',
        'https://free-proxy-list.net/',
    ]
    conn = sqlite3.connect('/tmp/proxy.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE if not exists proxy( ip CHAR(20) PRIMARY KEY NOT NULL, port int not null, type CHAR(100) NOT NULL);')

    def parse(self, response):
        if response.url == 'https://free-proxy-list.net/':
            trs = response.xpath('//tr')
            for tr in trs:
                try:
                    ip = tr.xpath('.//td[1]/text()').extract_first().strip()
                    port = tr.xpath('.//td[2]/text()').extract_first().strip()
                    code = tr.xpath('.//td[3]/text()').extract_first().strip()
                    print(ip, port, code)
                    self.cur.execute('insert into proxy values(%r, %r, %r);' % (ip, port, code))
                    self.conn.commit()
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
                    print(ip, port, code)
                    self.cur.execute('insert into proxy values(%r, %r, %r);' % (ip, port, code))
                    self.conn.commit()
                except Exception as e:

                    print('---------------')
                    print(e)


