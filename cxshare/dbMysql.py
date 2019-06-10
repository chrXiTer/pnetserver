import pymysql 
import os



def getDBConnect(host, user, password, dbName): # 打开数据库连接
    conn = pymysql.connect(host, user, password, dbName)
    return db

def closeDBConnect(conn):# 关闭数据库连接
    conn.close()

def insertDataToDb(conn, tableName, colNameList, data):
    cursor = conn.cursor()
    strT1 = ", ".join(colNameList)
    strT2 = ", ".join(['"%s"' % data[colNameList[i]] for i in range(len(colNameList))])
    sqlStr = 'INSERT INTO %s (%s) VALUES (%s);' % (tableName, strT1, strT2)
    try:
        d1 = cursor.execute(sqlStr)
        d2 = conn.commit()
    except:
        conn.rollback()

def selectOneDataById(conn, tableName, colNameList, ID):
    strT1 = ", ".join(colNameList)
    sqlStr = 'SELECT %s FROM %s WHERE ID=%d;' % (strT1, tableName, ID)
    dataOri = selectOne(conn, sqlStr)
    return dataOri
    #data = [dataOri[colName] for colName in colNameList]
    #return data

def updateDataToDb(conn, tableName, colNameList, record):
    strs = []
    ID = None
    for i in range(len(colNameList)):
        recordValue = str(record[i])
        if type(record[i]).__name__ == 'str':
            recordValue = "'" + record[i] + "'"
        elif colNameList[i] == 'ID':
            ID = recordValue
        elif type(record[i]).__name__ == 'NoneType':
            recordValue = 'null'
        strs.append("`" + colNameList[i] + "` = " + recordValue)
    strT = ", ".join(strs)
    sqlStr = 'UPDATE %s set %s where ID=%s;' % (tableName, strT, ID)
    execUpdate(conn, sqlStr)

def getInsertId(db):
    return selectOne(db, 'SELECT LAST_INSERT_ID();')

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