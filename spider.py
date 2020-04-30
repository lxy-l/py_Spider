import urllib.request as urllib
import urllib.error as urlliberror
import MysqlDB
from bs4 import BeautifulSoup
import requests
import mysql.connector
import time
import json
import re

baseURL = 'https://search.bidcenter.com.cn/search?keywords=BIM&page='
headers = {
	"authority":"search.bidcenter.com.cn",
	"method": "GET",
	"path": "/search?keywords=BIM&page=3",
	"scheme": "https",
	"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	"accept-encoding": "gzip,deflate,br",
	"accept-language": "zh-CN,zh;q=0.9",
	"cache-control": "max-age=0",
	"cookie": "bidguidnew=2746c834-c786-4e3f-abe2-20970c9a1f7e; bidguid=c67554c9-ffee-4a0a-a963-1049001ffa78; keywords==BIM; UM_distinctid=16f82aaced89f4-079d047d0a71cd-6a547d2e-1fa400-16f82aaced9bf1; CNZZDATA888048=cnzz_eid%3D1334948636-1578444044-%26ntime%3D1578444044; Hm_lvt_9954aa2d605277c3e24cb76809e2f856=1578445230; Hm_lpvt_9954aa2d605277c3e24cb76809e2f856=1578446537",
	"referer": "https://search.bidcenter.com.cn/search?keywords=BIM",
	"sec-fetch-mode":"navigate",
	"sec-fetch-site":"same-origin",
	"sec-fetch-user":"?1",
	"upgrade-insecure-requests":"1",
	"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3970.5 Safari/537.36"
}

dbConfig = {
    'host': 'loclhost',
    'user': 'root',
    'password': '962921921',
    'port': 3306,
    'database': 'py_database',
    'charset': 'utf8mb4'
}

def Findhref(baseURL,headers,pageNum,db):
    rep=requests.get(url=baseURL+str(pageNum), headers=headers)
    html=rep.text
    bf = BeautifulSoup(html,features="html.parser")
    table=bf.find(id="jq_project_list")
    for tr in table.find_all("tr"):
        td1=tr.find(name="td",attrs={"class":"zb_title"})   #链接标题
        td2=tr.find(name="td",attrs={"class":"list_time"})  #时间
        td3=tr.find(name="td",attrs={"class":""})           #结果
        td4=tr.find(name="td",attrs={"class":"list_area"})  #链接地区
        if(td1!=None):
            db.Insert("INSERT INTO py_spider (Title,TitleLink,Type,Address, Time)VALUES(%s, %s, %s, %s, %s )",(td1.find('a').text.strip(),td1.find('a').get('href').strip(),td3.text.strip(),td4.find('a').text.strip(),td2.text))
            # print("链接:"+td1.find('a').get('href')+"  标题:"+td1.find('a').text+"  时间："+td2.text+" 类型："+td3.text+" 地区："+td4.find('a').text)

def main():
    db=MysqlDB(dbConfig)
    i=1
    while i<=10:
        print("开始爬取第"+str(i)+"页")
        Findhref(baseURL,headers,i,db)
        i+=1
    db.Select("select * from py_spider")
    db.close()
    print("爬取完成，3s后数据库关闭...")

class MysqlDB:
    
   def __init__(self,dbConfig):
       try:
           self.db=mysql.connector.connect(**dbConfig)
           self.cursor = self.db.cursor()
           self.cursor.execute("SELECT VERSION()")
           data = self.cursor.fetchone()
           print ("数据库版本: %s " % data)
       except mysql.connector.Error as e:
           print('connect fails!{}'.format(e))

   def close(self):
       if self.cursor != None:
           self.cursor.close()
       if self.db != None:
           self.db.close()
       print("数据库关闭...")
      
   def __items(self,sqlCommand,params=None):
       count=0
       try:
           count=self.cursor.execute(sqlCommand,params)
           self.db.commit()
       except Exception as e:
           print(e)
       return count

   def Insert(self,sqlCommand,params=None):
       return self.__items(sqlCommand, params)

   def Delete(self,sqlCommand,params=None):
       return self.__items(sqlCommand,params)

   def Update(self,sqlCommand,params=None):
       return self.__items(sqlCommand,params)

   def SelectSingle(self,sqlCommand, params=None):
       dataOne = None
       try:
           count = self.cursor.execute(sqlCommand, params)
           if count != 0:
               dataOne = self.cursor.fetchone()
       except Exception as ex:
           print(ex)
       return dataOne

   def Select(self, sqlCommand, params=None):
       dataall = None
       try:
           count = self.cursor.execute(sqlCommand, params)
           if count != 0:
               dataall = self.cursor.fetchall()
       except Exception as ex:
           print(ex)
       return dataall
  
if __name__ == "__main__":
    main()
    time.sleep(3)
