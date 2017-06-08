# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests


class ScrapytestPipeline(object):
    def process_item(self, item, spider):
        return item

class axespipeline(object):
    DOWNLOAD_PIC = False

    def open_spider(self,spider):
        self.f = open('info.txt','w')
    def close_spider(self,spider):
        self.f.close()
        
    def process_item(self,item,spider):
        # 图片下载 按照货号建立文件夹 分商品保存图片
        picroot = 'D:/study/axes/'
        picpath = picroot + item['货号'] + '/'

        if not os.path.exists(picroot):
            os.mkdir(picroot)
        if not os.path.exists(picpath):
            os.mkdir(picpath)

        try:
            #信息保存
            line=str(dict(item))+'\n'
            self.f.write(line)

            #图片下载
            if DOWNLOAD_PIC  == True:
                urls = item['细节图'] + item['预览图']
                for url in urls:
                    try:
                        #判断是否重复下载
                        picname = url.split('/')[-1]
                        if not os.path.exists(picpath+picname):
                            with open(picpath+picname,'wb') as p:
                                p.write(requests.get('http://'+url).content)
                                p.close()
                                print('图片下载成功')
                        else:
                            print('图片已下载')
                    except:
                        print('下载失败 url='+url)
                        break
        except:
            self.f.write('分析失败'+item+'\n')

        return item

