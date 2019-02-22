import pymysql
from selenium import webdriver


class MysqlPipeline(object):
    def __init__(self):
        # 数据库连接对象
        self.db = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='zhanghaoyu18',
            database='spider',
            charset="utf8"
        )
        # 游标对象
        self.cursor = self.db.cursor()

    def process_item(self, item):
        ins = 'insert into autohome1 values(%s,%s,%s,%s,%s,%s,%s,%s)'
        L = [
            item['brand_name'],
            item['series'],
            item['car_name'],
            item['car_url'],
            item['dealer_price'],
            item['factory_price'],
            item['used_price'],
            item['premium_rate'],
        ]
        self.cursor.execute(ins, L)
        # 一定要提交到数据库执行
        self.db.commit()
        return 0

    # process_item处理完成后会执行此方法
    def close_spider(self):
        self.cursor.close()
        self.db.close()
        print("MySQL数据库断开连接")


def func(urls,db):
    item = {}
    i = 0
    count = len(urls)
    for url in urls:
        i+=1
        print(i,'/',count,':',int(i / count * 100), '%')
        driver.get(url)
        item['car_url'] = url
        try:
            item['car_name'] = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div[1]/div[1]/div[1]/h2").get_attribute("innerText")
        except:
            item['car_name'] = '暂无'
        try:
            item['brand_name']=driver.find_element_by_xpath("//div[@class='athm-sub-nav__car__name']/a[1]").get_attribute("innerText")
        except:
            item['brand_name']='暂无'
        try:
            item['series'] = driver.find_element_by_xpath("//div[@class='athm-sub-nav__car__name']/a/h1").get_attribute("innerText")
        except:
            item['series']='暂无'

        try:
            item['dealer_price'] = driver.find_element_by_xpath("//a[@class='emphasis']").get_attribute("innerText")
        except:
            item['dealer_price'] = '暂无'
        try:
            item['factory_price'] =driver.find_element_by_xpath("//span[@class='factoryprice']").get_attribute("innerText")
        except:
            item['factory_price'] = '暂无'
        try:
            item['used_price'] =driver.find_element_by_xpath("//span[@class='usedprice']/a").get_attribute("innerText")
        except:
            item['used_price'] = '暂无'
        try:
            item['premium_rate'] = driver.find_element_by_xpath("//span[@class='premium']/a").get_attribute(
                "innerText")
        except:
            item['premium_rate'] = '暂无'
        print(item)
        db.process_item(item)


if __name__=='__main__':
    opt = webdriver.ChromeOptions()
    opt.headless=True
    driver = webdriver.Chrome(options=opt)

    # driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
    urls = []
    for page in range(1,82):
        print(page,'/',81,":",int(page/81*100),'%')
        brand_url='https://car.autohome.com.cn/price/list-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-' + str(page) + '.html'
        driver.get(brand_url)
        cars = driver.find_elements_by_xpath("//div[@id='brandtab-1']/div[contains(@class,'intervalcont')]/div/ul/li/div[1]/div/p/a")
        for car in cars:
            url = car.get_attribute('href')
            urls.append(url)
    db = MysqlPipeline()
    func(urls,db)
    db.close_spider()


