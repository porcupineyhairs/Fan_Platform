# encoding: utf-8
"""
@auth: cyq
@name: flaskContent
@desc: flask 上下文
"""
import sys

from werkzeug.local import LocalStack

from FlaskDemo import app
from flask import _request_ctx_stack,_app_ctx_stack,appcontext_pushed,appcontext_popped

"""
1.最小原型app 是一个函数, 而flask 是一个对象,被调用执行 `__call__` 方法
2.app.__call__ 里的函数是 wsgi_app()
3.wsgi_app() 会根据环境变量数据实例化一个 RequestContext(env) 并执行ctx.push() 将请求上下文推入一个栈中
4.request_ctx.push() 先判断是否有一个 appContent 没有的话推入一个
5._request_ctx_stack.top  就是现在请求的对象  也是current_app 对象
6._app_ctx_stack.top 是现在app 对象  也就是request 
"""


def __call__(self, environ, start_response):
    return self.wsgi_app(environ, start_response)


def wsgi_app(self, environ, start_response):
    """
    environ 环境变量
    """
    ctx = self.request_context(environ)  # 初始化请求对象  RequestContext()
    error = None
    try:
        try:
            ctx.push()
            response = self.full_dispatch_request()
        except Exception as e:
            error = e
            response = self.handle_exception(e)
        except:  # noqa: B001
            error = sys.exc_info()[1]
            raise
        return response(environ, start_response)  # 返回对象
    finally:
        if self.should_ignore_error(error):
            error = None
        ctx.auto_pop(error)  # 最后删除

class RequestContext():

    def __init__(self, app, environ, request=None, session=None):
        self.app = app
        if request is None:
            request = app.request_class(environ)  # 就是一个Request 对象
        self.request = request
        self.flashes = None
        self.session = session

        self._implicit_app_ctx_stack = []
    def push(self):
        #top = _request_ctx_stack.top
         #   top.pop(top._preserved_exc)
        app_ctx = _app_ctx_stack.top
        if app_ctx is None or app_ctx.app != self.app:  #判斷
            app_ctx = self.app.app_context()
            app_ctx.push()
            self._implicit_app_ctx_stack.append(app_ctx)  #棧裏放入
        else:
            self._implicit_app_ctx_stack.append(None)

        _request_ctx_stack.push(self)


    # 上下文
    def __enter__(self):
        #   self.push()
        pass
    def __exit__(self, exc_type, exc_value, tb):
        #self.auto_pop(exc_value)
        pass

class AppContext(object):

    def __init__(self, app):
        self.app = app
        self.url_adapter = app.create_url_adapter(None)
        self.g = app.app_ctx_globals_class()

        # Like request context, app contexts can be pushed multiple times
        # but there a basic "refcount" is enough to track them.
        self._refcnt = 0

    def push(self):
        self._refcnt += 1
        if hasattr(sys, "exc_clear"):
            sys.exc_clear()
        _app_ctx_stack.push(self)
        appcontext_pushed.send(self.app)

    def pop(self, exc=_sentinel):
        try:
            self._refcnt -= 1
            if self._refcnt <= 0:
                if exc is _sentinel:
                    exc = sys.exc_info()[1]
                self.app.do_teardown_appcontext(exc)
        finally:
            rv = _app_ctx_stack.pop()
        assert rv is self, "Popped wrong app context.  (%r instead of %r)" % (rv, self)
        appcontext_popped.send(self.app)

    def __enter__(self):
        self.push()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.pop(exc_value)

        if BROKEN_PYPY_CTXMGR_EXIT and exc_type is not None:
            reraise(exc_type, exc_value, tb)

"""
#context locals
_request_ctx_stack = LocalStack() #LocalStack()包含pop、push方法以及Local对象，上下文通过该对象push和pop
_app_ctx_stack = LocalStack()
current_app = LocalProxy(_find_app)
request = LocalProxy(partial(_lookup_req_object, 'request')) #reuqest是LocalProxy的对象，设置和获取request对象中的属性通过LocalProxy定义的各种双下划线实现
session = LocalProxy(partial(_lookup_req_object, 'session'))
g = LocalProxy(partial(_lookup_app_object, 'g'))"""
if __name__ == '__main__':
    app.run()
