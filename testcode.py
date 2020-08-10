a = [{'id': 1, 'name': '打开网页', 'desc': '打开网页', 'methodId': None, 'type': None, 'locator': None, 'do': 'get',
      'value': 'www.baidu.com', 'variable': None, 'validate': None},
     {'id': 2, 'name': '使用方法', 'desc': None, 'methodId': 1, 'type': None, 'locator': None, 'do': None, 'value': None,
      'variable': None, 'validate': None},
     {'id': 3, 'name': '截图', 'desc': None, 'methodId': None, 'type': None, 'locator': None, 'do': 'screenshot',
      'value': None, 'variable': None, 'validate': None},
     {'id': 4, 'name': 'get title', 'desc': None, 'methodId': None, 'type': None, 'locator': None, 'do': 'get_title',
      'value': None, 'variable': 'title', 'validate': '[{"eq": ["title", "python_百度搜索"]}]'}]

a.pop(0)
print(a)