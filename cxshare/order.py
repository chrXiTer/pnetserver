import json
import dbMysql
import time

def addOrder(userInfo, orderContent):
    orderStatus = object()
    orderStatus.main = "add"
    uiJsonStr = json.dumps(userInfo)
    ocJsonStr = json.dumps(orderContent)
    osJsonStr = json.dumps(orderStatus)
    timestamp = int(time.time())
    version = 1
    conn = dbMysql.getDBConnect()
    dbMysql.insertDataToDb(conn, 'order', 
        ['USER_INFO', 'ORDER_CONTENT', 'ORDER_STATUS', 'TIMESTAMP', 'VERSION'],
        [uiJsonStr, ocJsonStr, osJsonStr, timestamp, version])
    
    conn.close()

def getOrder(ID):
    conn = dbMysql.getDBConnect()
    data = dbMysql.selectOneDataById(conn, 'order', ['USER_INFO', 'ORDER_CONTENT', 'ORDER_STATUS', 'VERSION'], ID)
    return data
