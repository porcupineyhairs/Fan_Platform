# encoding: utf-8
"""
@auth: cyq
@name: current_app
@desc: current_app
"""
from flask import current_app, g

"""
再请求过程当中, 只要访问current_app, 想相当于访问其中资源
"""

from FlaskDemo import app


@app.route("/")
def index():
    g.user = "hello"
    print(current_app)
    return 'ok'
if __name__ == '__main__':
    app.run()
