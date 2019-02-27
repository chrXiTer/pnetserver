import pymysql 
import os



def getDBConnect(host, user, password, dbName): # 打开数据库连接
    db = pymysql.connect(host, user, password, dbName)
    return db

def closeDBConnect(db):# 关闭数据库连接
    db.close()

def execSqlFile(db, sqlFilePath):
    cursor = db.cursor()
    with open(sqlFilePath, 'r+') as f: ##读取SQL文件,获得sql语句的list
        sql_list = f.read().split(';')[:-1]  # sql文件最后一行加上;
        sql_list = [x.replace('\n', ' ') if '\n' in x else x for x in sql_list]  # 将每段sql里的换行符改成空格
    try: ##执行sql语句，使用循环执行sql语句
        for sql_item in sql_list:
            cursor.execute(sql_item)
        db.commit()
        return 1
    except:
        db.rollback()
        return -1

def execUpdate(db, updateSql): # insert update delete
    cursor = db.cursor() 
    try:
        cursor.execute(updateSql)
        db.commit()
        return 1
    except:
        db.rollback()
        return -1

def selectOne(db, selectSql):
    cursor = db.cursor() # 使用 cursor() 方法创建一个游标对象 cursor
    cursor.execute(selectSql) # 使用 execute()  方法执行 SQL 查询 
    data = cursor.fetchone() # 使用 fetchone() 方法获取单条数据.
    return data