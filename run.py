import sys, os
from appdc import create_app
import appdc.cmdTH.cmd as cmdM
import appdc.ovsnew.tool as ovsTool

sys.path.insert(0, "/Users/cx/Desktop/cx/croot/pnetserver/3lib")

app = create_app()

@app.route('/12345')
def index():
    return "-12345"

if __name__ == "__main__":
    print(f"脚本名：{sys.argv[0]}")
    for i in range(1, len(sys.argv)):
        print(f"参数{i}:sys.argv[i]")
    if len(sys.argv) == 0: 
        cmdM.main()
    else:
        #ovsTool.prepare()
        app.run('0.0.0.0', '80', threaded=False, processes=64)


