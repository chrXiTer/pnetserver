from telnetlib import Telnet


# 调用telnet对象的 expect 函数，成功后调用 onSuccess，否则打印错误信息
def expect2(tn, regList, timeout, onSuccess):
    ret = tn.expect(regList, timeout)
    if ret[0] != -1 :
        onSuccess()
    else:
        print("cx error")

# telnet 连接到主机并执行命令
def do_telnet(host, username, password, finish, commands):     
    tn = Telnet(host, port=23, timeout=10)  
    tn.set_debuglevel(2)  

    if username:
        expect2(tn, [r'login: '], 10, 
            lambda tn, username: tn.write(username.encode('utf8') + b"\n"))
    if password:
        expect2(tn, [r'Password: '], 10,
            lambda tn, username: tn.write(password.encode('utf8') + b"\n"))
    tn.read_until(finish)

    for command in commands:
        tn.write(b'%s\n' % command.encode('utf8'))
    tn.read_until(finish)

    tn.close() # tn.write('exit\n')  

if __name__=='__main__':  
    host = '10.255.254.205' # Telnet服务器IP  
    username = 'administrator'   # 登录用户名  
    password = 'dell1950'  # 登录密码  
    finish = ':~$ '      # 命令提示符  
    commands = ['echo "test"']  
    do_telnet(host, username, password, finish, commands)

