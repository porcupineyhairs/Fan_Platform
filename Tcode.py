caseApis = [
    {"method": "101", "url": "https://douban.uieee.com/v2/book/search?q=旅行&count=1", "account": "-1", "interval": "0",
     "params": [{"name": "q", "value": "旅行"}, {"name": "count", "value": "1"}], "header": [],
     "body": {"type": "101", "value": "{}"},
     "verify": {"type": "102", "value": [{"name": "$.count", "value": "1", "mode": "101"}]},
     "extract": {"type": "101", "value": [{"name": "count", "value": "$.count"}]}},
    {"method": "101", "url": "https://douban.uieee.com/v2/book/search?q=旅行&count={{count}}", "account": "-1",
     "interval": "0", "params": [{"name": "q", "value": "旅行"}, {"name": "count", "value": "{{count}}"}], "header": [],
     "body": {"type": "102", "value": [{"name": "aa", "value": "22", "type": "text"}]},
     "verify": {"type": "102", "value": [{"name": "", "value": "", "mode": "101"}]},
     "extract": {"type": "101", "value": []}}]

caseDesc = ""
caseName = "豆瓣test"
caseType = "200"
id = 3673
moduleId = 127
moduleType = 100
updateBy = "v-caoyongqi"
