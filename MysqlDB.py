import mysql.connector
class MysqlDB:
    """Mysql Connect"""    
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


