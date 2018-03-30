__author__ = 'tian'
__author__ = 'tian'
import scrapy
import urllib
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from guiyangScrapy.items import GuiyangscrapyItem
from urllib.request import urlopen
from urllib.parse import quote #用于解决网址的中文问题
import os
import json
import logging


# from selenium.common.exceptions import NoSuchElementException
#ip池和user-agent还没设置

class QuotesSpider(scrapy.Spider):
    name = 'guiyang'

    def start_requests(self):
        # nums = list(range(1,108))
        # prefix_url = 'http://www.gyopendata.gov.cn/datadirectory.htm?type=0&value1=0&pageNo='
        # urls = [prefix_url+str(num) for num in nums]
        nums = list(range(1,15))
        urls = ['http://www.gyopendata.gov.cn/city/datadirectory.htm?value=0&doId='+str(num) for num in nums]

        for url in urls:
            print('url = %s'%url)
            yield scrapy.Request(url=url, callback=self.urls_parse,meta={'url': url})

    def urls_parse(self,response):
        page_num = response.xpath('//*[@class="page"]/span/font[3]/text()').extract()[0] #总页数
        catagory_num = response.meta['url'].split('=')[2]
        print('catagory_num = %s' %catagory_num)
        url_prefix = 'http://www.gyopendata.gov.cn/city/datadirectory.htm?type=0&value1=0&doId='+catagory_num+'&doId='+catagory_num+'&pageNo='
        print('url_prefix = %s'%url_prefix)
        nums = list(range(1,int(page_num)))
        urls = [url_prefix+str(num) for num in nums]

        for url in urls:
            print('url2 = %s' %url)
            yield scrapy.Request(url=url,callback=self.parse)


    def parse(self, response):
        print('1')
        soup = BeautifulSoup(response.text, 'lxml')
        url_prefix = 'http://www.gyopendata.gov.cn/city/'
        # base_url = 'http://www.gyopendata.gov.cn/city/datadownload.htm?resId='
        # base_url2 = 'http://www.gyopendata.gov.cn/city/datadownload2.htm?resId='
        # mid_url = '&fileName='
        # mid_url_ = '&ResName='
        titles = soup.find_all('p', 'data_rig_tit')
        i = 0  # 关于这个也可能出现错误
        # print('........................................')
        # print(soup.find_all('p', 'data_rig_tit')[0].get_text())

        for link in soup.find_all('div', 'sjml-box1-bt'):
            print('2')
            downloadLinks = []
            # href每个具体下载页面的链接
            href = url_prefix + link.find('a').get('href')
            print('href = %s' %href)
            # 每个分页面
            yield scrapy.Request(url=href, callback=self.parseData)

    #
    #         driver = webdriver.Chrome("/Users/tian/Downloads/chromedriver")
    #         driver.get(href)
    #
    #
    #         #点击下载的实现
    #
    #         form_ = driver.find_element_by_xpath("//*[@class='collapse navbar-collapse']/input")
    #         isLogin = form_.get_attribute("value")
    #         if isLogin == '':
    #
    #             login_ = driver.find_element_by_xpath("//*[@class='collapse navbar-collapse']")
    #             loginbutton = login_.find_element_by_xpath(".//*[@class='nav navbar-nav navbar-right hidden-sm unlogined']/li/a/span")
    #             loginbutton.click()
    #             userName = driver.find_element_by_xpath("//*[@id='username']")
    #             userName.clear()
    #             userName.send_keys('xiaotian')
    #             password = driver.find_element_by_xpath("//*[@id='password']")
    #             password.clear()
    #             password.send_keys('xiaotian123')
    #             #yzm = driver.find_element_by_xpath("//*[@id='image']")
    #             #captcha =
    #             captcha = response.xpath("//*[@id='image']").extract()
    #             if len(captcha) > 0:
    #                 print('存在验证码')
    #                 localpath = r'/Users/tian/Downloads/captcha.png'
    #                 urllib.urlretrieve(captcha[0],file_name=localpath)
    #                 print('done!')
    #             else:
    #                 print('此时没有验证码')
    #
    #
    #
    #
    #
    #
    #             print(loginbutton.text)
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #             print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    #         else:
    #             print("ooooooooooooooooooooooooooooooooooooooooooooooooo")
    #
    #
    #
    #
    #
    #
    #
    #
    #         data_field = driver.find_element_by_xpath("//html/body/div[5]/div[2]/div[2]/div[2]/p[1]/span").text
    #         abstract = driver.find_element_by_xpath("//html/body/div[5]/div[2]/div[2]/div[2]/p[2]/span").text
    #         keyword = driver.find_element_by_xpath("//html/body/div[5]/div[2]/div[2]/div[2]/p[3]/span").text
    #         theme_classification = driver.find_element_by_xpath(
    #             "//html/body/div[5]/div[2]/div[2]/div[2]/p[4]/span[1]").text
    #         industry_classfication = driver.find_element_by_xpath(
    #             "//html/body/div[5]/div[2]/div[2]/div[2]/p[4]/span[2]").text
    #         service_classfication = driver.find_element_by_xpath(
    #             "//html/body/div[5]/div[2]/div[2]/div[2]/p[4]/span[3]").text
    #         open_attribute = driver.find_element_by_xpath("//html/body/div[5]/div[2]/div[2]/div[2]/p[5]/span").text
    #         update_frequency = driver.find_element_by_xpath("//html/body/div[5]/div[2]/div[2]/div[2]/p[6]/span").text
    #         release_date = driver.find_element_by_xpath("//html/body/div[5]/div[2]/div[2]/div[2]/p[8]/span").text
    #         update_date = driver.find_element_by_xpath("//html/body/div[5]/div[2]/div[2]/div[2]/p[9]/span").text
    #         data_supplier_agent = driver.find_element_by_xpath(
    #             "//html/body/div[5]/div[2]/div[2]/div[2]/p[10]/span").text
    #         data_supplier_address = driver.find_element_by_xpath(
    #             "//html/body/div[5]/div[2]/div[2]/div[2]/p[11]/span").text
    #         data_maintenance_agent = driver.find_element_by_xpath(
    #             "//html/body/div[5]/div[2]/div[2]/div[2]/p[12]/span").text
    #         language = driver.find_element_by_xpath("//html/body/div[5]/div[2]/div[2]/div[2]/p[13]/span").text
    #         unknown = driver.find_element_by_xpath("//html/body/div[5]/div[2]/div[2]/div[2]/p[14]").text
    #
    #         title = titles[i].get_text().strip()
    #         i += 1
    #
    #         if '文件大小' in unknown:
    #             file_size = driver.find_element_by_xpath("//html/body/div[5]/div[2]/div[2]/div[2]/p[14]/span").text
    #             file_amount = driver.find_element_by_xpath("//html/body/div[5]/div[2]/div[2]/div[2]/p[15]/span").text
    #             security_degree = driver.find_element_by_xpath(
    #                 "//html/body/div[5]/div[2]/div[2]/div[2]/p[16]/span").text
    #             resId = driver.find_element_by_xpath("//html/body/div[5]/div[2]/div[2]/div[2]/p[17]/span").text
    #             record_size = ''
    #         else:
    #             record_size = driver.find_element_by_xpath("//html/body/div[5]/div[2]/div[2]/div[2]/p[14]/span").text
    #             security_degree = driver.find_element_by_xpath(
    #                 "//html/body/div[5]/div[2]/div[2]/div[2]/p[15]/span").text
    #             resId = driver.find_element_by_xpath("//html/body/div[5]/div[2]/div[2]/div[2]/p[16]/span").text
    #             file_size = ''
    #             file_amount = ''
    #
    #         allFileNames = driver.find_elements_by_xpath("//ul[@id='fileList']/input")
    #         index = 1
    #         for file_name in allFileNames:
    #             item = GeneralItem()
    #             item['title'] = title
    #             item['data_field'] = data_field
    #             item['abstract'] = abstract
    #             item['keyword'] = keyword
    #             item['theme_classification'] = theme_classification
    #             item['industry_classfication'] = industry_classfication
    #             item['service_classfication'] = service_classfication
    #             item['open_attribute'] = open_attribute
    #             item['update_frequency'] = update_frequency
    #             item['release_date'] = release_date
    #             item['update_date'] = update_date
    #             item['data_supplier_agent'] = data_supplier_agent
    #             item['data_supplier_address'] = data_supplier_address
    #             item['data_maintenance_agent'] = data_maintenance_agent
    #             item['language'] = language
    #             item['file_size'] = file_size
    #             item['file_amount'] = file_amount
    #             item['record_size'] = record_size
    #             item['security_degree'] = security_degree
    #             item['resId'] = resId
    #             print('resId = %s' %resId)
    #
    #             fileN = file_name.get_attribute('value')
    #             if 'undefined' in fileN:   #貌似这里有问题!
    #                 path_pre = "//ul[@id='fileList']/li["
    #                 path_post = "]/a"
    #                 path = path_pre + str(index) + path_post
    #                 print('i = %d'%i)
    #                 print('fileN = %s' %fileN)
    #                 #fileN = file_name.find_element_by_xpath(".//li/a").text        #这里可能出错
    #                 #xpath_url = './/li/a'
    #                 #fileN = file_name.find_element_by_xpath('./li/a').text
    #                 #fileN = driver.find_element_by_xpath("//ul[@id='fileList']/input[index]/li/a").text
    #                 #fileN = driver.find_element_by_xpath("//ul[@id='fileList']/li[0]/a").text
    #                 fileN = file_name.find_element_by_xpath(path).text
    #
    #                 print('ooo%s'%fileN)
    #             item['file_name'] = fileN
    #             index+=1
    #             yield item
    #
    #             downloadLink = base_url + resId + mid_url + fileN
    #             downloadLink_ = base_url + resId + mid_url_ + fileN
    #             print('下载地址为:%s' % downloadLink)
    #
    #             yield Request(downloadLink, callback=self.parse2, meta={'url': downloadLink, 'url_': downloadLink_})
    #
    #             # self.downloading(downloadLink)
    #
    # def parse2(self, response):
    #     if response.status == 500:
    #         pass
    #         print('111111111111111111111111111111111111111111111111111111')
    #     else:
    #         print(response.meta['url'])
    #         self.downloading(response.meta['url'], response.meta['url_'])
    #
    # def downloading(self, url, url_):
    #
    #     self.downloadingFile(url)
    #     print('pissoff')
    #     if not os.path.exists('/Users/tian/Downloads/scrapy_file_Download_/' + url.split('=')[2]):
    #         print('pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp')
    #         print('pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp')
    #         print('pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp')
    #         self.downloadingFile(url_)

    def downloadingFile(self, url, fileName):
        r = requests.get(url)
        r.encoding = 'utf-8'
        html = r.text
        with open('/Users/tian/Downloads/scrapy_file_Download_/' + fileName, 'w', encoding='utf-8') as code:
            code.write(html)

    def getDownloadLinks(self, url):
        downloadLinks = []
        base_url = 'http://www.gyopendata.gov.cn/datadownload2.htm?resId='
        mid_url = '&fileName='
        driver = webdriver.Chrome("/Users/tian/Downloads/chromedriver")
        driver.get(url)
        resId = driver.find_element_by_xpath("//*[contains(text(), '信息资源标识符')]").text.split('：')[1]
        print('resId=%s' % resId)
        allFileNames = driver.find_elements_by_xpath("//ul[@id='fileList']/input")
        for fileName in allFileNames:
            print('fileName=%s' % fileName)
            downloadLink = base_url + resId + mid_url + fileName.get_attribute('value')
            print(downloadLink)
            downloadLinks.append(downloadLink)
            downloadLink = ''
        return downloadLinks

    def parseData(self, response):
        print('3')
        title = response.xpath('//*[@id="resName"]/@value').extract()[0]
        resId = response.xpath('//*[@id="resId"]/@value').extract()[0]
        data_field = response.xpath("//*[contains(text(), '数据领域')]/span/text()").extract()[0].strip()

        abstract = response.xpath("//*[contains(text(), '摘')]/span/text()").extract()[0].strip()
        #print(type(abstract))
        print('...................')
        key_word = response.xpath("//*[contains(text(), '关 键 字')]/span/text()").extract()[0].strip()
        theme_classification = response.xpath("//*[contains(text(), '主题分类')]/span[1]/text()").extract()[0].strip()
        industry_classfication = response.xpath("//*[contains(text(), '主题分类')]/span[2]/text()").extract()[0].strip()
        service_classfication = response.xpath("//*[contains(text(), '主题分类')]/span[3]/text()").extract()[0].strip()
        open_attribute = response.xpath("//*[contains(text(), '开放属性')]/span[1]/text()").extract()[0].strip()
        update_frequency = response.xpath("//*[contains(text(), '开放属性')]/span[2]/text()").extract()[0].strip()
        release_date = response.xpath("//*[contains(text(), '发布日期')]/span[1]/text()").extract()[0].strip()
        update_date = response.xpath("//*[contains(text(), '发布日期')]/span[2]/text()").extract()[0].strip()
        data_supplier_agent = response.xpath("//*[contains(text(), '发布日期')]/span[3]/text()").extract()[0].strip()
        data_supplier_address = response.xpath("//*[contains(text(), '数据提供方地址')]/span/text()").extract()[0].strip()
        data_maintenance_agent = response.xpath("//*[contains(text(), '数据维护方单位')]/span[1]/text()").extract()[0].strip()
        language = response.xpath("//*[contains(text(), '数据维护方单位')]/span[2]/text()").extract()[0].strip()
        security_degree = response.xpath("//*[contains(text(), '安全等级')]/span[1]/text()").extract()[0].strip()
        file_size = response.xpath("//*[contains(text(), '安全等级')]/span[2]/text()").extract()
        if file_size:
            file_size = file_size[0].strip()
        file_amount = response.xpath("//*[contains(text(), '安全等级')]/span[3]/text()").extract()
        if file_amount:
            file_amount = file_amount[0].strip()
        record_size = response.xpath("//*[contains(text(), '数据维护方单位')]/span[3]/text()").extract()
        if record_size:
            record_size = record_size[0].strip()

        # 取filelist
        fileList_base = 'http://www.gyopendata.gov.cn/city/filelist.htm?'
        fileList_url_1 = fileList_base + 'resId=' + resId + '&resName=' + quote(title) + '&text1=csv' + '&doId=1'
        fileList_url_2 = fileList_base + 'resId=' + resId + '&resName=' + quote(title) + '&text1=csv' + '&doId=2'
        fileList_url = [fileList_url_1, fileList_url_2]

        response_1 = urlopen(fileList_url_1, timeout=15)
        response_2 = urlopen(fileList_url_2, timeout=15)
        data_1 = response_1.read().decode('utf-8')
        data_2 = response_2.read().decode('utf-8')
        data1 = json.loads(data_1)
        data2 = json.loads(data_2)
        # item = GeneralItem()    #可能因为放在循环里面而存在问题

        if data1:
            for d1 in data1:
                fileName_1 = d1.get('fileName', '')
                resName_1 = d1.get('resName', '')
                tableName_1 = d1.get('tableName', '')
                download_url_1 = 'http://www.gyopendata.gov.cn/city/datadownload.htm?resId=' + resId + '&resName=' + resName_1 + '&text1=' + tableName_1 + '&text2=csv'
                try:
                    self.downloadingFile(download_url_1, fileName_1)  #可能存在因文件不存在而导致下载有问题
                    item = GuiyangscrapyItem()
                    item['title'] = title
                    item['data_field'] = data_field
                    item['abstract'] = abstract
                    item['keyword'] = key_word
                    item['theme_classification'] = theme_classification
                    item['industry_classfication'] = industry_classfication
                    item['service_classfication'] = service_classfication
                    item['open_attribute'] = open_attribute
                    item['update_frequency'] = update_frequency
                    item['release_date'] = release_date
                    item['update_date'] = update_date
                    item['data_supplier_agent'] = data_supplier_agent
                    item['data_supplier_address'] = data_supplier_address
                    item['data_maintenance_agent'] = data_maintenance_agent
                    item['language'] = language
                    item['file_size'] = file_size
                    item['file_amount'] = file_amount
                    item['record_size'] = record_size
                    item['security_degree'] = security_degree
                    item['resId'] = resId
                    item['file_name'] = fileName_1
                    yield item
                except:
                    logging.info('there might be some downloading error...')
                    continue




        if data2:
            for d2 in data2:
                uploadName_2 = d2.get('uploadName', '')
                fileName_2 = d2.get('fileName', '')
                createTime_2 = d2.get('createTime', '')
                uploadDir_2 = d2.get('uploadDir', '')
                download_url_2 = 'http://www.gyopendata.gov.cn/city/datadownload2.htm?resId=' + resId + '&fileName=' + fileName_2 + '&uploadDir=' + uploadDir_2
                try:
                    self.downloadingFile(download_url_2, uploadName_2)
                    item = GuiyangscrapyItem()
                    item['title'] = title
                    item['data_field'] = data_field
                    item['abstract'] = abstract
                    item['keyword'] = key_word
                    item['theme_classification'] = theme_classification
                    item['industry_classfication'] = industry_classfication
                    item['service_classfication'] = service_classfication
                    item['open_attribute'] = open_attribute
                    item['update_frequency'] = update_frequency
                    item['release_date'] = release_date
                    item['update_date'] = update_date
                    item['data_supplier_agent'] = data_supplier_agent
                    item['data_supplier_address'] = data_supplier_address
                    item['data_maintenance_agent'] = data_maintenance_agent
                    item['language'] = language
                    item['file_size'] = file_size
                    item['file_amount'] = file_amount
                    item['record_size'] = record_size
                    item['security_degree'] = security_degree
                    item['resId'] = resId
                    item['file_name'] = uploadName_2
                    yield item
                except:
                    logging.info('there might be some downloading error...')
                    continue


                print('downloading')
        # item = GeneralItem()
        # item['title'] = title
        # item['data_field'] = data_field
        # item['abstract'] = abstract
        # item['keyword'] = key_word
        # item['theme_classification'] = theme_classification
        # item['industry_classfication'] = industry_classfication
        # item['service_classfication'] = service_classfication
        # item['open_attribute'] = open_attribute
        # item['update_frequency'] = update_frequency
        # item['release_date'] = release_date
        # item['update_date'] = update_date
        # item['data_supplier_agent'] = data_supplier_agent
        # item['data_supplier_address'] = data_supplier_address
        # item['data_maintenance_agent'] = data_maintenance_agent
        # item['language'] = language
        # item['file_size'] = file_size
        # item['file_amount'] = file_amount
        # item['record_size'] = record_size
        # item['security_degree'] = security_degree
        # item['resId'] = resId
        # print('resId = %s' % resId)


