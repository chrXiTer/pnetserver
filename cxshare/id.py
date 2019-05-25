import re

def getIdLastChar2(id):  # 与 getIdLastChar 一样，根据身份证前17位的值，计算第18位校验位的值
    def for_check(n):   # return [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2][n]
        for i in range(0,12):
            if (n + i) % 11 == 1:
                t = i % 11
        if t == 10:
            t = 'X'
        else:
            t = str(t)
        return t

    def for_mod(id): # 根据身份证的前17位，求和取余，返回余数
        w = [(2 ** i) % 11 for i in range(0, 18)] # w表示每一位的加权因子
        w = w[::-1] #队列 w 做反序得到 [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1]
        sum = 0
        for i in range(0,17):
            sum += int(id[i]) * int(w[i])
        sum = sum % 11
        return sum
    return for_check(for_mod(id[:-1]))



def getIdLastChar(id): # 根据身份证前17位的值，计算第18位校验位的值
    idcard_list=list(id)
    idcard_ints=[int(n) for n in idcard_list[:17]]
    S =((idcard_ints[0] + idcard_ints[10]) * 7 + 
        (idcard_ints[1] + idcard_ints[11]) * 9 + 
        (idcard_ints[2] + idcard_ints[12]) * 10 + 
        (idcard_ints[3] + idcard_ints[13]) * 5 + 
        (idcard_ints[4] + idcard_ints[14]) * 8 + 
        (idcard_ints[5] + idcard_ints[15]) * 4 + 
        (idcard_ints[6] + idcard_ints[16]) * 2 + 
        idcard_ints[7] * 1 + idcard_ints[8] * 6 + idcard_ints[9] * 3 
    )
    Y = S % 11
    M = "10X98765432"[Y] #判断校验位
    return M

def check_true(id): # 检查身份证校验位有效性
    return getIdLastChar(id) == id[-1]  #id[17]

def checkIdcard(idcard):
    Errors=['验证通过!','身份证号码位数不对!','身份证号码出生日期超出范围或含有非法字符!',
        '身份证号码校验错误!','身份证地区非法!']
    idcard=str(idcard)
    idcard=idcard.strip()
    
    area={"11":"北京","12":"天津","13":"河北","14":"山西","15":"内蒙古","21":"辽宁","22":"吉林",
        "23":"黑龙江","31":"上海","32":"江苏","33":"浙江","34":"安徽","35":"福建","36":"江西",
        "37":"山东","41":"河南","42":"湖北","43":"湖南","44":"广东","45":"广西","46":"海南",
        "50":"重庆","51":"四川","52":"贵州","53":"云南","54":"西藏","61":"陕西","62":"甘肃",
        "63":"青海","64":"宁夏","65":"新疆","71":"台湾","81":"香港","82":"澳门","91":"国外"}
    if(not area[(idcard)[0:2]]): #地区校验
        return Errors[4]
    if(len(idcard)==15): #15位身份号码检测
        if((int(idcard[6:8])+1900) % 4 == 0 or((int(idcard[6:8])+1900) % 100 == 0 and (int(idcard[6:8])+1900) % 4 == 0 )):
            ereg=re.compile('[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}$')#//测试出生日期的合法性
        else:
            ereg=re.compile('[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}$')#//测试出生日期的合法性
        if(not re.match(ereg,idcard)):
            return Errors[2]
    elif(len(idcard)==18):#18位身份号码检测
        #闰年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))
        #平年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))
        if(int(idcard[6:10]) % 4 == 0 or (int(idcard[6:10]) % 100 == 0 and int(idcard[6:10])%4 == 0 )):
            ereg=re.compile('[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9Xx]$')#//闰年出生日期的合法性正则表达式
        else:
            ereg=re.compile('[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}[0-9Xx]$')#//平年出生日期的合法性正则表达式
        if(not re.match(ereg,idcard)): #出生日期的合法性检查
            return Errors[2]
        if(not check_true(idcard)):
            return Errors[3]
    else:
        return Errors[1]
    return Errors[0]

def _genId(i1, i2,i3,i4,i5):   # 垃圾python，不支持尾调用
    i5 = i5 + 1
    if(i5 > 999):
        i5 = 0
        i4 = i4 + 1
        if(i4 > 31):
            i4 = 1
            i3 = i3 + 1
            if(i3 > 12):
                i3 = 1
                i2 = i2 - 1
    id = i1 + str(i2) + str(i3).zfill(2) + str(i4).zfill(2) + str(i5).zfill(3)
    i6 = getIdLastChar(id)
    id = id + i6
    return id, i2, i3, i4, i5

def genIdHY(lastId):
    i1 = lastId[0:6]
    i2 = int(lastId[6:10])
    i3 = int(lastId[10:12])
    i4 = int(lastId[12:14])
    i5 = int(lastId[14:17])
    id, i2, i3, i4, i5 = _genId(i1, i2,i3,i4,i5)
    while(1):
        if(checkIdcard(id) == '验证通过!'):
            yield id    
        id, i2, i3, i4, i5 = _genId(i1, i2,i3,i4, i5)

if __name__ == "__main__":
    #print(checkIdcard('430421198902213153'))
    #print(check_true('430421198902213153'))
    print(genIdHY('430421199301010005'))

    






