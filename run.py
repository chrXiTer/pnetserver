from appdc import create_app
from flask_script import Manager
import appdc.cmd.cmd as cmdM
import sys

app = create_app()

manager = Manager(app)

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
        manager.run()


