from flask_script import Manager, Shell
from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
from App import create_app

app = create_app()

manage = Manager(app)

def app_start():
    httpServer = WSGIServer(('127.0.0.1', 5000), app)
    httpServer.serve_forever()



if __name__ == '__main__':
    app.run()
