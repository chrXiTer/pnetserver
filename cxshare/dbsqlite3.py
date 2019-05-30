import sqlite3
import file as cxfile
# import file as cxfile

def connToDB(dbpath): # 'test.db'
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    return conn, cursor

def createTable(conn, cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS webpc (url TEXT primary key, 
        time varchar(100),
        title TEXT,
        contentOri TEXT,
        contentText TEXT,
        contentJson TEXT,
        type integer)''') # 1 身份证  10 手机号  100 qq邮箱  1000 qq  10000 邮箱

def insertDataToDb(conn, cur, tableName, colNameList, dataList):
    strT1 = ", ".join(colNameList)
    for data in dataList:
        strT2 = ", ".join(['"%s"' % data[colNameList[i]] for i in range(len(colNameList))])
        sqlStr = 'INSERT INTO %s (%s) VALUES (%s);' % (tableName, strT1, strT2)
        cur.execute(sqlStr)
    conn.commit()

def reduceDBDataByIDNo(conn, cursor, tableName):
    cursor.execute('''
        SELECT `身份证`, `ID`, * FROM %s WHERE `身份证` IN (
                SELECT `身份证` FROM %s GROUP BY `身份证` HAVING COUNT(`身份证`) >=2
        ) ORDER BY `身份证`
    ''' % (tableName,tableName))
    tmpData = dict()
    colNameList = [tuple[0] for tuple in cursor.description]
    for row in cursor:
        IDNo = row[0]
        tmpData[IDNo]= tmpData.get(IDNo) or []
        tmpData[IDNo].append(list(row))
    idsNeedDelete = []

    def reduceRecord(idsNeedDelete, records):
        IDToDelete = records[0][1]
        for i in range(len(records[0])):
            if records[0][i] == None:
                records[0][i] = records[1][i]
            elif records[1][i] == None:
                records[1][i] = records[0][i]
            elif records[1][i] != records[0][i] and colNameList[i] != "ID":
                if colNameList[i] == "其它":
                    records[0][i] = records[0][i] + "$" + records[1][i]
                    records[1][i] = records[0][i] + "$" + records[1][i]
                else:
                    IDToDelete = -1
        if IDToDelete != -1:
            idsNeedDelete.append(IDToDelete)
            records.remove(records[0])
            if len(records) > 1:
                reduceRecord(idsNeedDelete, records)

    for IDNo in tmpData:
        records = tmpData[IDNo]
        reduceRecord(idsNeedDelete, records)
    
    for IDNo in tmpData:
        records = tmpData[IDNo]
        for record in records:
            updateDataToDB(conn, cursor, tableName, colNameList[2:-1], record[2:-1])
    for ID in idsNeedDelete:
        deleteDataFromDB(conn, cursor, tableName, ID)
    
def updateDataToDB(conn, cursor, tableName, colNameList, record):
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
    cursor.execute('UPDATE %s set %s where ID=%s;' % (tableName, strT, ID))
    conn.commit()

def deleteDataFromDB(conn, cursor, tableName, ID):
    cursor.execute('DELETE FROM %s WHERE ID=%s;' % (tableName, ID))
    conn.commit()


if __name__ == "__main__":
    conn, cursor = connToDB('/Users/cx/Desktop/ccc')
    #reduceDBDataByIDNo(conn, cursor, 'main')

    objList = cxfile.cvsToObjList("/Users/cx/Desktop/pc/proj/spiders/111.csv")
    insertDataToDb(conn, cursor, "main", ['姓名','身份证','性别','工作单位'], objList)

