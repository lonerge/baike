from lxml import etree
import requests
import json
import re



class Baike(object):
    def __init__(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'
        }
        res = requests.get(
            'https://baike.baidu.com/item/%E6%B3%B0%E5%8B%92%C2%B7%E6%96%AF%E5%A8%81%E5%A4%AB%E7%89%B9/8472307', headers=headers
        )
        self.html = etree.HTML(res.text)
        self.info = dict()

    def parse(self):
        # 基本信息
        content = ''.join(self.html.xpath('//div[@class="lemma-summary"]//*/text()')).strip()
        # 去特殊符号
        special = re.findall(r'\[\d+]', content)
        # print(special)
        for spec in special:
            content = content.replace(spec, '').replace('\n\xa0\n', '')
        self.info['content'] = content

        # 人物关系
        relation = []
        relations = self.html.xpath('//*[@id="slider_relations"]/ul/li')
        for relat in relations:
            temp = dict()
            temp['relation'] = relat.xpath('./a/div/text()')[0]
            temp['url'] = 'https://baike.baidu.com' + relat.xpath('./a/@href')[0]
            temp['name'] = relat.xpath('./a/div/em/text()')[0]
            relation.append(temp)
        self.info['relation'] = relation
        # print(self.info)

        # 信息表
        infobox = dict()
        dt_list = self.html.xpath('/html/body/div[3]/div[4]/div/div[1]/div/div[5]/dl[1]//dt/text()')
        # print(dt_list)
        # print(dt_list, len(dt_list),type(dt_list))
        dd_list = self.html.xpath('/html/body/div[3]/div[4]/div/div[1]/div/div[5]/dl[1]//dd//text()')
        dd_list1 = [x.strip() for x in dd_list if x.strip() != '']
        dd_list1.pop(-1)
        dd_list1.pop(-4)
        # dd_list1 = list(filter(None, dd_list))
        # print(dd_list1, len(dd_list1))
        for i in range(len(dt_list)):
            infobox[dt_list[i].replace('\xa0', '').replace('\n', '')] = dd_list1[i]
        self.info['infobox'] = infobox
        # print(self.info)

        # 信息表+url
        infobox_url = dict()
        a = self.html.xpath('/html/body/div[3]/div[4]/div/div[1]/div/div[5]/dl[2]/dd//a/text()')
        a_href = self.html.xpath('/html/body/div[3]/div[4]/div/div[1]/div/div[5]/dl[2]/dd//a/@href')
        a.remove('展开')
        a.remove('收起')
        a = [x.strip() for x in a if x.strip() != '']
        # print(a, len(a))
        for i in range(len(a)-8):
            infobox_url[a[i]] = 'https://baike.baidu.com' + a_href[i]
        self.info['infobox_url'] = infobox_url
        # print(self.info)
        return self.info

    def save(self, info):
        # 序列化info字典
        result = json.dumps(info, ensure_ascii=False, indent=1)
        with open('baike.json', 'w') as f:
            f.write(result)

    def run(self):
        info = self.parse()
        self.save(info)


if __name__ == '__main__':
    baike = Baike()
    baike.run()







