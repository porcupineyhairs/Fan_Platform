a = [{'eq': ['status_code', 200]}, {'eq': ['body.text', '我是棒棒哒图灵机器人']}, {'eq': ['code', 10000]}]
b = [{"dq": ["status_code", 200]}, {"eq": ["body.text", "我是棒棒哒图灵机器人"]}, {"eq": ["code", 10000]}]

d = []
for i in a:
    for k, v in i.items():
        print(k,v)
        data = {k, v}
        d.append(data)

print(d)
