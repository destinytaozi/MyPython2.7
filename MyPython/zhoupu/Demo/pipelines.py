# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import smtplib
import time
from email.mime.text import MIMEText
import mysql.connector as mariadb
from mysql.connector import errorcode
from scrapy.utils.log import logger
from scrapy.utils.project import get_project_settings

mail_item_dict = {}


class ProductDetailPipeline(object):
    def __init__(self, mariadb_url, mariadb_port, mariadb_dbname, mariadb_user, mariadb_passwd):
        self.mariadb_url = mariadb_url
        self.mariadb_port = mariadb_port
        self.mariadb_dbname = mariadb_dbname
        self.mariadb_user = mariadb_user
        self.mariadb_passwd = mariadb_passwd
        self.mariadb_connection = mariadb.connect(host=self.mariadb_url, port=self.mariadb_port,
                                                  user=self.mariadb_user, password=self.mariadb_passwd,
                                                  database=self.mariadb_dbname, charset='utf8')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mariadb_url=crawler.settings.get('MARIADB_HOST'),
            mariadb_port=crawler.settings.get('MARIADB_PORT'),
            mariadb_dbname=crawler.settings.get('MARIADB_DBNAME'),
            mariadb_user=crawler.settings.get('MARIADB_USER'),
            mariadb_passwd=crawler.settings.get('MARIADB_PASSWD'),
        )

    def open_spider(self, spider):
        try:
            self.mariadb_connection = mariadb.connect(host=self.mariadb_url, port=self.mariadb_port,
                                                      user=self.mariadb_user, password=self.mariadb_passwd,
                                                      database=self.mariadb_dbname, charset='utf8')
        except mariadb.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger.critical(u'用户名或密码错误.')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logger.critical(u'数据库不存在.')
            else:
                logger.error(err)

    def process_item(self, item, spider):
        logger.info(item)
        product_code = item['productCode']
        seller_flag = item['sellerFlag']
        # current_price = item['price']
        total_price = item['totalPrice']
        conn = self.mariadb_connection
        times = 1
        while not conn.is_connected():
            logger.error(u'数据库连接已经断开,正在尝试第[%s]次连接...' % times)
            self.open_spider(spider)
            conn = self.mariadb_connection
            times += 1
            if times == 4:
                logger.error(u'数据库连接存在问题，停止爬虫...')
                # spider.crawler.signals.disconnect_all(signal=signals.spider_closed)
                return
        if times > 1:
            logger.info(u'数据库连接成功...')
        cursor = conn.cursor()
        # 如果商品编码不存在 或 商品编码存在及销售标识不存在
        if not self._query_exists_product(product_code, seller_flag):
            self._insert_t_product(cursor, item)
            self._insert_t_product_price(cursor, item)
        # 商品编码及销售标识存在
        else:
            price = self._query_price(product_code, seller_flag)
            history_min_price = price[0]
            history_avg_price = price[1]
            # 如果当前抓取价格(减去积分)小于历史最低价或历史平均价,更新商品信息
            if total_price != u'None':
                if float(total_price) < history_min_price:
                    item['minPrice'] = total_price
                    item['avgPrice'] = unicode(history_avg_price)
                    mail_item_dict[product_code] = item
                    self._update_t_product(cursor, item)
                else:
                    item['avgPrice'] = unicode(history_avg_price)
                    if float(total_price) < history_avg_price:
                        item['minPrice'] = unicode(history_min_price)
                        mail_item_dict[product_code] = item
                    self._update_t_product(cursor, item, flag=2)
                self._insert_t_product_price(cursor, item)
        conn.commit()
        cursor.close()

    def close_spider(self, spider):
        self.mariadb_connection.close()
        if mail_item_dict:
            # 如果mail_item_dict不为空,则发送邮件
            logger.info(u'哇涩，又有最新低价,发送邮件中...')
            self._send_email(mail_item_dict.values())

    def _query_price(self, product_code, seller_flag):
        """
        查询指定商品编码及卖家标识的商品历史最低售价及历史平均价
        :param product_code: 商品编码
        :param seller_flag: 卖家标识
        :return: (最低售价, 平均价)
        """
        if product_code is not None and seller_flag is not None:
            query_min_price = "SELECT minPrice FROM t_product WHERE productCode = %s AND sellerFlag = %s"
            query_avg_price = "SELECT AVG(price) FROM t_product_price WHERE productCode = %s AND sellerFlag = %s"
            cursor = self.mariadb_connection.cursor(buffered=True)
            cursor.execute(query_min_price, (product_code, seller_flag))
            min_price = cursor.fetchall()[0][0]
            cursor.execute(query_avg_price, (product_code, seller_flag))
            avg_price = cursor.fetchall()[0][0]
            logger.info(u'商品历史最低价为: %s, 历史平均价为: %s' % (min_price, avg_price))
            return min_price, avg_price
        else:
            raise ValueError(u'商品编码或卖家标识为空.')

    def _query_exists_product(self, product_code, seller_flag):
        """
        判断指定商品编码及卖家标识在t_product表中是否存在
        :param product_code: 商品编码
        :param seller_flag: 卖家标识
        :return: 如果存在返回True，否则False
        """
        if product_code is not None and seller_flag is not None:
            query_product = "SELECT COUNT(1) FROM t_product WHERE productCode = %s AND sellerFlag = %s"
            cursor = self.mariadb_connection.cursor(buffered=True)
            cursor.execute(query_product, (product_code, seller_flag))
            count = cursor.fetchall()[0][0]
            return True if count > 0 else False

    def _insert_t_product(self, cursor, item):
        """
        插入t_product表数据
        :param item: item对象
        :return: 
        """
        if item['japaneseName'] != u'None':
            try:
                insert_t_product = "INSERT INTO t_product(productCode, productUrl, state, chineseName, japaneseName, " \
                                   "imgUrl, sellerFlag) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                # cursor = self.mariadb_connection.cursor()
                logger.info(u'插入新的商品[%s]...' % item['chineseName'])
                cursor.execute(insert_t_product, (
                    item['productCode'], item['productUrl'], item['state'], item['chineseName'], item['japaneseName'],
                    item['imgUrl'], item['sellerFlag']))
                # self.mariadb_connection.commit()
                logger.info(u'插入t_product成功...')
            except mariadb.Error as err:
                logger.error(u'插入t_product表失败. 原因为: %s' % err)
                self.mariadb_connection.rollback()

    def _insert_t_product_price(self, cursor, item):
        """
        插入t_product_price表数据
        :param item: item对象 
        :return: 
        """
        # 为None时说明该商品暂时没货，不需要插入price表
        if item['price'] != u'None':
            try:
                insert_t_product_price = "INSERT INTO t_product_price(productCode, price, sellerFlag, pointFlag, points, " \
                                         "promotionFlag, totalPrice, extractTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                # cursor = self.mariadb_connection.cursor()
                logger.info(u'插入新的爬虫商品[%s]价格...' % item['chineseName'])
                cursor.execute(insert_t_product_price, (
                    item['productCode'], item['price'], item['sellerFlag'], item['pointFlag'], item['points'],
                    item['promotionFlag'], item['totalPrice'], item['extractTime']))
                # self.mariadb_connection.commit()
                logger.info(u'插入t_product_price成功...')
            except mariadb.Error as err:
                logger.error(u'插入t_product_price表失败. 原因为: %s' % err)
                self.mariadb_connection.rollback()

    def _update_t_product(self, cursor, item, flag=1):
        """
        更新已有商品的最低售价及平均价
        :param item: item对象
        :return: 
        """
        try:
            if flag == 1:
                update_t_product = "UPDATE t_product SET state = %s, chineseName = %s, imgUrl = %s, minPrice = %s, avgPrice = %s WHERE productCode = %s AND sellerFlag = %s"
                # cursor = self.mariadb_connection.cursor()
                logger.info(u'更新商品[%s]最低售价及平均价...' % item['chineseName'])
                cursor.execute(update_t_product, (
                    item['state'], item['chineseName'], item['imgUrl'], item['minPrice'], item['avgPrice'],
                    item['productCode'], item['sellerFlag']))
                # self.mariadb_connection.commit()
            else:
                update_t_product = "UPDATE t_product SET state = %s, chineseName = %s, imgUrl = %s, avgPrice = %s WHERE productCode = %s AND sellerFlag = %s"
                logger.info(u'更新商品[%s]平均价...' % item['chineseName'])
                cursor.execute(update_t_product, (
                    item['state'], item['chineseName'], item['imgUrl'], item['avgPrice'], item['productCode'],
                    item['sellerFlag']))
            logger.info(u'更新t_product成功...')
        except mariadb.Error as err:
            logger.error(u'更新历史最低价及平均价失败. 原因为: %s', err)

    def _send_email(self, mail_item_list):
        # logger.info(mail_item_list)
        html_content = self._gen_html_content(mail_item_list)
        logger.info(html_content)

        smtp_host = get_project_settings().get('SMTP_HOST')
        mail_from = get_project_settings().get('MAIL_FROM')
        mail_to = ",".join(get_project_settings().get('MAIL_TO'))
        smtp_user = get_project_settings().get('SMTP_USER')
        smtp_pass = get_project_settings().get('SMTP_PASS')
        smtp_port = get_project_settings().get('SMTP_PORT')
        subject = '哇涩，又有最新低价,赶紧查看~~~'

        msg = MIMEText(html_content, _subtype='html', _charset='utf8')
        msg['Subject'] = subject
        msg['From'] = mail_from
        msg['To'] = mail_to
        try:
            # s = smtplib.SMTP()
            s = smtplib.SMTP_SSL(host=smtp_host, port=smtp_port)
            # s.connect(smtp_host, smtp_port)
            # s.login(smtp_user, smtp_pass)
            s.ehlo()
            # s.starttls()  # enable TLS
            # s.ehlo()
            s.login(smtp_user, smtp_pass)
            s.sendmail(mail_from, mail_to, msg.as_string())
            s.close()
            logger.info(u'发送邮件成功...')
            return True
        except Exception, e:
            logger.error(u'邮件发送失败,原因为: %s' % e)
            is_success = False
            times = 1
            while not is_success:
                logger.info(u'正在尝试第[%s]次重新发送邮件...' % times)
                # 休眠3秒再尝试新的连接
                time.sleep(3)
                is_success = self._send_email(mail_item_dict.values())
                times += 1
                if times == 4:
                    logger.error(u'邮件发送失败...')
                    break

    def _gen_html_content(self, mail_item_list):
        date = datetime.datetime.now().strftime('%Y%m%d_%H:%M:%S')
        html_one = u"""
                    <html xmlns="http://www.w3.org/1999/xhtml">
                    <head>
                        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                        <title>商品最低价上报</title>
                    <body>
                        <div id="container">
                            <p><strong>最新低价商品统计</strong></p>
                            <p>统计时间: """ + date + """</p>
                                <table width="1400" border="2" bordercolor="green" cellspacing="2">
                                    <div id="content">
                                        <tr>
                                            <td><strong>序号</strong></td>
                                            <td><strong>商品名称</strong></td>
                                            <td><strong>商品图片</strong></td>
                                            <td><strong>商品URL</strong></td>
                                            <td><strong>销售标识</strong></td>
                                            <td><strong>促销标识</strong></td>
                                            <td><strong>当前价</strong></td>
                                            <td><strong>积分</strong></td>
                                            <td><strong>最后价(扣减积分)</strong></td>
                                            <td><strong>历史最低价</strong></td>
                                            <td><strong>历史平均价</strong></td>
                                        </tr>
                """
        html_two = ""
        for index, item in enumerate(mail_item_list):
            index += 1
            total_price = unicode(int(float(item['price']) - float(item['points'])))
            tr = u"""
                    <tr>
                        <td>""" + unicode(index) + """</td>
                        <td>""" + item['chineseName'] + """</td>
                        <td> <img width="120px" height="120px" src='""" + item['imgUrl'] + """'/></td>
                        <td>""" + item['productUrl'] + """</td>
                        <td>""" + self._get_seller_info(int(item['sellerFlag'])) + """</td>
                        <td>""" + self._get_promotion_info(int(item['promotionFlag'])) + """</td>
                        <td>""" + item['price'] + """</td>
                        <td>""" + item['points'] + """</td>
                        <td>""" + total_price + """</td>
                        <td>""" + item['minPrice'] + """</td>
                        <td>""" + item['avgPrice'] + """</td>
                        </tr>
                        """
            html_two += tr

        html_three = u"""
                </table>
                        </div>
                    </div>
                    </div>
                </body>
                </html>
                """
        html_content = str(html_one + html_two + html_three)
        return html_content

    def _get_seller_info(self, seller_flag):
        if seller_flag == 1:
            return unicode('自营')
        elif seller_flag == 2:
            return unicode('联营')
        else:
            return unicode('第三方')

    def _get_promotion_info(self, point_flag):
        return unicode('当前有促销活动') if point_flag == 1 else unicode('暂无促销活动')
