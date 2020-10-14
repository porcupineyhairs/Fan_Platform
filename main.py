from flask_script import Manager
from gevent import monkey
from gevent.pywsgi import WSGIServer

from App import create_app

monkey.patch_all()
app = create_app()
manage = Manager(app)


def app_start():
    httpServer = WSGIServer(('127.0.0.1', 5000), app)

    httpServer.serve_forever()


if __name__ == '__main__':
    app.run(debug=False)
    # app_start()
