# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql.cursors
import pymysql


class QidianPipeline(object):

    def process_item(self, item, spider):
        connection = pymysql.connect(host='127.0.0.1',
                                     db='scrapy',
                                     user='scrapy',
                                     password='Abc,123.',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `article` WHERE  `onlyid` = %s AND `siteid` = %s "
                results = cursor.execute(sql, (
                    item['only_id'],
                    item['site_id'],
                ))
                # 如果没有该本书则进行插入，否则进行更新
                if results == 0:
                    sql = "INSERT INTO `article` (`siteid`,`sitename`,`articleid`,`articlename`,`author`,`onlyid`," \
                          "`lastedtime`,`lastedname`,`isfull`,`isvip`,`votes`,`articleurl`,`chaptersize`,`monthsvote`,`talks`,`moneyman`) VALUES" \
                          " (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql, (
                        item['site_id'],
                        item['site_name'],
                        item['article_id'],
                        item['article_name'],
                        item['author'],
                        item['only_id'],
                        item['lasted_time'],
                        item['lasted_name'],
                        item['is_full'],
                        item['is_vip'],
                        item['votes'],
                        item['article_url'],
                        item['chapter_size'],
                        item['months_vote'],
                        item['talks'],
                        item['money_man'],
                    ))
                else:
                    sql = "UPDATE `article` SET `siteid` = %s, `sitename` = %s,`articleid` = %s,`articlename` = %s,`author` = %s," \
                          "`lastedtime` = %s,`lastedname` = %s,`isfull` = %s,`isvip` = %s,`votes` = %s,`articleurl` = %s,`chaptersize` = %s, `monthsvote` = %s,`talks` = %s,`moneyman` = %s WHERE  `onlyid` = %s AND `siteid` = %s"
                    cursor.execute(sql, (
                        item['site_id'],
                        item['site_name'],
                        item['article_id'],
                        item['article_name'],
                        item['author'],
                        item['lasted_time'],
                        item['lasted_name'],
                        item['is_full'],
                        item['is_vip'],
                        item['votes'],
                        item['article_url'],
                        item['chapter_size'],
                        item['months_vote'],
                        item['talks'],
                        item['money_man'],

                        item['only_id'],
                        item['site_id'],
                    ))
                connection.commit()
        finally:
            connection.close()
        return item
