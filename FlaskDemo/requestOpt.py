# encoding: utf-8
"""
@auth: cyq
@name: requestOpt
@desc: 钩子函数
"""

from FlaskDemo import app


@app.before_request  # 每次请求之前操作
def before_request():
    """
    1 需要某一时间段统计数据
    2 验证用户
    3 请求时间验证

    """
    print("before_request")




@app.teardown_request #  请求之后
def teardown_request(exception):
    """
    通常用来释放资源
    不管有没有错误都会被调用
    """
    print("teardown_request")


@app.after_request
def after_request(response):
    """
    response 响应 必填
    return 必须是一个Response对象
    用处用来修改响应
    视图出现错误不会调用
    """
    response.headers['you'] = 'momo'
    return response



