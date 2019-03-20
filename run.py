from appdc import create_app
import appdc.cmd.cmd as cmdM
import sys
import appdc.ovsnew.tool as ovsTool

app = create_app()

@app.route('/12345')
def index():
    return "-12345"

if __name__ == "__main__":
    print("脚本名：" + sys.argv[0])
    for i in range(1, len(sys.argv)):
        print("参数"+str(i)+str(sys.argv[i]))
    if len(sys.argv) == 0: 
        cmdM.main()
    else:
        sys.argv = []
        ovsTool.prepare()
        app.run('0.0.0.0', '80', threaded=False, processes=64)


