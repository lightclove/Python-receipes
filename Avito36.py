# coding: utf-8
import requests
from lxml import html
import urllib.parse
import urllib.request
import smtplib

class Avito(object):
    MAX_SUMM = 70000

    RESULT = []

    def parse_avito_run(self):
        #url = 'https://www.avito.ru/bryansk/zemelnye_uchastki/prodam?bt=1&district=203&f=531_5491-5492'
        url = 'https://www.avito.ru/sankt-peterburg/telefony/samsung?q=samsung%20galaxy%20note%208&sgtd=21'
        r = requests.get(url)
        res = html.fromstring(r.content)
        result = res.xpath(u'//*[contains(text(), "Последняя")]/@href')
        num = self._get_page_num(result[0])
        result = self.get_page_data(num)
        return result

    def get_page_data(self, num):
        #url = 'https://www.avito.ru/bryansk/zemelnye_uchastki/prodam?p={}bt=1&district=203&f=531_5491-5492'
        url = 'https://www.avito.ru/sankt-peterburg/telefony/samsung?q=samsung%20galaxy%20note%208&sgtd=21'
        for i in range(1, num):
            r = requests.get(url.format(i))
            self.get_all(r.content)
        return self.RESULT

    def _get_page_num(self, href):
        result = urllib.parse.urlparse(href)
        result = urllib.parse.parse_qs(result.query)
        return int(result['p'][0])

    def get_all(self, data):
        data = self._get_desc(data)
        for key, i in enumerate(data):
            href = i.xpath('//h3[@class="title item-description-title"]/a/@href')[key]
            title = i.xpath('//h3[@class="title item-description-title"]/a/@title')[key]
            address = i.xpath('//p[@class="address fader"]/text()')[key]
            summ = i.xpath('//div[@class="about"]/text()[1]')[key]
            summ = summ.strip()
            summ = summ.replace(" руб.", "")
            summ = summ.replace(" ", "")
            if summ:
                summ = int(summ)
                if summ > self.MAX_SUMM:
                    continue

            else:
                summ = u'Без цены '
            self.RESULT.append({'title': title,
                                'href': 'https://www.avito.ru' + href,
                                'address': address,
                                'sum': summ
                                })

    def _get_desc(self, data):
        return self.get_from_xpath(data, '//div[@class="description"]')

    def get_from_xpath(self, data, xpath):
        res = html.fromstring(data)
        return res.xpath(xpath)

if __name__ == '__main__':
    avito = Avito()
    avito.parse_avito_run()
    msg = u'Subject: Samsung Galaxy Note 8'+"\n"
    for res in avito.RESULT:
        for k, i in res.items():
            msg+=str(res[k]).strip()+"\n"
        msg+='-------------------------------'+'\n'
    server = smtplib.SMTP('smtp.yandex.com', 587)
    server.starttls()
    server.login("sendfromemail1@ya.ru", "MyPassword")
    server.sendmail('sendfromemail1@ya.ru', 'sendtoemail2@gmail.com', msg.encode('utf-8'))
    server.quit()