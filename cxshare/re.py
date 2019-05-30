import re

def phone(strData): 
    #总长度11位，第一位为1,第二位为[3-9],第3-11位[0-9]
    pattern = r"[^\d]*((1[3-9])\d{9})[^\d]*"
    res0 = re.findall(pattern, strData)
    ret = [r[0] for r in res0]
    if len(res0) > 0:
        print("ddd")
    return ret

def idCard(strData):
    '''1- 6位：地区编码  [1-6]\d{5}
    7-10位：出生年份  (19|20)\d{2}
    11-12位：出生月份  (0[1-9]|1[12])
    13-14位：出生日子  (0[1-9]|1[0-9]|2[0-9]|3[01])
    15-18位；其它      \d{3}[\dXx]
    '''
    pattern = r"[^\d]*([1-6]\d{5}(19|20)\d{2}(0[1-9]|1[12])(0[1-9]|1[0-9]|2[0-9]|3[01])\d{3}[\dXx])[^\d]*"
    res0 = re.findall(pattern, strData)
    ret = [r[0] for r in res0]
    return ret

'''
    res = re.match(pattern, strData)
    if res:
        idValue = res.groups()[0]
        return idValue
    else:
        return None
'''

def qq(strData): #最少5位,最长11位
    pattern = r"[1-9]\d{4,10}" 
    res = re.findall(pattern, strData)
    return print(res)

def qqMail(): #带qq号的QQ邮箱
    pattern = r"[1-9]\d{4,10}\.com"
    return pattern

def mail(strData): #xxx(不定长)@xx(不定长).com/cn
    pattern = r"\w{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}"
    res = re.findall(pattern, strData, re.I)
    return print(res)

if __name__ == "__main__":
    idCard("ddddgg")
    idCard("dddd430421198902213153ggg dddd430421198902213152ggg")
    phone(" 13875610112 ")