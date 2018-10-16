from appdc import create_app
from flask_script import Manager

app = create_app()

manager = Manager(app)

@app.route('/12345')
def index():
    return "-12345"

if __name__ == "__main__":
    manager.run()
