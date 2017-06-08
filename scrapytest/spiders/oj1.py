# -*- coding: utf-8 -*-
import scrapy
import re
from axes_type import axes_type
from datetime import datetime
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor




class Oj1Spider(scrapy.Spider):
    items_num = 0
    name = "axes"
    #allowed_domains = ["axesfemme.com"]
    #根据品牌创建start_urls
    #brand = ['axesfemme','poetique','kids','nostalgie','kawaii']
    start_urls = ['http://shop.axesfemme.com/Form/Product/ProductList.aspx?shop=0&cat=&bid=poetique&pid=&vid=&swrd=&img=2&sort=07&cicon=&min=&max=&udns=0&dosp=&pno=3']

    linklist = LinkExtractor(allow=r'pno=\d+')
    linkpage = LinkExtractor(allow=r'cat=&swrd=')
    rules = [Rule(linklist),
             Rule(linkpage, callback='parse_item', follow=True)]


    #商品页分析
    def parse_item(self,response):

        infodict={}
        axesmeta = response.css('meta[property]::attr(content)').extract()
        axesspec = response.css('div[class=d2]::text').extract()
        
        #商品名、商品主预览图、商品描述
        #商品名 = re.findall('｜\S*',response.css('title').extract()[0])
        infodict['商品名']= axesmeta[0]
        infodict['货号']=axesspec[0]
        infodict['价格'] = response.css('div[id=status] dd::text').extract()[0][2:]
        infodict['商品链接']=response.url
        infodict['预览图']= axesmeta[3].split('//')[-1]
        infodict['颜色'] = axesspec[1].split('、')
        infodict['材质'] = axesspec[3:]
        infodict['商品描述']=axesmeta[7].split('&l')[0]
        infodict['品牌'] = axesmeta[2].split('=')[-1]

        typenum = re.findall('var categoryId2 = "(\d*?)"',response.text)
        typ = axes_type.axes_type.type('',typenum)
        infodict['类型'] = typ

        #尺寸 获取所有尺寸的大小 0type 1S 2M 3L 4XL 5XXL
        sizes = response.css('tr[class*=row]')
        size = [i.css('td::text').extract() for i in sizes]
        infodict['尺寸'] = [i for i in size if len(i)>1]


        #商品细节图
        detailpic=response.css('div[id=mainPhoto] img::attr(src)').extract()
        for i in range(len(detailpic)):
            detailpic[i]=detailpic[i].split('//')[-1]
        infodict['细节图'] = detailpic

        self.items_num += 1

        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"  已下载:", self.items_num,'个')
        yield infodict