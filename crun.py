import appdc.cmd.cmd as cmdM
import sys

if __name__=='__main__':
    print("脚本名：" + sys.argv[0])
    for i in range(1, len(sys.argv)):
        print("参数"+str(i)+str(sys.argv[i]))
    cmdM.main()


